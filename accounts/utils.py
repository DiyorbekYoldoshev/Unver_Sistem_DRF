import requests
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

TOKEN = "8268472648:AAHnpCFMp0pVh4eKcga5gqoZOBG9tdYDJR0"
CHAT_ID = "1954153232"

@receiver(post_save, sender=User)
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        text = f"🧑‍💻 Yangi foydalanuvchi yaratildi:\nID: {instance.id}\nEmail: {instance.email}"
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text}
        )
