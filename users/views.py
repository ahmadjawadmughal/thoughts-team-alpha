

from django.shortcuts import render, redirect
from users.models import User, UserProfile
from django.views.generic.edit import CreateView,UpdateView,FormView,DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from users.forms import *
# import email
from django.core.mail import EmailMessage,send_mail 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_str,force_bytes
from Thoughts import settings
from . tokens import generate_token

@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["pswd"]
        password_confirmation = request.POST["pswd_confirmation"]

        if User.objects.filter(username=username):
            messages.error(request,"Username is already exist!")

        if User.objects.filter(email=email):
            messages.error(request,"Email is already exist!")

        user_signup = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user_signup.is_active = True
        user_signup.save()

        messages.success(request, "You are successfully signed up! We have also send you a confirmation email in order to activate your account.")

        # Email

        subject = "Welcome to Thoughts-Login!!"
        message = "Hello"+ user_signup.first_name +"! \n"+"Welcome to Thoughts! \n Thank you for visiting our website \n Please confirm your email in order to activate your account. \n\n Thank you \n\n  Thoughts"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user_signup.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        # Email address confirmation email

        current_site = get_current_site(request)
        email_subject = "Confirm your email @ Thoughts - Login!"
        message2 = render_to_string("email_confirmation.html",{
            "name" : user_signup.first_name,
            "domain" : current_site.domain,
            "uid" : urlsafe_base64_encode(force_bytes(user_signup.pk)),
            "token" : generate_token.make_token(user_signup)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user_signup.email],
        )
        email.fail_silently = True
        email.send()

        return redirect("login")

    return render(request, "users/user_form.html")

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["pswd"]
        user = authenticate(request, username=username, password=password)
        
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "post_thoughts/thought.html", {"fname": fname})
        else:
            messages.error(request, "Wrong Credentials.")
            return redirect("login")

    return render(request, "users/login.html")

@csrf_exempt
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out!")

    return redirect("HomeView")

@csrf_exempt
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user_signup = User.objects.get(pk=uid)

    except (TypeError,ValueError,OverFlowError,User.DoesNotExist):
        user_signup = None

    if user_signup is not None and generate_token.check_token(user_signup,token):
        user_signup.is_active = True 
        user_signup.save()
        login(request,user_signup)

        return redirect("home")

    else:
        return render(request,"activation_failed.html")        
