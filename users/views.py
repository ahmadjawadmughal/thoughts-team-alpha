from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from users.models import User, UserProfile
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.views.generic.edit import CreateView,UpdateView,FormView,DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages





# Create your views here----------------------------------------------------------------------------------

class Changepass(PasswordChangeView):
    template_name = 'users/change_password.html'  # Specify your template
      

    def form_valid(self, form):
        messages.success(self.request, "Changed password successfully.")
        return super().form_valid(form)

    success_url = reverse_lazy('ListProfile')



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

#-------------------------------------------------------------------------------------------------------------

# UserProfile CRUD operations

class Profile(LoginRequiredMixin, CreateView):
    model = UserProfile
    fields = "__all__"

    def get_success_url(self):
        return reverse('DetailProfile', args=[self.object.user.pk])    
    
    def form_valid(self, form):
        already_profile = UserProfile.objects.filter(user=self.request.user).first()
        if already_profile:
            return redirect('UpdateProfile', pk=already_profile.pk)   #we can display msg as already profile exists just update
            #return HttpResponseForbidden("You already have a profile.")
        else:    
            form.instance.user = self.request.user  # Assigned the user to the profile
            return super().form_valid(form)


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = "__all__"
    #success_url = "/users/UpdateProfile/"
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('DetailProfile', args=[self.object.user.pk])
    
    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)  # get the existing profile for the current user
    
    def dispatch(self, request, *args, **kwargs):        
        if not UserProfile.objects.filter(user=request.user).exists():  # Check if the user has a profile
            return redirect('Profile')  # If no profile exists, redirect to create profile
        return super().dispatch(request, *args, **kwargs)



class DeleteProfile(LoginRequiredMixin, DeleteView):
    model = UserProfile
    fields = "__all__"
    #success_url = "/users/ListProfile/"
    login_url = reverse_lazy('login')   

    def post(self, request, *args, **kwargs):
        if 'confirm' in request.POST:
            return super().delete(request, *args, **kwargs)
        else:
            return redirect ("ListProfile")  #also the deletetion cancelled
    
    def get_success_url(self):
        return reverse ('ListProfile')  #after deletion reverse to ListProfile




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




