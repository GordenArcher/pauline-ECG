from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Payments, Company, Invoice, Config
from .serializer import InvoiceSerializer, CompanySerializer, PaymentSerializer, ConfigSerializer

# Create your views here.
@api_view(['POST'])
def add_company(request):
    data = request.data

    try:
        company_names = data.get("company_name")
        date_added = data.get("date_added")

        if not company_names or not date_added:
            return Response({
                "status": "error",
                "message": "Both 'company name' and 'date added' are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        name_list = [name.strip() for name in company_names.split(',') if name.strip()]

        if not name_list:
            return Response({
                "status": "error",
                "message": "No valid company names provided."
            }, status=status.HTTP_400_BAD_REQUEST)

        added = []
        duplicates = []

        for name in name_list:
            if Company.objects.filter(company_name=name).exists():
                duplicates.append(name)
            else:
                Company.objects.create(company_name=name, date_added=date_added)
                added.append(name)

        return Response({
            "status": "success",
            "type": "company",
            "message": "Processing complete",
            "added": added,
            "duplicates": duplicates
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": "error",
            "type": "server error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 



@api_view(['GET'])
def get_all_companies(request):
    try:
        companies = Company.objects.all()

        company_serializer = CompanySerializer(companies, many=True)

        return Response({
            "status":"success",
            "type":"company",
            "data": company_serializer.data,
            "message":"ok"
        }, status=status.HTTP_200_OK)

    except Exception as e:    
        return Response({
            "status":"error",
            "type":"server error",
            "message":f"{e}"
        }, status=status.HTTP_400_BAD_REQUEST)   


@api_view(['POST'])
def create_invoice(request):
    try:
        data = request.data
        company_name = data.get("company_name")
        invoice_number = data.get("invoice_number")
        invoice_amount = data.get("invoice_amount")
        meter_type = data.get("meter_type")
        invoice_type = data.get("invoice_type")
        currency = data.get("currency")
        is_taxed = data.get("is_taxed")
        rent_amount = data.get("rent_amount")
        total_amount = data.get("total_amount")
        description = data.get("description")
        created_at = data.get("created_at")

        if not all([company_name, invoice_number, invoice_amount, meter_type, invoice_type, is_taxed, total_amount, description, created_at]):
            return Response({
                "status":"error",
                "message":"some fields are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        

        if Invoice.objects.filter(invoice_number=invoice_number).exists():
            invoice = Invoice.objects.get(invoice_number=invoice_number)
            invoice_serializer = InvoiceSerializer(invoice)

            return Response({
                "status":"error",
                "type":"invoice",
                "invoice": invoice_serializer.data,
                "message":"invoice number already exists"
            }, status=status.HTTP_400_BAD_REQUEST)


        try:
            company = Company.objects.get(company_name=company_name)
        except Company.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"{company} does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)

        Invoice.objects.create(
            company=company,
            invoice_number=invoice_number, 
            invoice_amount=invoice_amount, 
            meter_type=meter_type,
            invoice_type=invoice_type,
            currency=currency,
            is_taxed=is_taxed,
            rent_amount=rent_amount,
            total_amount=total_amount,
            description=description,
            created_at=created_at
        )
        
        return Response({
            "status":"success",
            "type":"invoice",
            "message":"created"
        }, status=status.HTTP_200_OK)
        

    except Exception as e:
        return Response({
            "status":"error",
            "type":"server error",
            "message":f"{e}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
def create_invoice_upload(request):
    pass    



@api_view(['GET'])
def get_all_invoices(request):
    try:
        invoices = Invoice.objects.all()

        invoice_serializer = InvoiceSerializer(invoices, many=True)

        return Response({
            "status":"success",
            "type":"invoice",
            "data": invoice_serializer.data,
            "message":"ok"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status":"error",
            "type":"server error",
            "message":f"{e}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    

@api_view(['POST'])
def add_payments(request):
    data = request.data
    try:
        company_name = data.get("company_name")
        invoice_number = data.get("invoice_number")
        date = data.get("date")
        reference = data.get("reference")
        bank = data.get("bank")
        amount = data.get("amount")
        notes = data.get("notes")

        if not all([company_name, invoice_number, date, reference, bank, amount]):
            return Response({
                "status":"error",
                "message":"All fields are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            invoice = Invoice.objects.get(invoice_number=invoice_number)
        except Invoice.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Invoice {invoice_number} does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if Payments.objects.filter(invoice=invoice).exists():
            invoice = Invoice.objects.get(invoice=invoice)
            
            invoice_serializer = InvoiceSerializer(invoice)

            return Response({
                "status":"error",
                "type":"payment",
                "data": invoice_serializer.data,
                "message":"Invoice already exists with another payment"
            }, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            company = Company.objects.get(company_name=company_name)
        except Company.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"{company_name} does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        

        Payments.objects.create(company=company, invoice=invoice, payment_date=date, reference=reference, bank=bank, amount=amount, notes=notes or None)
        return Response({
            "status":"success",
            "type":"payment",
            "message":"ok"
        }, status=status.HTTP_200_OK)


    except Exception as e:
        return Response({
            "status":"error",
            "type":"server error",
            "message":f"{e}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_all_payments(request):
    try:
        payments = Payments.objects.all()

        payment_serializer = PaymentSerializer(payments, many=True)

        return Response({
            "status":"success",
            "type":"payment",
            "data": payment_serializer.data,
            "message":"ok"
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status":"error",
            "type":"server error",
            "message":f"{e}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    


@api_view(['GET'])
def get_config(request):
    try:
        config = Config.objects.first()
        config_serializer = ConfigSerializer(config)

        return Response({
            "status":"success",
            "type":"config",
            "data": config_serializer.data,
            "message":"ok"
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "status":"error",
            "type":"server error",
            "message":f"{e}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)          
    


@api_view(['POST'])
def check_password(request):
    password = request.data.get("password")

    try:

        if not password:
            return Response({
                "status":"error",
                "type":"password error",
                "message":"Password is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        config = Config.objects.first()
        actual_password = config.password

        if actual_password == password:
            print(f"Provided: {password}, Actual: {Config.password}")
            return Response({
                "status":"success",
                "allow":True,
                "type":"password success",
                "message":"ok"
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                "status":"error",
                "type":"password error",
                "message":"Password incorrect"
            }, status=status.HTTP_400_BAD_REQUEST)       


    except Exception as e:
        return Response({
            "status":"error",
            "type":"server error",
            "message":f"{e}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                  
    


@api_view(['POST'])
def change_config(request):
    try:
        data = request.data
        tax_amount = data.get("tax_amount")
        dollar_rate = data.get("dollar_rate")

        config, created = Config.objects.get_or_create(
            defaults={
                "tax_amount": tax_amount,
                "dollar_rate": dollar_rate
            }
        )

        if not created:
            config.tax_amount = tax_amount
            config.dollar_rate = dollar_rate
            config.save()

        config_serializer = ConfigSerializer(config)

        return Response({
            "status": "success",
            "type": "config",
            "data": config_serializer.data,
            "message": "updated"
        }, status=status.HTTP_200_OK)

    except Exception as e:   
        import traceback
        traceback.print_exc()
        return Response({
            "status": "error",
            "type": "server error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def change_config_theme(request):
    try:
        theme = request.data.get("theme")

        config = Config.objects.first()

        config.theme = theme
        config.save()

        config_serializer = ConfigSerializer(config)

        return Response({
            "status": "success",
            "type": "config",
            "data": config_serializer.data,
            "message": "updated"
        }, status=status.HTTP_200_OK)

    except Exception as e:   
        import traceback
        traceback.print_exc()
        return Response({
            "status": "error",
            "type": "server error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def get_company_invoice(request):
    data = request.data

    try:
        company_name = data.get('company_name')

        if not company_name:
            return Response({
                "status":"error",
                "message":"Company name was not provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            company =  Company.objects.get(company_name=company_name)
        except Company.DoesNotExist:
            return Response({
                "status":"error",
                "message":"Comapany does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
        
        company_invoices = Invoice.objects.filter(company=company)

        invoice_serializer = InvoiceSerializer(company_invoices, many=True)

        return Response({
            "status":"success",
            "message":"company invoice retrieved",
            "invoice": invoice_serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": "error",
            "type": "server error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        