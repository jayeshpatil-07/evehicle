from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
     path('admin/', admin.site.urls),  
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('booking/', views.booking, name='booking'),
    path('slot/<int:station_id>/', views.slot, name='slot'),
    path("payment/<int:booking_id>/", views.payment, name="payment"),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
