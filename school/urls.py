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
path('list-files/', ListUploadedFilesView.as_view(), name='list-files'),
path('health/', CheckHealthOfApplication.as_view(),name='health'),
path('ready/', CheckReadyOfApplication.as_view(),name='health'),
path('upload2/', FileUploadView2.as_view(), name='file-upload2'),
path('list-files2/', ListUploadedFilesView2.as_view(), name='list-files2'),



]
