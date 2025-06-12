# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verify/<uuid:token>/', views.verify_email, name='verify_email'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('api/get_all_rp_logs/<str:rp_name>/', views.get_all_rp_logs, name='get_all_rp_logs'),
]
