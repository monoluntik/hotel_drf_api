from account.models import MyUser
from rest_framework import serializers
from chat.models import Message
# 
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """For Serializing User"""
    password = serializers.CharField(write_only=True)
    class Meta:
        model = MyUser
        fields = ['email', 'password']
# 
# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    sender = serializers.SlugRelatedField(many=False, slug_field='email', queryset=MyUser.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='email', queryset=MyUser.objects.all())
    class Meta:
        model = Message
        fields = '__all__'

