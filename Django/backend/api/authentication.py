from rest_framework.permissions import BasePermission
from account.models import CustomUser



class IsAuthenticatedCustom(BasePermission): 
    
    """허가를 넘겨주는 메서드"""
    def has_permission(self, request, view):
        from account.utils import decodeJWT 

        user = decodeJWT(request.META.get("HTTP_AUTHORIZATION", None), method= "Auth")

        #비정상일 때
        if user == "expired" or user == "decode_error" or user is None:
            return False
        
        request.user = user
        if request.user.is_authenticated and request.user:
            return True
        return False
