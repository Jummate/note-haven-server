from django.urls import path
from . import views

urlpatterns = [
    # path('', views.users),
    path('signup/', views.create_new_user, name="signup"),
    path('login/', views.login, name="login"),
    # path('resend-otp/', views.resend_otp),
    # path('login/', views.resend_otp),
]