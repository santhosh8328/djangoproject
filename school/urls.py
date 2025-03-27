from django.urls import path
from .views import *
from school import views
from . import views

urlpatterns = [
path('get-users-list/', views.AllUserDetails.as_view(), name='get-users-list'),
path('users/', user_list, name='user-list'),
path('create-user/', create_user, name='create-user'), 
path('sleep/', sleep_view, name='sleep'),
path('upload/', FileUploadView.as_view(), name='file-upload'),

]
