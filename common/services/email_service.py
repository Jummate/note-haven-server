from django.core.mail import send_mail

def forward_mail(subject:str, from_email:str, recipient_list:list, html_message:str):
    if isinstance(recipient_list, str):
        recipient_list = [recipient_list]  # Wrap it in a list if it's a string
    return send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, html_message=html_message, message="")