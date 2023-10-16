
from django.urls import path
from users.views import *

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/",user_login, name="login"),
    path("logout/",user_logout, name="logout"),
    path("Success/",Success.as_view(),name="Success"),
    #path("ConfirmDeleteProfie/",Confirm_delete_profile.as_view(),name="ConfirmDeleteProfie"),

    path("ChangePass/", Changepass.as_view(), name="ChangePassword"),
    # logged in user profile detail
    path("myprofile/<pk>/",myProfile_detail.as_view(),name="myProfile_detail"),

    # CRUD
    path("profile/",Profile.as_view(), name="Profile"),
    path("UpdateProfile/<pk>",UpdateProfile.as_view(), name="UpdateProfile"),
    path("DeleteProfile/<pk>",DeleteProfile.as_view(),name="DeleteProfile"),
    path("ListProfile/",ListProfile.as_view(), name="ListProfile"),
    path("DetailProfile/<pk>",DetailProfile.as_view(), name="DetailProfile"),
    
]
