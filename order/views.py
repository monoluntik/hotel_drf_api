from django.shortcuts import render
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from order.models import Order
from order.serializers import OrderSerializer

# Create your views here.
 

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]


    @action(methods=['GET'], detail=False)
    def history(self, requset):
        owner = requset.user
        queryset = self.queryset.filter(owner=owner)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)        