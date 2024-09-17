from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(
    [
        BillingProfile,
        InvoiceItem,
        Invoice,
        BillingProfileChild,
        RatePlan,
        Subscription,
        Payment,
    ]
)
