from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RatePlan(models.Model):
    PLAN_CHOICES = [
        ("PLATINUM", "Platinum"),
        ("GOLD", "Gold"),
        ("SILVER", "Silver"),
        ("BRONZE", "Bronze"),
    ]

    name = models.CharField(max_length=10, choices=PLAN_CHOICES, unique=True)
    max_vms = models.PositiveIntegerField()
    max_backups = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# Create your models here.
class BillingProfile(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Billing Profile for {self.user.username}"

    def add_funds(self, amount: float):
        self.balance += amount
        self.save()

    def charge(self, amount: float):
        # FIXME: Use balance if credited for now just go to negative values
        # if self.balance < amount:
        #     raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.save()

class BillingProfileChild(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    active = models.BooleanField(
        default=True,
    )

    class Meta:
        unique_together = ("user", "billing_profile")
        verbose_name = "Child Billing Account"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.billing_profile.user.username}"




@receiver(models.signals.post_save, sender=User)
def create_billing_profile(sender, instance, created, **kwargs):
    if created:
        BillingProfile.objects.create(user=instance)


class Subscription(models.Model):
    billing_profile = models.OneToOneField(BillingProfile, on_delete=models.CASCADE)
    rate_plan = models.ForeignKey(RatePlan, on_delete=models.CASCADE,null=True)
    start_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.billing_profile.user.username} - {self.rate_plan.name}"
    
@receiver(models.signals.post_save, sender=BillingProfile)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        rate_plan = RatePlan.objects.first()
        Subscription.objects.create(billing_profile=instance,rate_plan=rate_plan)


class InvoiceItem(TimestampMixin):
    billing_profile = models.ForeignKey(
        BillingProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(
        max_length=255,
    )
    content_object = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)

    # def __str__(self):
    #     return f"Pending of {self.amount} for {self.billing_profile.user.username}"


class Invoice(TimestampMixin):
    billing_profile = models.ForeignKey(
        BillingProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    is_paid = models.BooleanField(default=False)
    items = models.ManyToManyField(InvoiceItem)
    due_date = models.DateField(null=True, blank=True)
    

    # def __str__(self):
    #     return f"Invoice of {self.total} for {self.billing_profile.user.username}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def pay(self):
        if self.is_paid:
            raise ValueError("Invoice is already paid.")
        self.is_paid = True
        self.save()
        self.billing_profile.charge(self.total)

    @property
    def total(self):
        return sum([item.amount for item in self.items.all()])


class Payment(TimestampMixin):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(
        max_length=255,
    )
    reference = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return (
            f"Payment of {self.amount} for {self.invoice.billing_profile.user.username}"
        )

    def save(self, *args, **kwargs):
        self.invoice.pay()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.invoice.is_paid = False
        self.invoice.save()
        super().delete(*args, **kwargs)
