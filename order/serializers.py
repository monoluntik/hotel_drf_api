from django.core.checks import messages
from django.http import request
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from account.tasks import send_order_info
from main.models import Apartment, Hotel
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    hotel = serializers.ReadOnlyField(source='hotel.name')
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        owner = request.user
        apartment = validated_data.get('apartment')
        hotel = apartment.hotel
        validated_data['owner'] = owner
        validated_data['hotel'] = hotel
        message = []
        for i in validated_data:
            val = validated_data.get(i)
            message.extend([f'{i}: {val}'])
        message = '\n'.join(message)
        send_order_info.delay(validated_data['email'], message)
        return super().create(validated_data)



