from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

router = DefaultRouter()
router.register("vms",VirtualMachineViewSet,basename="virtual-machine")
urlpatterns = [
    
]

urlpatterns += router.urls