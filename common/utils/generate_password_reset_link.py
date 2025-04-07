from decouple import config
from django.conf import settings

def generate_password_reset_link(token):
    base_url = settings.FRONTEND_BASE_URL
    return f"{base_url}/reset-password/{token}"
