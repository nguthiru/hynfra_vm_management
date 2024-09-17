from .models import *


def get_billing_profile(user):
    billing_profile_child = BillingProfileChild.objects.filter(user=user)
    if billing_profile_child.exists():
        billing_profile = billing_profile_child.first().billing_profile
    else:
        billing_profile,_ = BillingProfile.objects.get_or_create(user=user)
    return billing_profile

def invoice_item(
    user,
    amount,
    name,
    content_object,
):
    billing_profile = get_billing_profile(
        user
    )
    invoice_item = InvoiceItem.objects.create(
        billing_profile=billing_profile,
        amount=amount,
        name=name,
        content_object=content_object,
    )
    invoice = Invoice.objects.filter(
        billing_profile=billing_profile, is_paid=False, due_date__gte=timezone.now()
    )
    if invoice.exists():
        invoice = invoice.first()
        invoice.items.add(invoice_item)
        invoice.save()
    else:
        invoice = Invoice.objects.create(
            billing_profile=billing_profile,
        )
        invoice.items.add(invoice_item)
        invoice.save()
    return invoice_item
