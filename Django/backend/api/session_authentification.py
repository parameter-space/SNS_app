from rest_framework.authentication import SessionAuthentication

"""csrf 없이 session 인증할 수 있게 만들어 준다. api 테스트를 위해 사용"""
class NoCsrfSessionAuthentification(SessionAuthentication):
    def enforce_csrf(self, request):
        return 