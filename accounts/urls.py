from django.urls import path
from .views import *

urlpatterns = [
    path('login/',user_login , name="login") ,
    path("signup/", signup , name="signup"),
    path("logout",user_log_out , name= "logout"),
    path("check-otp",check_otp , name= "check_otp"),
    path("resend-code" , resend_code , name= "resend_code")
]