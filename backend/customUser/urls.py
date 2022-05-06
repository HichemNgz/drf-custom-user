from django.urls import path
from . import views


urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register/', views.registerUser, name='user-register'),
    path('users/update/', views.updateUserProfile, name='user-update'),
    path('users/profile/', views.getUserProfile, name='user-profile'),
    path('users/', views.getAllUsers, name='get-all-users'),
    path('', views.home, name='home')
]