from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import *
from .serializers import *
from .permissions import IsAuthorPermission

class PermissionMixin:

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 
        'delete', 'destroy']:
            permissions= [IsAuthorPermission,]
        elif self.action == 'create':
            permissions = [IsAuthenticated]
        else: 
            permissions = []

        return [permission() for permission in permissions]




class ApartmentViewSet(ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer


class HotelViewSet(PermissionMixin,ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    @action(methods=['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset().filter(
            Q(name__icontains=q)|
            Q(description__icontains=q)|
            Q(country__icontains=q)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)    


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


