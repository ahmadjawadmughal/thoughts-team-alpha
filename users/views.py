from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from users.models import User, UserProfile
from django.views.generic.edit import CreateView,UpdateView,FormView,DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



 

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
    success_url = "/users/UpdateProfile/"
        
    def get_success_url(self):
        return reverse('DetailProfile', args=[self.object.user.pk])
       
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
    #template_name = '/users/user_profile_detail.html/'
    #success_url = "/users/Success/"            

class Success(TemplateView):
    template_name = "users/success.html/"

