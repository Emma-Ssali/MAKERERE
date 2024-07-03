from smtplib import SMTPException
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .utils import send_email_with_attachment
import os
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from .forms import GeneratePayslipForm, EmailPayslipForm
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from MAKPAY.settings import EMAIL_HOST_USER
from django.conf import settings


# Create your views here.
def home(request):
    employee = Employee.objects.all()
    context = {
        'employee': employee,
    }
    return render(request, 'home.html', context)


def payslip(request, pk):
    employee = Employee.objects.get(id=pk)
    template_path = 'employee_payslip.html'
    context = {
        'employee': employee,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def generate_payslip(request):
    if request.method == 'POST':
        form = GeneratePayslipForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data['employee_id']
            employee = get_object_or_404(Employee, pk=employee_id)

            #Generate payslip content
            payslip_content = render_to_string('employee_payslip.html', {'employee': employee})

            #Display form to send email
            email_form = EmailPayslipForm(initial={'recipient_email': employee.email, 'payslip_content': payslip_content})
            return render(request, 'send_payslip.html', {'form': email_form})
    else:
        form = GeneratePayslipForm()

    return render(request, 'generate_payslip.html', {'form': form})


def send_payslip(request):
    if request.method == 'POST':
        form = EmailPayslipForm(request.POST, request.FILES)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            payslip_document = request.FILES.get('payslip_document')

            try:
                email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [recipient_email])
                if payslip_document:
                    email.attach(payslip_document.name, payslip_document.read(), payslip_document.content_type)

                email.send()
                return render(request, 'success.html', {'recipient_email': recipient_email})

            except SMTPException as e:
                return render(request, 'error.html', {'error_message': f"SMTP error occured: {e}"})

            except Exception as e:
                return render(request, 'error.html', {'error_message': f"Failed to send email: {e}"})
    else:
        form = EmailPayslipForm()

    return render(request, 'send_payslip.html', {'form': form})


def send_email(recipient_email, payslip_content):
    subject = 'New Payslip received'
    message = f'Dear Employee,\n\n{payslip_content}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print(f"Email sent to {recipient_email}")
    except SMTPException as e:
        print(f"SMTP error occured while sending email to {recipient_email}: {str(e)}")
    except Exception as e:
        #Handle exception
        print(f"Failed to send email to {recipient_email}: {(str(e))}")


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            return redirect('home')
        else:
            messages.error(request, 'You cannot access this site')

    return render(request, 'login.html')


def logout(request):
    return render(request, 'login.html')


def about(request):
    return render(request, 'about.html')