from django.urls import path
from post_thoughts.views import *

urlpatterns = [
    path("thought_list/", ListThoughts.as_view(),name="ListThoughts"),
    path("thought_detail/<pk>",DetailThoughts.as_view(), name="DetailThoughts"),
    path("thought_create/",CreateThoughts.as_view(),name="CreateThoughts"),
    path("thought_update/<pk>",UpdateThought.as_view(),name="UpdateThought"),
    path("thought_delete/<pk>",DeleteThoughts.as_view(),name="DeleteThoughts"),
    path("Success/",Success.as_view(),name="Success"),
    #CRUD URL Comment
    #path('thoughts/<int:thought_id>/comments/create/', CreatemyComment.as_view(), name='create_comment'),
    #path('thoughts/<int:thought_id>/comments/', ListmyComments.as_view(), name='list_comments'),
    #path('thoughts/<int:thought_id>/comments/<int:pk>/update/', UpdateComment.as_view(), name='update_comment'),

    path("Comment/",CreateComment.as_view(),name="CreateComment"),
    path("UpdateComment/<pk>",UpdateComment.as_view(), name="UpdateComment"),
    path("DeleteComment/<pk>",DeleteComment.as_view(), name="DeleteComment"),
    path("ListComment/",ListComment.as_view(),name="ListComment"),
    path("DetailComment/<pk>",DetailComment.as_view(), name="DetailComment"),
    path("SuccessComment/",SuccessComment.as_view(),name="SuccessComment"),
    
    # home page
    path("home/", Home.as_view(), name="Home"),
    # about page
    path("about/", About.as_view(), name="About"),


]
