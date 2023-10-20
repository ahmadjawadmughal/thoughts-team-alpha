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


# Create your views here-------------------------------------------------------------------------------

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
            # create_user convert password into hashes, ensure the securely store in the DB
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
        
        # if user already exist , then login
        if user is not None:
            login(request, user)
            fname = user.first_name

            return render (request,"post_thoughts/home.html", {"fname": fname})

        else:
            messages.error(request, "Wrong Credentials.")
            return redirect("login")

    return render(request, "users/login.html")




#update password view
class Changepass(PasswordChangeView):
    template_name = 'users/change_password.html'      

    def form_valid(self, form):
        messages.success(self.request, "Changed password successfully.")
        return super().form_valid(form)

    success_url = reverse_lazy('ListProfile')



@csrf_exempt
def user_logout(request):
    logout(request)
    messages.success(request, "You are logged out!") 
    return redirect("login")



# User Profile CRUD operations---------------------------------------------------------------------------------

#only loggedin user can access this create profile


from django.shortcuts import redirect

class Profile(LoginRequiredMixin, CreateView):
    model = UserProfile
    fields = ["bio", "city", "date_of_birth", "profile_picture"]
    login_url = "/users/login/"

    def get_success_url(self):
        return reverse('ListProfile')  # Redirect to the list of profiles after creation

    # Save the form with additional functionalities
    def form_valid(self, form):
        try:
            # Try to get the user's profile
            profile = UserProfile.objects.get(user=self.request.user)
            # Profile exists, redirect to the list of profiles
            return redirect('ListProfile')
        except UserProfile.DoesNotExist:
            # Profile doesn't exist, create a new one
            form.instance.user = self.request.user
            form.save()
        return redirect('ListProfile')


"""
class Profile(LoginRequiredMixin, CreateView):
    model = UserProfile
    fields = ["bio", "city", "date_of_birth", "profile_picture"]
    login_url = "/users/login/"

    def get_success_url(self):
        return reverse('DetailProfile', args=[self.object.pk])
    
    
    #save the form with additional functionalities
    def form_valid(self, form):
        
        try:
            already_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
            if already_profile:
                return redirect('ListProfile')   #we can display msg as already profile exists just update
              
            else:    
                form.instance.user = self.request.user  # Assigned the user to the profile
                return super().form_valid(form)
            
        except:
            form.instance.user = self.request.user  # Assigned the user to the profile
            return super().form_valid(form)
 """           
   


#user can update profile with specific detail changes
class UpdateProfile(LoginRequiredMixin,UpdateView):
    model = UserProfile
    fields = ['bio','city','profile_picture','date_of_birth']
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('DetailProfile', args=[self.object.pk])
  



class DeleteProfile(DeleteView):
    model = UserProfile  
   
    def get_success_url(self):
        return reverse ('ListProfile')  #after deletion reverse to ListProfile   



class ListProfile(LoginRequiredMixin,ListView):
    model = UserProfile
    login_url = "/users/login/"
    success_urls = "/users/Success/"



class DetailProfile(DetailView):
    model = UserProfile
    template_name = "users/userprofile_detail.html"
   


class Success(TemplateView):
    template_name = "users/success.html/"




    
