from typing import Type
from core.models import VirtualMachine,VirtualMachineBackup
from django.contrib.auth import get_user_model
from .models import BillingProfile,Subscription
from .utils import get_billing_profile
User = get_user_model()
def has_exceeded_vm_plan(user, rate_plan =None):
    if rate_plan is None:
        billing_profile = get_billing_profile(user)
        rate_plan = Subscription.objects.get(billing_profile=billing_profile).rate_plan
    if rate_plan.max_vms < VirtualMachine.objects.filter(owner=user).count():
        return True
    return False

def has_exceeded_backup_plan(user,rate_plan=None):
    if rate_plan is None:
        billing_profile = get_billing_profile(user)
        rate_plan = Subscription.objects.get(billing_profile=billing_profile).rate_plan
    if rate_plan.max_backups < VirtualMachineBackup.objects.filter(vm__owner=user).count():
        return True
    return False