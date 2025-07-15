# super/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.superuser_login_view, name='super_login'),
    path('dashboard/', views.superuser_dashboard_view, name='super_dashboard'),
    path('profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('profile/<int:user_id>/add_child/', views.add_child_view, name='add_child'),
    path('child/<int:child_id>/update/', views.update_child_view, name='update_child'),
    path('profile/<int:user_id>/delete/', views.delete_user_view, name='delete_user'),
]