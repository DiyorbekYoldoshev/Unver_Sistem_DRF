import requests
from django.utils.deprecation import MiddlewareMixin

TOKEN = "8268472648:AAHnpCFMp0pVh4eKcga5gqoZOBG9tdYDJR0"
CHAT_ID = "1954153232"

class TelegramRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Faqat API uchun
        if request.path.startswith('/api/') and request.method in ['GET', 'POST', 'PUT', 'DELETE']:
            method = request.method
            user = request.user if request.user.is_authenticated else 'Anonim'
            text = f"🔔 So‘rov kelib tushdi\nMethod: {method}\nURL: {request.path}\nUser: {user}"

            # Xabarni yuborish
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": text}
            )

        return None

