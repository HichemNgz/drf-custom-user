from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializerWithToken, UserSerializer

from django.contrib.auth.models import User
from .models import *

from django.contrib.auth.hashers import make_password



@api_view(['GET'])
def home(request):
    return Response('Hello')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


#register user
@api_view(['POST'])
def registerUser(request):
    data = request.data

    user = User.objects.create(
        username = data['username'],
        email = data['email'],
        password = make_password(data['password'])
        #other fields = ...
    )
    
    user_id = user.save()

    Profile.objects.create(
        user_id = user.id,
        phone = data['phone']
    )

    serializer = UserSerializerWithToken(user, many = False)
    return Response(serializer.data)



#update user profile
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    profile = Profile.objects.get(user_id = user.id)

    serializer = UserSerializerWithToken(user, many = False)

    data = request.data

    user.username = data['username']
    user.email = data['email']
    profile.phone = data['phone']
    
    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()
    profile.save()
    

    return Response(serializer.data)



#get logged in user information
@api_view(['GET'])
def getUserProfile(request):
    user = request.user

    serializer = UserSerializer(user, many = False)
    return Response(serializer.data)


#get all users (for admins only)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAllUsers(request):
    user = request.user

    users = User.objects.all()

    serializer = UserSerializer(users, many = True)
    return Response(serializer.data)