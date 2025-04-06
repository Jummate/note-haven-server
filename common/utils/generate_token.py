from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from datetime import timedelta, timezone as dt_timezone
from django.utils import timezone

from users.models import CustomUser



def generate_reset_token(user):
    token = AccessToken.for_user(user)  # Generate an access token
    token['email'] = user.email
    token.set_exp(from_time=timezone.now(), lifetime=timedelta(minutes=15))  # Set expiry to 15 minutes
    return str(token)  # Return the token as a string

def verify_reset_token(token):
    try:
        decoded_token = AccessToken(token)  # Decode the token
        email = decoded_token.get("email")  # Extract user email
        user = CustomUser.objects.get(email=email)
        token_issued_at = timezone.datetime.fromtimestamp(decoded_token['iat'], tz=dt_timezone.utc)

        if user.last_password_reset and token_issued_at < user.last_password_reset:
            return None  # Token was issued before last reset, so it's invalid
        return email  # Return user email if valid
    except TokenError as e:
        print("Token error:", str(e))
        return None
    except Exception as e:
        print("Other error:", str(e))
        return None