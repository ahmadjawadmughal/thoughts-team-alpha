from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,UpdateView,FormView,DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from post_thoughts.models import *



# Create your views here.
# home page
class Home(TemplateView):
    template_name = "post_thoughts/home.html"

# about page

class About(TemplateView):
    template_name = "post_thoughts/about.html"

class ChangePass(LoginRequiredMixin, UpdateView):
    model = Thought
    fields = ["password"]

    def get_success_url(self):
        #redirect to detailthought view with a specific primary key
        #return reverse('DetailThoughts', args=[self.object.user.pk])
        return reverse('ListThoughts')
    
    login_url = reverse_lazy('login')   #if user not loggedin, first this will redirect user for login page
    

class CreateThoughts(LoginRequiredMixin, CreateView):
    model = Thought
    fields = "__all__"

    def get_success_url(self):
        #redirect to detailthought view with a specific primary key
        #return reverse('DetailThoughts', args=[self.object.user.pk])
        return reverse('ListThoughts')
    
    login_url = reverse_lazy('login')   #if user not loggedin, first this will redirect user for login page



class UpdateThought(LoginRequiredMixin, UpdateView):
    model = Thought
    fields = "__all__"

    def get_success_url(self):
        return reverse('DetailThoughts', args=[self.object.user.pk])  
    
    login_url = reverse_lazy('login')



class DeleteThoughts(LoginRequiredMixin, DeleteView):
    model = Thought
    fields = "__all__"
    
    def get_success_url(self):
        return reverse('DetailThoughts', args=[self.object.user.pk])
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
    # Retrieve the object to be deleted using the 'pk' from the URL
        return self.model.objects.get(pk=self.kwargs['pk'])


#getting thoughts of loggedin user
class My_thoughts(LoginRequiredMixin, ListView):
    model = Thought
    template_name = "post_thoughts/thought_list.html"
    login_url = reverse_lazy('login')

    # to associate thoughts with users.
    def get_queryset(self):  #a queryset of all thoughts will come not single object
        return self.model.objects.filter(user=self.request.user)



#all thoughts of users
class ListThoughts(ListView):
    model = Thought
    template_name = "post_thoughts/thought_list.html"
    success_url = "/thoughts/Success/"



class DetailThoughts(DetailView):
    model = Thought
    #template_name = "post_thoughts/success.html/"
    #success_url = "/thoughts/Success/" 
    def get_success_url(self):
        return reverse('DetailThoughts', args=[self.object.user.pk])  
                    
    def get_object(self, queryset=None):
    # Retrieve the object to be deleted using the 'pk' from the URL
        return self.model.objects.get(pk=self.kwargs['pk'])
    login_url = reverse_lazy('login')       



class Success(TemplateView):
    template_name = "post_thoughts/success.html/"


# CRUD for the Comment Model

class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = "__all__"
    success_url = reverse_lazy("ListComment")
    login_url = reverse_lazy('login')
    
    

class UpdateComment(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = "__all__"

    def get_success_url(self):
        # Assuming you want to redirect to the user_profile view with a specific primary key
        return reverse('DetailComment', args=[self.object.user.pk])
    
    def get_object(self, queryset=None):
    # Retrieve the object to be deleted using the 'pk' from the URL
        return self.model.objects.get(pk=self.kwargs['pk'])

    login_url = reverse_lazy('login')         


class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    fields = "__all__"

    def get_success_url(self):
        # Assuming you want to redirect to the user_profile view with a specific primary key
        return reverse('DetailComment', args=[self.object.user.pk]) 

    #success_url = "/thoughts/"
    login_url = reverse_lazy('login')
   

class ListComment(ListView):
     model = Comment
     template_name = "post_thoughts/comment_list.html"
     success_url = "/thoughts/SuccessComment/"

class DetailComment(DetailView):
    model = Comment
    template_name = "post_thoughts/comment_detail.html/"
    
                

class SuccessComment(TemplateView):
    template_name = "post_thoughts/comment_list.html/"


