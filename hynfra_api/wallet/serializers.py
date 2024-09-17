from rest_framework import serializers
from .models import *
from users.serializers import UserSerializer

class BillingProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingProfile
        fields = '__all__'

class BillingProfileChildSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = BillingProfileChild
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    amount = serializers.SerializerMethodField('get_total')
    class Meta:
        model = Invoice
        fields = '__all__'

    def get_total(self, obj):
        return obj.total

    

class RatePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatePlan
        fields = '__all__'

class SubscriptionSerialiser(serializers.ModelSerializer):
    rate_plan = RatePlanSerializer()
    class Meta:
        model = Subscription
        fields = '__all__'



class InvoicePaymentSerializer(serializers.Serializer):

    invoices = serializers.ListField(
        child=serializers.IntegerField()
    )
    
    def validate(self, data):
        if not data.get("invoices"):
            raise serializers.ValidationError("Invoices list is empty.")
        
        #check if invoices exists
        for invoice_id in data.get("invoices"):
            if not Invoice.objects.filter(id=invoice_id).exists():
                raise serializers.ValidationError(f"Invoice with id {invoice_id} does not exist.")
        return data
    
    
