from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Все пути, которые начинаются с api/v1/, мы перенаправляем в приложение product
    path('api/v1/', include('product.urls')),
]
