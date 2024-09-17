from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include
urlpatterns = [
    
]
router = DefaultRouter()
router.register(r'billing-profile', BillingProfileViewset)
router.register(r'client-account',ChildBillingProfileViewset)
router.register(r'invoice', InvoiceViewset)
router.register(r'rate-plan', RatePlanViewset,)
urlpatterns += router.urls
