from django.urls import path
from post_thoughts.views import *

urlpatterns = [
    path("list/", ListThoughts.as_view(),name="ListThoughts"),
    path("detail/<pk>",DetailThoughts.as_view(), name="DetailThoughts"),
    path("create/",CreateThoughts.as_view(),name="CreateThoughts"),
    path("update/<pk>",UpdateThought.as_view(),name="UpdateThought"),
    path("delete/<pk>",DeleteThoughts.as_view(),name="DeleteThoughts"),
    path("Success/",Success.as_view(),name="Success"),
    path("CreateComment/",CreateComment.as_view(),name="CreateComment"),
    path("UpdateComment/<pk>",UpdateComment.as_view(), name="UpdateComment"),
    path("DeleteComment/<pk>",DeleteComment.as_view(), name="DeleteComment"),
    path("ListComment/",ListComment.as_view(),name="ListComment"),
    path("DetailComment/<pk>",DetailComment.as_view(), name="DetailComment"),
    path("SuccessComment/",SuccessComment.as_view(),name="SuccessComment"),
    # home page
    path("home/", Home.as_view(), name="Home"),
]
