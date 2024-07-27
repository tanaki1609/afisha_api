from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.register_api_view),
    path('authorization/', views.AuthAPIView.as_view())
]
