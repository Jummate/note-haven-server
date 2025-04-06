from django.urls import path
from . import views

urlpatterns = [
    # path('', views.users),
    path('signup/', views.create_new_user, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('forgot-password/', views.forgot_password, name="forgot-password"),
    path('reset-password/', views.reset_password, name="reset-password"),

    # path('login/', views.resend_otp),
]