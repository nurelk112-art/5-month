from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.admin),
    path('', include('product.urls')),  # Маршруты твоего приложения с товарами
    path('', include('users.urls')),    # Маршруты аутентификации пользователей
]