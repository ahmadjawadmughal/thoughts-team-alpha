from django.shortcuts import render
from django.views.generic.edit import CreateView,UpdateView,FormView,DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from post_thoughts.models import *
# Create your views here.

class CreateThoughts(CreateView):
    model = Thought
    fields = "__all__"
    success_url = "/thoughts/Success/"

class UpdateThought(UpdateView):
    model = Thought
    fields = "__all__"
    success_url = "/thoughts/Success/"

class DeleteThoughts(DeleteView):
    model = Thought
    fields = "__all__"
    success_url = "/thoughts/Success/"

class ListThoughts(ListView):
    model = Thought

    success_url = "/thoughts/Success/"

class DetailThoughts(DetailView):
    model = Thought

    success_url = "/thoughts/Success/"        

class Success(TemplateView):
    template_name = "post_thoughts/success.html/"

# CRUD for the Comment Model


class CreateComment(CreateView):
    model = Comment
    fields = "__all__"

    success_url = "/thoughts/SuccessComment/"

class UpdateComment(UpdateView):
    model = Comment
    fields = "__all__"

    success_url = "/thoughts/SuccessComment/"

class DeleteComment(DeleteView):
    model = Comment
    fields = "__all__"

    success_url = "/thoughts/SuccessComment/"

class ListComment(ListView):
     model = Comment

     success_url = "/thoughts/SuccessComment/"

class DetailComment(DetailView):
    model = Comment

    success_url = "/thoughts/SuccessComment/"             

class SuccessComment(TemplateView):

    template_name = "post_thoughts/success.html/"


# home page

class Home(TemplateView):
    template_name = "post_thoughts/home.html"