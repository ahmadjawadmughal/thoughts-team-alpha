from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,UpdateView,FormView,DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from post_thoughts.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from post_thoughts.forms import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Create your views here------------------------------------------------------------------------------


# home page 
class Home(TemplateView):
    template_name = "post_thoughts/home.html"




# about page
class About(LoginRequiredMixin,TemplateView):
    login_url = "/users/login/"
    template_name = "post_thoughts/about.html"




# change password
class ChangePass(LoginRequiredMixin, UpdateView):
    model = Thought
    fields = ["password"]

    def get_success_url(self):
        return reverse('ListThoughts')
    
    login_url = reverse_lazy('login')   #if user not loggedin, first this will redirect user for login page


# Thoughts CRUD Operation ------------------------------------------------------------------------------------------------


class CreateThoughts(LoginRequiredMixin, CreateView):
    model = Thought
    fields = ["title","thought","image","is_private"]

    def get_success_url(self):
        return reverse('MyThoughts')
    
    def form_valid(self, form):
        # Set the current user as the user of the thought
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    login_url = reverse_lazy('login')   #if user not loggedin, first this will redirect user for login page




class UpdateThought(LoginRequiredMixin, UpdateView):
    model = Thought
    fields = ['title','thought','image','is_private']

    def get_success_url(self):
        return reverse('DetailThoughts', args=[self.object.pk])  
    login_url = reverse_lazy('login')




class DeleteThoughts(LoginRequiredMixin, DeleteView):
    model = Thought
    
    def get_success_url(self):
        return reverse('ListThoughts')
    login_url = reverse_lazy('login')




class ListThoughts(LoginRequiredMixin,ListView):
    model = Thought
    login_url = reverse_lazy('login')
    template_name = "post_thoughts/thought_list.html"




class DetailThoughts(DetailView):
    model = Thought
    login_url = reverse_lazy('login')  
    def success_url(self):
        return reverse('DetailThoughts', args = [self.object.user.pk])
    
    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thought = self.get_object()

        comments = Comment.objects.filter(thoughts=thought)

        context['comments'] = comments
        return context     




# Displaying thoughts of loggedin/current user
class My_thoughts(LoginRequiredMixin,ListView):
    model = Thought
    template_name = "post_thoughts/my_thought.html"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    



class Success(TemplateView):
    template_name = "post_thoughts/success.html/"


# CRUD for the Comment Model-----------------------------------------------------------------------------------

class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["text"]
    #success_url = reverse_lazy("")
    login_url = reverse_lazy('login')
    
    def get_success_url(self):
        return reverse('DetailThoughts', args=[self.object.thoughts.pk])
   
  
    def form_valid(self, form):
        thought_pk = self.kwargs["thought_pk"]  #get the thought pk from URL
        thought = get_object_or_404(Thought, pk=thought_pk)
        form.instance.thoughts = thought
        # Set the current user as the user of the thought
        form.instance.user = self.request.user
        return super().form_valid(form)




class UpdateComment(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ["text"]
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('DetailThoughts', args=[self.object.thoughts.pk])
         



class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse('DetailThoughts', args=[self.object.thoughts.pk])


   

class ListComment(LoginRequiredMixin,ListView):
    model = Comment
    login_url = "/users/login/"
    template_name = "post_thoughts/comment_list.html"
  



class DetailComment(DetailView):
    model = Comment
    template_name = "post_thoughts/comment_detail.html/"
    
                
class SuccessComment(TemplateView):
    template_name = "post_thoughts/comment_list.html/"


# search bar functionality-------------------------------------------------------------------

#Added Search functionality where a user inputs text, all the Thoughts that even contain some chunk of that text in thought or in the title, appear in the list.
@login_required
def search(request):
    query = request.GET["query"] 
    if len(query) > 60:  #check for length of query
        object_list = Thought.objects.none() # empty queryset

    else:
        object_listTitle = Thought.objects.filter(title__icontains=query)
        object_listThought = Thought.objects.filter(thought__icontains=query)
        object_list = object_listTitle.union(object_listThought) # AUB
     
    context = {
        "object_list" : object_list,
        "query" : query
    }
    return render(request,"post_thoughts/search.html",context)



# View to Share thought with users-------------------------------------------------------------
@login_required
def share_form(request,thought_pk):
    #owner = request.user  # Get the currently logged-in user
    thought = Thought.objects.get(id=thought_pk)

    if request.method == "POST":  # 'POST' request execute means when form is submitted 
        form = Thought_ShareForm(request.POST)

        if form.is_valid():
            shared_user = form.cleaned_data["shared_with"] 
            thought.shared_with.add(*shared_user)   # Added the shared user to the Thought's 'shared_with' ManyToMany field
            return redirect('DetailThoughts', thought.id ) 
           
        else: #if form data isnt valid show blank form
            form = Thought_ShareForm()  
    
    else:
        form = Thought_ShareForm()
    
    return render(request, 'post_thoughts/share_form.html/', {"form": form})




# Displaying Thoughts shared with request.user------------------------------------------------
class share_with_me(LoginRequiredMixin, ListView):
    model = Thought
    template_name = "post_thoughts/shared_with_me.html"
    context_object_name = "thoughts"

    def get_queryset(self): #retrieve all thoughts shared with request.user
        print(self.request.user)
        all_thoughts = Thought.objects.filter(shared_with=self.request.user)
        return all_thoughts

    login_url = "/users/login/" 




