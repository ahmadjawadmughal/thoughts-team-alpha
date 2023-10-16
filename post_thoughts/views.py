from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
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


class About(LoginRequiredMixin,TemplateView):
    login_url = "/users/login/"
    template_name = "post_thoughts/about.html"

# change password
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
        return reverse('ListThoughts')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    login_url = reverse_lazy('login')   




class UpdateThought(LoginRequiredMixin, UpdateView):
    model = Thought
    fields = "__all__"

    def get_success_url(self):
        return reverse('DetailThoughts', args=[self.object.user.pk])  
    
    def get_object(self, queryset=None):  #retrieve the thought to be updated from URL by pk as kwarg
        return self.model.objects.get(pk=self.kwargs['pk'])

    login_url = reverse_lazy('login')



class DeleteThoughts(LoginRequiredMixin, DeleteView):
    model = Thought
    success_url = reverse_lazy('ListThoughts')
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
    # Retrieve the object to be deleted using the 'pk' from the URL
        return self.model.objects.get(pk=self.kwargs['pk'])






class DetailThoughts(LoginRequiredMixin,DetailView):
    model = Thought
                    
    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])



class Success(TemplateView):
    template_name = "post_thoughts/success.html/"
    #can use get_context_data as well for sending data to html by context
#------------------------------------------------------------------------------------------

# CRUD for the Comment Model
    
#----------------------------------------------------------

class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = "__all__"
    success_url = reverse_lazy("ListComment")
    """
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
    """    

    def form_valid(self, form):
        thought_pk = self.kwargs['thought_pk']
        thought = Thought.objects.get(pk=thought_pk)
        form.instance.thought = thought
        form.instance.user = self.request.user
        return super().form_valid(form)

    login_url = reverse_lazy('login')




class UpdateComment(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = "__all__"

    def get_success_url(self):
        # Assuming you want to redirect to the user_profile view with a specific primary key
        return reverse('DetailComment', args=[self.object.user.pk])
    
#we will get queryset of whole comments so i will overwrite query method here

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
   

class ListComment(LoginRequiredMixin,ListView):
     model = Comment
     login_url = "/users/login/"
     template_name = "post_thoughts/comment_list.html"
     success_url = "/thoughts/SuccessComment/"

class DetailComment(DetailView):
    model = Comment
    template_name = "post_thoughts/comment_detail.html/"
    
                

class SuccessComment(TemplateView):
    template_name = "post_thoughts/comment_list.html/"
#-------------------------------------------------------------------------------------------------------

@csrf_exempt
@login_required
def share_form(request):
    owner = request.user  # Get the currently logged-in user
    if request.method == "POST":
        form = Thought_ShareForm(request.POST)
        if form.is_valid():
            thought = form.cleaned_data["thought"]
            username = form.cleaned_data["username"]     
            try:
                thought = Thought.objects.get(thought=thought, user=owner)  # Check if the tweet belongs to the logged-in user
            except Thought.DoesNotExist:
                return JsonResponse({"message": "You cannot share a tweet that doesn't belong to you."}, status=400)
            
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"message": "User not found."}, status=400)
            
            all_shared_thoughts = user.share_thoughts.all()
            
            if thought in all_shared_thoughts:
                return JsonResponse({"message": f"Tweet '{thought.title}' is already shared with '{user.username}'."})
            else:
                user.share_thoughts.add(thought)
                return JsonResponse({"message": f"Tweet '{thought.title}' shared successfully with '{thought.title}'."})
        else:
            return JsonResponse({"message": "Invalid form data."}, status=400)
    
    else:
        form = Thought_ShareForm()
    
    return render(request, 'share_form.html/', {"form": form})


# search bar functionality

def search(request):
    query = request.GET["query"] # "query" is the name property of the <input> tag
    if len(query) > 60:
        object_list = Thought.objects.none() # empty queryset
    else:

        object_listTitle = Thought.objects.filter(title__icontains=query)
        object_listThought = Thought.objects.filter(thought__icontains=query)
        object_list = object_listTitle.union(object_listThought) # AUB
   # if object_list.count() == 0:
   #     messages.warning(request,"No search results found. Please enter correct query.")    
    context = {
        "object_list" : object_list,
        "query" : query
    }
    return render(request,"post_thoughts/search.html",context)
