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



class ListThoughts(ListView):
    model = Thought
    template_name = "post_thoughts/thought_list.html"
    success_url = "/thoughts/Success/"



class DetailThoughts(DetailView):
    model = Thought
    #template_name = "post_thoughts/success.html/"
    success_url = "/thoughts/Success/"        



class Success(TemplateView):
    template_name = "post_thoughts/success.html/"



# CRUD for the Comment Model

class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = "__all__"

    def get_success_url(self):
        # Assuming you want to redirect to the user_profile view with a specific primary key
        return reverse('DetailComment', args=[self.object.user.pk])
    login_url = reverse_lazy('login')


class UpdateComment(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = "__all__"

    success_url = "/thoughts/comment_detail.html/"
    login_url = reverse_lazy('login')

class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    fields = "__all__"

    success_url = "/thoughts/SuccessComment/"
    login_url = reverse_lazy('login')

class ListComment(ListView):
     model = Comment

     success_url = "/thoughts/SuccessComment/"

class DetailComment(DetailView):
    model = Comment
    template_name = "post_thoughts/comment_detail.html/"
    
                

class SuccessComment(TemplateView):

    template_name = "post_thoughts/success.html/"


