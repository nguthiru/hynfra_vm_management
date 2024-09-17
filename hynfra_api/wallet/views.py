from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from .models import *
from .serializers import *
from users.permissions import IsAdmin, IsStandardUser
from .permissions import has_exceeded_vm_plan, has_exceeded_backup_plan


class BillingProfileViewset(viewsets.ReadOnlyModelViewSet):
    queryset = BillingProfile.objects.all()
    serializer_class = BillingProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # create users billing profile if it doesnt exist
        if not BillingProfile.objects.filter(user=user).exists():
            BillingProfile.objects.create(user=user)
        if user.is_admin():
            return BillingProfile.objects.all()
        return BillingProfile.objects.filter(user=user)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        user = request.user
        if not BillingProfile.objects.filter(user=user).exists():
            BillingProfile.objects.create(user=user)
        billing_profile = BillingProfile.objects.get(user=user)
        serializer = self.get_serializer(billing_profile)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_users(self, request, *args, **kwargs):
        """
        Allows the user to add to their billing profile
        """
        user_ids = request.data.get("user_ids")
        if user_ids is None or len(user_ids) == 0:
            return Response({"detail": "Please provide user_ids"}, status=400)

        billing_profile = self.get_object()
        if billing_profile.user == request.user or request.user.is_admin():

            for user_id in user_ids:
                user = get_object_or_404(User, id=user_id)

                # check if user is already in another profile
                if BillingProfileChild.objects.filter(user=user).exists():
                    return Response(
                        {
                            "detail": f"User with id: {user_id } already linked to a billing profile."
                        },
                        status=400,
                    )

                BillingProfileChild.objects.get_or_create(
                    billing_profile=billing_profile, user=user
                )
            return Response({"detail": "Users added successfully."})
        else:
            return Response(
                {"detail": "Not authorized to add users to this billing profile."},
                status=403,
            )


class ChildBillingProfileViewset(viewsets.ModelViewSet):
    queryset = BillingProfileChild.objects.all()
    serializer_class = BillingProfileChildSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return BillingProfileChild.objects.all()
        return BillingProfileChild.objects.filter(billing_profile__user=user)

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_admin():
            raise PermissionDenied("Only admins can create child billing profiles.")
        serializer.save()

    @action(detail=False, methods=["POST"])
    def add_user(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if user_id is None:
            return Response({"detail": "Please provide user_id"}, status=400)
        user = get_object_or_404(User, id=user_id)
        billing_profile = BillingProfile.objects.filter(user=request.user)

        if billing_profile.exists():
            billing_profile = billing_profile.first()
            # check if it already exists
            if BillingProfileChild.objects.filter(user=user).exists():
                return Response(
                    {"detail": "User already linked to a billing profile."}, status=400
                )
                
            else:
                
                billing_profile_child = BillingProfileChild.objects.create(
                    billing_profile=billing_profile, user=user
                )
                return Response({"detail": "User added successfully."})
        return Response({"detail": "Billing profile not found."}, status=400)

    @action(detail=False, methods=["GET"])
    def active_users(self, request, *args, **kwargs):
        active_users = self.get_queryset().filter(active=True)
        # paginate
        page = self.paginate_queryset(active_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(active_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def deactivate_user(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if user_id is None:
            return Response({"detail": "Please provide user_id"}, status=400)
        user = BillingProfileChild.objects.filter(
            user__id=int(user_id), billing_profile__user=request.user
        )
        billing_profile_child = self.get_queryset().filter(user__id=int(user_id))
        if billing_profile_child.exists():
            billing_profile_child = billing_profile_child.first()
            billing_profile_child.active = False
            billing_profile_child.save()
            return Response({"detail": "User deactivated successfully."})
        return Response({"detail": "User not found."}, status=400)

    @action(detail=False, methods=["GET"])
    def inactive_users(self, request, *args, **kwargs):
        inactive_users = self.get_queryset().filter(active=False)
        # paginate
        page = self.paginate_queryset(inactive_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(inactive_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def activate_user(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if user_id is None:
            return Response({"detail": "Please provide user_id"}, status=400)

        billing_profile_child = self.get_queryset().filter(user__id=user_id)
        if billing_profile_child.exists():
            billing_profile_child = billing_profile_child.first()
            billing_profile_child.active = True
            billing_profile_child.save()
            return Response({"detail": "User activated successfully."})
        return Response({"detail": "User not found."}, status=400)


class RatePlanViewset(viewsets.ReadOnlyModelViewSet):
    queryset = RatePlan.objects.all()
    serializer_class = RatePlanSerializer

    @action(detail=True, methods=["post"])
    def upgrade(self, request, *args, **kwargs):
        user = request.user
        rate_plan = self.get_object()
        try:
            billing_profile = BillingProfile.objects.get(user=user)
            subscription = Subscription.objects.filter(billing_profile=billing_profile)

            if subscription.first().rate_plan == rate_plan:
                return Response(
                    {"detail": "You are already subscribed to this plan."},
                    status=400,
                )
            if has_exceeded_vm_plan(user, rate_plan):
                return Response(
                    {
                        "detail": "You have exceeded the maximum number of virtual machines allowed for this plan."
                    },
                    status=400,
                )
            if has_exceeded_backup_plan(user, rate_plan):
                return Response(
                    {
                        "detail": "You have exceeded the maximum number of backups allowed for this plan."
                    },
                    status=400,
                )
            subscription, _ = Subscription.objects.get_or_create(
                billing_profile=billing_profile
            )
            subscription.rate_plan = rate_plan
            subscription.save()

            return Response(
                {
                    "detail": "Plan Changed successfully.",
                    "data": SubscriptionSerialiser(subscription).data,
                }
            )

        except BillingProfile.DoesNotExist:
            return Response({"detail": "Billing Profile does not exist."}, status=400)


class SubscriptionViewset(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerialiser


class InvoiceViewset(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Invoice.objects.all()
        return Invoice.objects.filter(billing_profile__user=user)

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_admin():
            raise PermissionDenied("Only admins can create invoices.")
        serializer.save()

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
    )
    def pay(self, request, pk=None):

        serializer = InvoicePaymentSerializer(data=request.data)
        if serializer.is_valid():
            invoices = Invoice.objects.filter(
                id__in=serializer.validated_data["invoices"],
            )
            total = 0
            for invoice in invoices:
                if (
                    request.user.is_admin()
                    or invoice.billing_profile.user == request.user
                ):
                    if not invoice.is_paid:
                        total += invoice.total
                        # FIXME: Change to using callbacks etc in production
                        payments = Payment.objects.create(
                            invoice=invoice, amount=invoice.total, method="mock"
                        )

                        return Response(
                            {"detail": "Invoices paid successfully.", "amount": total}
                        )
                else:
                    raise PermissionDenied("Not authorized to pay this invoice.")
        return Response(serializer.errors, status=400)
