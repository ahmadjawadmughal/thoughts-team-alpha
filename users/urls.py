
from django.urls import path
from users.views import *

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/",user_login, name="login"),
    path("logout/",user_logout, name="logout"),
    path("Success/",Success.as_view(),name="Success"),
    # CRUD
    path("profile/",Profile.as_view(), name="Profile"),
    path("UpdateProfile/<pk>",UpdateProfile.as_view(), name="UpdateProfile"),
    path("DeleteProfile/<pk>",DeleteProfile.as_view(),name="DeleteProfile"),
    path("ListProfile/",ListProfile.as_view(), name="ListProfile"),
    path("DetailProfile/<pk>",DetailProfile.as_view(), name="DetailProfile"),

]
