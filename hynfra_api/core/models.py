from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from typing import Type
User = get_user_model()

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class VirtualMachine(TimestampMixin):
    class StatusChoices(models.TextChoices):
        CREATED = "created", "Created"
        RUNNING = "running", "Running"
        STOPPED = "stopped", "Stopped"
        DELETED = "deleted", "Deleted"
        PAUSED = "paused", "Paused"

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='vms', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_running = models.BooleanField(default=False)
    disk_size_gb = models.PositiveIntegerField(default=20)
    cpu_core_count = models.PositiveIntegerField(default=1)
    ram_size_gb = models.PositiveIntegerField(default=2)
    status = models.CharField(max_length=100, choices=StatusChoices.choices,default=StatusChoices.CREATED)
    ip_address = models.CharField(
        max_length=255, null=True, blank=True, default=None
    )

    def __str__(self):
        return self.name
    
    @property
    def backup_cost(self):
        """
        Calculate the cost of creating a backup for this VM
        For simplicity, we'll just charge $0.1 per GB.
        """
        return self.disk_size_gb * 0.1

    

    def stop_vm(self):
        self.is_running = False
        self.status = self.StatusChoices.STOPPED
        self.save()

    def start_vm(self):
        self.is_running = True
        self.status = self.StatusChoices.RUNNING
        self.save()

    def delete(self, *args, **kwargs):
        self.status = self.StatusChoices.DELETED
        self.save()

@receiver(
    models.signals.post_save, sender=VirtualMachine
)
def create_vm_instance(sender,instance,created,*args, **kwargs):
    if created:
        #FIXME: create a random ip_address
        
        instance.ip_address = '128.1.72.122'
        instance.save()

class VirtualMachineBackup(TimestampMixin):

    class BackupStatus(models.TextChoices):
        CREATED = "created", "Created"
        IN_PROGRESS = "in_progress", "In Progress"


    vm = models.ForeignKey(VirtualMachine, related_name='backups', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    backup_size = models.FloatField(
        help_text="Size of the backup in GB",
        null=True,blank=True
    )
    status = models.CharField(
        max_length=100, choices=BackupStatus.choices, default=BackupStatus.CREATED
    )




    def __str__(self):
        return f"{self.name} for VM '{self.vm.name}'"
    
    @classmethod
    def create_backup(cls, vm : Type[VirtualMachine]) :
        return cls.objects.create(vm=vm, name=f"{vm.name} Backup",backup_size = vm.disk_size_gb)

