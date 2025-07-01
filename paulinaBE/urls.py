from django.urls import path
from . import views

urlpatterns = [
    path("add_company/", views.add_company),
    path("companies/", views.get_all_companies),
    path("add_invoice/", views.create_invoice),
    path("upload_invoice/", views.create_invoice_upload),
    path("invoices/", views.get_all_invoices),
    path("add_payment/", views.add_payments),
    path("payments/", views.get_all_payments),
    path("config/", views.get_config),
    path("update_config/", views.change_config),
    path("update_theme/", views.change_config_theme),
    path("check_password/", views.check_password),
    path("company_invoice/", views.get_company_invoice),
]