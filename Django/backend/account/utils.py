import jwt
from datetime import datetime, timedelta
from django.conf import settings
import random
from .models import CustomUser, Jwt

def get_random_string(length):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(length))

def get_access_token(payload):
    return jwt.encode( 
        {"exp": datetime.now() + timedelta(minutes=5), **payload},
        settings.SECRET_KEY,
        algorithm="HS256",
    )

def get_refresh_token():
    return jwt.encode( 
        {"exp": datetime.now() + timedelta(minutes=30), "data": get_random_string(10)},
        settings.SECRET_KEY,
        algorithm="HS256",
    )

def decodeJWT(bearer, method):

    if not bearer:
        return None
    token = bearer[7:] 
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"]) 
    except jwt.exceptions.ExpiredSignatureError:
        return "expired"
    except jwt.exceptions.DecodeError:
        return "decode_error"
    
    

    if decoded:
        try:
            if method == "Delete_jwt":
                Jwt.objects.filter(user_id = decoded["user_id"]).delete()
                return None
            elif method == "Auth":
                jwt_search = Jwt.objects.get(user_id = decoded["user_id"]) 
                user_id = jwt_search.user.id 
                if user_id == None:
                    return None
                else:
                    user = CustomUser.objects.get(id = user_id)
                    return user
        except: None 