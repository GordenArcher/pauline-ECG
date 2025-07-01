from django.db import models
from django.utils import timezone

class Company(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    date_added = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name_plural = "Companies"


class Invoice(models.Model):    
    METER_TYPES = (
        ('one_phase', '1 PH'),
        ('three_phase', '3 PH'),
    )
    INVOICE_TYPES = (
        ('meter_suply', 'Meter Supply'),
        ('enclosure_supply', 'Enclosure Supply'),
        ('installment', 'Installment'),
    )
    CURRENCY_TYPE = (
        ('cedis', 'Cedis'),
        ('dollars', 'Dollars')
    )
    TAXED = (
        ('taxed', 'Taxed'),
        ('not_taxed', 'Not Taxed')
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    invoice_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    meter_type = models.CharField(max_length=15, choices=METER_TYPES, default='one_phase', blank=True, null=True)
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPES, default='meter_suply', blank=True, null=True)
    currency = models.CharField(max_length=10, choices=CURRENCY_TYPE, default='cedis', blank=True, null=True)
    is_taxed = models.CharField(max_length=10, choices=TAXED, default='not_taxed', blank=True, null=True)
    rent_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    issue_date = models.DateField(default=timezone.now, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.invoice_number}"
    
    class Meta:
        ordering = ['-issue_date']

class Payments(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payments')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    bank = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Payment of {self.amount} for Invoice #{self.invoice.invoice_number}"
    
    class Meta:
        ordering = ['-payment_date']


class Config(models.Model):

    THEME = (
        ('dark', 'Dark'),
        ('light', 'Light')
    )
    tax_amount = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    dollar_rate = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    theme = models.CharField(max_length=10, choices=THEME, default='dark', blank=True, null=True)

    def __str__(self):
        return f"{self.tax_amount}"