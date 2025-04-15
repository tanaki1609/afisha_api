from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterValidateSerializer, AuthValidateSerializer
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def authorization_api_view(request):
    serializer = AuthValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)  # username=admin1, password=123

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User credentials are wrong!'})


@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(username=username,
                                    password=password,
                                    is_active=False)
    # create code (6-symbol)
    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})
