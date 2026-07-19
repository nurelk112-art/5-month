from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import (
    UserRegisterValidateSerializer, 
    UserLoginValidateSerializer, 
    UserConfirmValidateSerializer
)

@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterValidateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            data={'message': 'Пользователь успешно зарегистрирован. Код подтверждения отправлен (проверьте консоль сервера).'},
            status=status.HTTP_201_CREATED
        )
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def confirm_api_view(request):
    serializer = UserConfirmValidateSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        user = User.objects.get(username=username)
        
        # Активируем пользователя
        user.is_active = True
        user.save()
        
        # Удаляем код, чтобы его нельзя было использовать повторно
        user.confirmation.delete()
        
        return Response(data={'message': 'Аккаунт успешно активирован!'}, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserLoginValidateSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        
        # Аутентификация встроенным методом Django
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if not user.is_active:
                return Response(
                    data={'errors': 'Ваш аккаунт не активирован. Пожалуйста, подтвердите его с помощью кода.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Если всё ок, создаем или берем существующий токен
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key}, status=status.HTTP_200_OK)
            
        return Response(data={'errors': 'Неверный логин или пароль.'}, status=status.HTTP_401_UNAUTHORIZED)
        
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)