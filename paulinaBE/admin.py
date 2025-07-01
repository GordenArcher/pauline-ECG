from django.contrib import admin
from .models import Invoice, Payments, Company, Config

# Register your models here.

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('company', 'invoice_number', 'invoice_amount', 'meter_type', 'invoice_type', 'is_taxed', 'rent_amount', 'total_amount', 'description', 'created_at')
    search_fields = ('company', 'invoice_number', 'invoice_amount', 'meter_type', 'invoice_type', 'is_taxed', 'rent_amount', 'total_amount', 'description', 'created_at')
    list_filter = ('company', 'invoice_number', 'invoice_amount', 'meter_type', 'invoice_type', 'is_taxed', 'rent_amount', 'total_amount', 'description', 'created_at')

    def __str__(self):
        return f"#{self.invoice_number} by {self.company.company_name}"


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name','date_added')
    search_fields = ('company_name','date_added')
    list_filter = ('company_name','date_added')

    def __str__(self):
        return f"{self.company_name}"
    


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('company', 'invoice', 'payment_date', 'reference', 'bank', 'amount', 'notes')
    search_fields = ('company', 'invoice', 'payment_date', 'reference', 'bank', 'amount', 'notes')
    list_filter = ('company', 'invoice', 'payment_date', 'reference', 'bank', 'amount', 'notes')

    def __str__(self):
        return f"An amount of {self.amount} has been paid by {self.company.company_name}"
    


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('tax_amount', 'dollar_rate', 'password', 'theme')
    search_fields = ('tax_amount', 'dollar_rate', 'password', 'theme')
    list_filter = ('tax_amount', 'dollar_rate', 'password', 'theme')



admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Payments, PaymentAdmin)
admin.site.register(Config, ConfigAdmin)