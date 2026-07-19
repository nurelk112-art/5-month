import random
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserConfirmation

class UserRegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=3)
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username

    def create(self, validated_data):
        # Создаем пользователя, но делаем его неактивным
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  
        )
        
        # Генерируем 6-значный случайный код
        code = str(random.randint(100000, 999999))
        
        # Привязываем код к клиенту один к одному
        UserConfirmation.objects.create(user=user, code=code)
        
        # В реальном проекте здесь была бы отправка на Email, но для ДЗ просто выведем в консоль
        print(f"\n[CONFIRMATION CODE FOR {user.username}]: {code}\n")
        
        return user


class UserLoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserConfirmValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6, min_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise ValidationError({'username': 'Пользователь не найден.'})

        try:
            confirmation = user.confirmation
        except UserConfirmation.DoesNotExist:
            raise ValidationError({'code': 'Код подтверждения для этого пользователя не генерировался или уже использован.'})

        if confirmation.code != data['code']:
            raise ValidationError({'code': 'Неверный код подтверждения.'})

        return data