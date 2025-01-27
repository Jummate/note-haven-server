import random
import uuid

def get_otp_code():
    return str(random.randint(100000, 999999))  # 6-digit numeric code
def generate_id():
    return str(uuid.uuid4())
