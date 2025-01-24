from django.urls import path
from .apis import SignupAPIView, LoginAPIView, LogoutAPIView, ProfileAPIView, PasswordChangeAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('password_change/', PasswordChangeAPIView.as_view(), name='reset_password'),
]
