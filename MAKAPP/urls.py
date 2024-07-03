from django.urls import path
from .import views
from .views import login

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('payslips/<int:pk>', views.payslip, name='payslip'),
    path('generate_payslip/', views.generate_payslip, name='generate_payslip'),
    path('send_payslip/', views.send_payslip, name='send_payslip'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout, name='logout'),
]