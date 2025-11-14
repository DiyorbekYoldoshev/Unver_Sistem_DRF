import requests
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication

TOKEN = "8268472648:AAHnpCFMp0pVh4eKcga5gqoZOBG9tdYDJR0"
CHAT_ID = "1954153232"

class TelegramRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/') and request.method in ['GET', 'POST', 'PUT', 'DELETE']:
            method = request.method

            # 🔹 JWT token orqali foydalanuvchini aniqlash
            user = None
            try:
                jwt_auth = JWTAuthentication()
                auth_result = jwt_auth.authenticate(request)
                if auth_result is not None:
                    user, _ = auth_result
            except Exception:
                pass

            # 🔹 Foydalanuvchini aniqlash
            if user and user.is_authenticated:
                username = user.username
                role = user.role
            else:
                username = "Anonim"
                role = "-"

            text = f"🔔 So‘rov kelib tushdi\nMethod: {method}\nURL: {request.path}\nUser: {username} ({role})"
            print(text)

            # 🔹 Telegramga yuborish
            try:
                requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    data={"chat_id": CHAT_ID, "text": text}
                )
            except Exception as e:
                print(f"Telegramga yuborishda xato: {e}")

        return None
