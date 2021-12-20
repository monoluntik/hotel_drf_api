from django.contrib.auth import authenticate

from rest_framework import serializers

from account.models import MyUser
from account.tasks import send_activation_code

class ChangePasswordSerializer(serializers.Serializer):
    model = MyUser
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match!')
        return validated_data

    def create(self, validated_data):
        """ this func is calling when self.save() is called"""
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_code.delay(email=user.email, activation_code=str(user.activation_code))
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                message = 'unable to log in with provided credintials'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Must include "email" amd "password".'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=500, required=True)
    activation_code = serializers.CharField(max_length=6, min_length=6, required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm', 'activation_code')

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate_activation_code(self, code):
        if not MyUser.objects.filter(activation_code=code, is_active=False).exists():
            raise serializers.ValidationError('Неверный код активации')
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def save(self, **kwargs):
        print(self.validated_data)
        data = self.validated_data
        email = data.get('email')
        print(email)
        code = data.get('activation_code')
        password = data.get('password')
        try:
            user = MyUser.objects.filter(email=email,
                                      activation_code=code,
                                      is_active=False)[0]
            print(user)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')
        user.is_active = True
        print(user.is_active)
        user.activation_code = ''
        print(user.activation_code)
        user.set_password(password)
        user.save()