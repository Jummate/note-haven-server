from django.core.mail import send_mail

def forward_mail(subject:str, from_email:str, recipient_list:list, html_message:str):
    return send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, html_message=html_message, message="")