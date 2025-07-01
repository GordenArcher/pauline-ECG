from .models import Invoice, Payments, Company, Config
from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'



class InvoiceSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Invoice
        fields = '__all__'



class PaymentSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer()
    class Meta:
        model = Payments
        fields = '__all__'



class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ('tax_amount', 'dollar_rate', 'theme')