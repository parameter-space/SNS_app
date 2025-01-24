from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, UserSerializer, SignupSerializer
from .models import CustomUser, Jwt
from .utils import get_access_token, get_refresh_token
from api.authentication import IsAuthenticatedCustom
from django.contrib.auth.hashers import check_password

class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data.get("username"),
            password=serializer.validated_data.get("password"),
        )
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={"message": "입력하신 정보가 올바르지 않습니다."})
        
        # jwt 토큰 삭제
        Jwt.objects.filter(user=user).delete()

        # jwt 토큰 발급
        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token() # 암호화 된 토큰

        Jwt.objects.create( 
            user=user, 
            access=access,
            refresh=refresh
        )

        # 세션 로그인
        login(request, user) 

        
        response = Response(status=status.HTTP_200_OK) 
        data = {
            "access": access, 
            "message": "Login successful",
        }
        response.data = data
        response.set_cookie(key="access", value=access)
        response.set_cookie(key="refresh", value=refresh, httponly=True) 

        return response 
    



class LogoutAPIView(APIView):

    def get(self, request):

        # jwt 토큰 삭제
        from .utils import decodeJWT 
        user = decodeJWT(request.META.get("HTTP_AUTHORIZATION"), method="Delete_jwt") 

        # 세션 로그아웃
        logout(request)

        # 쿠키 삭제
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.data = {"message": "Logout successful"} 

        return response
    


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticatedCustom] 
    

    def get(self, request):
        # 현재 로그인된 사용자 정보 반환
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        # 현재 로그인된 사용자 정보 수정
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'})
        return Response(serializer.errors, status=400)


class PasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticatedCustom]
    


    def post(self, request):
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        print("data input success")
        if not current_password or not new_password:
            return Response({'error': 'Both current and new passwords are required.'}, status=400)
        print("data validation success")
        if not check_password(current_password, request.user.password):
            return Response({'error': 'Current password is incorrect.'}, status=400)
        print("password check success")
        request.user.set_password(new_password)
        request.user.save()
        print("password save success")
        return Response({'message': 'Password changed successfully'}, status=200)
    

class SignupAPIView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        print("success create class")
        if serializer.is_valid(raise_exception=True):
            print("success is_valid")
            serializer.validated_data.pop('password2')
            print("success pop")
            CustomUser.objects.create_user(**serializer.validated_data)
            print("success create user")
            return Response({'message': 'Signup successful', 'user_name': serializer.validated_data['username']}, status=status.HTTP_201_CREATED)
        return Response({'message': 'failed to signup', 'error_code' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)