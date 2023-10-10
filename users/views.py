from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from users.models import User, UserProfile
from django.views.generic.edit import CreateView,UpdateView,FormView,DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages

"""
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
"""

# Create your views here.

class Changepass(PasswordChangeView):
    template_name = 'users/change_password.html'  # Specify your template
      

    def form_valid(self, form):
        messages.success(self.request, "Changed password successfully.")
        return super().form_valid(form)

    success_url = reverse_lazy('ListProfile')


"""
def change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':   
            form = PasswordChangeForm(user=request.user, data=request.POST)    #with old password required
            #form = SetPasswordForm(user=request.user, data=request.POST)   #we can use this as well, then no old password field to change password
            if form.is_valid():
                form.save()
                messages.success(request, "Changed password successfully.")
                #update session as well
                update_session_auth_hash(request, form.user)
                return redirect("ListProfile")
        else:
            form = PasswordChangeForm(user=request.user)
            return render (request, "users/change_password.html", {'form': form})
    else:
        return redirect("login")
"""



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
            messages.error(request, "Username is already exist!")

        if User.objects.filter(email=email):
            messages.error(request, "Email is already exist!")

        if password != password_confirmation:
            messages.error(request, "Passwords do not match.")
        else:
            #Save password securely
            user_signup = User.objects.create_user(username=username, email=email, password=password, first_name= first_name, last_name=last_name)
            user_signup.is_active = True
            user_signup.save()

            messages.success(request, "You are successfully signed up!")
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

            return render (request,"users/userprofile_list.html", {"fname": fname})
            #return redirect('DetailProfile', user.pk) 

        else:
            messages.error(request, "Wrong Credentials.")
            return redirect("login")

    return render(request, "users/login.html")



@csrf_exempt
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out!") 
    return redirect("login")



# CRUD operations

class Profile(LoginRequiredMixin, CreateView):
    model = UserProfile
    fields = "__all__"

    def get_success_url(self):
        return reverse('DetailProfile', args=[self.object.user.pk])    

    def get(self, request, *args, **kwargs):
        # Only logged-in users can access this view
        return super().get(request, *args, **kwargs)



class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = "__all__"
    #success_url = "/users/UpdateProfile/"
        
    def get_success_url(self):
        return reverse('DetailProfile', args=[self.object.user.pk])
    
    #overwrite dispatch functon to check the userprofile already exist or not
    def dispatch(self, request, *args, **kwargs):  
        if not UserProfile.objects.filter(user=request.user).exists():  #check if userprofile not exists redirect to createprofile 
            return redirect('Profile') 
        return super().dispatch(request, *args, **kwargs)

    login_url = reverse_lazy('login')


class DeleteProfile(LoginRequiredMixin, DeleteView):
    model = UserProfile
    fields = "__all__"
    success_url = "/users/userprofile_confirm_delete.html"
    login_url = reverse_lazy('login')   #if user not loggedin, first this will redirect to login page 


class ListProfile(ListView):
    model = UserProfile
    success_urls = "/users/Success/"


class DetailProfile(DetailView):
    model = UserProfile

    
    def get_success_url(self):
        return reverse('DetailProfile', args=[self.object.user.pk])
    #template_name = '/users/user_profile_detail.html/'
    #success_url = "/users/Success/"            

class Success(TemplateView):
    template_name = "users/success.html/"

