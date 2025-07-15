from django.urls import path
from . import views

urlpatterns = [
    # URLs for the registration and verification process
    path('', views.register_view, name='register'),
    path('verification-sent/', views.verification_sent_view, name='verification_sent'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('verification-success/', views.verification_success_view, name='verification_success'),
    path('verification-failed/', views.verification_failed_view, name='verification_failed'),
]