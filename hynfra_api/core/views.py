from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import *
from .serializers import VirtualMachineSerializer,VirtualMachineBackupSerializer
from users.permissions import IsAdmin
from django.contrib.auth import get_user_model
from audit.models import AuditLog
from wallet.models import InvoiceItem, Invoice, RatePlan
from django.utils import timezone
from wallet.utils import invoice_item
from wallet.permissions import has_exceeded_backup_plan, has_exceeded_vm_plan

User = get_user_model()


class VirtualMachineViewSet(viewsets.ModelViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():  # Admins can see all VMs
            return VirtualMachine.objects.all()
        return VirtualMachine.objects.filter(
            owner=user,
        )  # Others can only see their own VMs

    def perform_create(self, serializer):
        if not self.request.user.is_staff:  # Check if the user is an admin
            raise PermissionDenied("Only admins can create VMs.")

        # Admins can specify the owner of the VM
        owner = self.request.data.get("owner")
        if not owner:
            raise PermissionDenied("Owner must be specified for the VM.")

        try:
            user = User.objects.get(pk=owner)
        except User.DoesNotExist:
            raise ValidationError("User does not exist.")
        
        # Check if the user has exceeded the VM plan
        if has_exceeded_vm_plan(user):
            raise ValidationError("User has exceeded the VM Limit.")

        serializer.save(owner=user)

    def destroy(self, request, *args, **kwargs):
        vm = self.get_object()
        if request.user.is_admin() or vm.owner == request.user:
            vm.stop_vm()
            vm.delete()
            return Response(
                {"message": "VM deleted successfully"}, status=status.HTTP_204_NO_CONTENT
            )
            
        return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["post"])
    def backup(self, request, pk=None):
        vm = self.get_object()
        if vm.owner == request.user or request.user.is_admin():

            # check if user has exceeded backup plan
            if has_exceeded_backup_plan(vm.owner):
                return Response(
                    {"detail": "Backup limit exceeded."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if vm.status == VirtualMachine.StatusChoices.DELETED:
                return Response(
                    {"detail": "Cannot backup a deleted VM."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            vm_backup = VirtualMachineBackup.create_backup(vm=vm)
            # log the backup
            AuditLog.objects.create(
                action="VM Backup",
                user=request.user,
                content_object=vm,
                details=f"Backup '{vm.name}' created for VM '{vm.name}'.",
            )

            # create an invoice on the item
            invoice_item(
                user=vm.owner,
                amount=vm.backup_cost,
                name=f"Backup of {vm.name}",
                content_object=vm_backup,
            )

            backup_status = f"Backup '{vm.name}' created for VM '{vm.name}'."
            return Response({"status": backup_status})
        return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["post"])
    def stop(self, request, pk=None):
        vm = self.get_object()
        if vm.owner == request.user or request.user.is_admin():
            vm.stop_vm()
            AuditLog.objects.create(
                action="VM Stop",
                user=request.user,
                content_object=vm,
                details=f"VM '{vm.name}' was stopped.",
            )
            return Response({"status": f"VM '{vm.name}' stopped."})
        return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        vm = self.get_object()
        if vm.owner == request.user or request.user.is_admin():
            vm.start_vm()
            AuditLog.objects.create(
                action="VM Start",
                user=request.user,
                content_object=vm,
                details=f"VM '{vm.name}' was started.",
            )
            return Response({"status": f"VM '{vm.name}' started."})
        return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["get"])
    def backup_cost(self, request, *args, **kwargs):
        vm = self.get_object()
        if vm.owner == request.user or request.user.is_admin():
            cost = vm.backup_cost
            return Response({"backup_cost": cost})
        return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsAdmin]
    )
    def transfer(self, request, pk=None):
        vm = self.get_object()

        new_owner_id = request.data.get("new_owner")
        if not new_owner_id:
            return Response(
                {"detail": "New owner must be specified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            new_owner = User.objects.get(pk=new_owner_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        # Transfer ownership
        old_owner = vm.owner
        vm.owner = new_owner
        vm.save()

        # Send notifications (simplified for now)
        # In production, we can use celery to send it to a background worker
        # old_owner.email_user("VM Transferred", f"Your VM '{vm.name}' has been transferred to another user.")
        # new_owner.email_user("New VM Assigned", f"You have been assigned a new VM: '{vm.name}'.")

        audit_log = AuditLog.objects.create(
            action="VM Transfer",
            user=request.user,
            content_object=vm,
            details=f"VM '{vm.name}' was transferred from {old_owner.username} to {new_owner.username}.",
        )

        return Response(
            {"detail": "VM successfully transferred.", "log_id": audit_log.id}
        )
    @action(methods=["GET"],detail=True)
    def backup_history(self,request,*args, **kwargs):
        vm = self.get_object()
        queryset = VirtualMachineBackup.objects.filter(vm=vm).order_by("-created_at")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = VirtualMachineBackupSerializer(
                page, many=True
            )
            return self.get_paginated_response(serializer.data)

        # If pagination is not applied, just return the serialized data
        serializer = VirtualMachineBackupSerializer(queryset, many=True)
        return Response(serializer.data)
