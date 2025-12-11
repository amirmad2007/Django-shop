from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login , logout
from accounts.models import MyUser as User , OTP
from django.urls import reverse , reverse_lazy
from .forms import LoginForm , SignupForm , OtpForm
import ghasedak_sms
import uuid
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from random import randint  
SMS = ghasedak_sms.Ghasedak(
    api_key='c7da7ddf8908b586cb3cf2ab0f6b32fa95ccee04438d8a1bc2871434ff6f9754BWyfZ6bWE4sZk89M'
)
def user_login(request):

    if request.user.is_authenticated:

        return redirect("home")
    
    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
             username = form.cleaned_data.get('username')
             password = form.cleaned_data.get("password")
             user = authenticate(request, username=username, password=password)
     
             if user is not None:

                    login(request, user)
                    return redirect("home") 
            
             else:
               
                form.add_error(None, "username or password is incorrect")
              
    return render(request, 'accounts/templates/index.html', context= {'form' : form}) 


from django.utils.http import urlencode

def signup(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code = randint(1000, 9999)
            print(code)
            otp_command = ghasedak_sms.SendOtpInput(
                send_date=datetime.now(),   
                receptors=[
                    ghasedak_sms.SendOtpReceptorDto(
                        mobile=cd["phone_number"],
                        client_reference_id = str(uuid.uuid4())
                    )
                ],
                template_name='Ghasedak',   
                inputs=[
                    ghasedak_sms.SendOtpInput.OtpInput(param='Code', value=str(code)),
                ],
                udh=False
            )

            # SMS.send_otp_sms(otp_command)

            OTP.objects.create(
                phone_number=cd["phone_number"],
                code=str(code)
            )

            # ساخت query string
            request.session['signup_data'] = {
            "username": cd["username"],
            "email": cd["email"],
            "password": cd["password"],
            "phone_number": cd["phone_number"],
        }

            return redirect("check_otp")

    return render(request, "SignUp.html", {"form": form})



def check_otp(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = OtpForm()

    if request.method == "POST":
        form = OtpForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get("code")

            signup_data = request.session.get('signup_data')

            if not signup_data:
                return redirect('signup')
            
            username = signup_data['username']
            email = signup_data['email']
            password = signup_data['password']
            phone_number = signup_data['phone_number']

            otp  = OTP.objects.filter(phone_number=phone_number, code=str(code)).first()
            if otp:
                if otp.is_valid():
            
                
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        phone_number=phone_number
                    )

                    login(request, user)
                    otp.delete()
                    return redirect("home")
                else:
                    form.add_error(None, "Code has expired")
                    otp.delete() 
            
            else:
                form.add_error(None, "Code is invalid")

    return render(request, "OTP.html", {"form": form})


def user_log_out(request):
    logout(request)  
    return redirect('home') 

def resend_code(request):
      code = randint(1000, 9999)
      print(code)
      signup_data = request.session.get('signup_data')
      phone_number = signup_data['phone_number']
      otp_command = ghasedak_sms.SendOtpInput(
                send_date=datetime.now(),   
                receptors=[
                    ghasedak_sms.SendOtpReceptorDto(
                        mobile=signup_data["phone_number"],
                        client_reference_id = str(uuid.uuid4())
                    )
                ],
                template_name='Ghasedak',   
                inputs=[
                    ghasedak_sms.SendOtpInput.OtpInput(param='Code', value=str(code)),
                ],
                udh=False
            )

    #   SMS.send_otp_sms(otp_command)
      OTP.objects.create(phone_number = phone_number , code =str(code))
      return redirect('check_otp')









'''class LoginFOrmView(FormView):
    template_name = 'accounts/templates/index.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "username or password is incorrect")
            return self.form_invalid(form)'''

     

# token = str(uuid.uuid4())
# User.objects.get_or_create