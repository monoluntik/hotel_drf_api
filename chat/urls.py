from django.urls import path
from . import views
urlpatterns = [
    # URL form : "/api/messages/1/2"
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list),  # For GET request.
    # URL form : "/api/messages/"
    path('api/messages/', views.message_list),   # For POST
    # URL form "/api/users/1"
    path('api/users/<int:pk>/', views.user_list),      # GET request for user with id
    path('api/users/', views.user_list),    # POST for new user and GET for all users list
]
