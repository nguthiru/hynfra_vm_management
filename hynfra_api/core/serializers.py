from rest_framework import serializers
from .models import VirtualMachine,VirtualMachineBackup
from django.contrib.auth import get_user_model
class VirtualMachineSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), required=False)

    class Meta:
        model = VirtualMachine
        fields = "__all__"
        read_only_fields = ['owner', 'created_at']

    def create(self, validated_data):
        return VirtualMachine.objects.create( **validated_data)
class VirtualMachineBackupSerializer(serializers.ModelSerializer):

    class Meta:
        model = VirtualMachineBackup
        fields = "__all__"
