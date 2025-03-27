import os
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from .serializers import FileUploadSerializer

from .forms import *
from .models import *
from .tasks import sleep_task

class AllUserDetails(APIView):
    def get(self,request):  
        user_data = list(User.objects.all().values())  # Remove .using('test_database')
        if user_data:  
            return Response({"data": user_data})
        else:
            return Response({"data": []})
        
def user_list(request):
    users = User.objects.all()  # Retrieve all users from the database
    return render(request, 'school/user_list.html', {'users': users})

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, "User was created successfully!")  # Add a success message
            return redirect('create-user')  # Redirect to the same page to clear the form
    else:
        form = UserForm()  # Create an empty form instance for GET requests
    return render(request, 'school/create_user.html', {'form': form})




@api_view(['POST'])
def sleep_view(request):
    seconds = request.data.get('seconds', 0)  # Get seconds from request body
    if isinstance(seconds, int):
        task = sleep_task.delay(seconds)  # Call the Celery task
        return Response({
            'status': 'success',
            'task_id': task.id,
            'message': 'Task has been started'
        })
    return Response({
        'status': 'error',
        'message': 'Invalid input. Please provide a number.'
    })



UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'uploaded_files')

os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            file_path = os.path.join(UPLOAD_DIR, file.name)

            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            return Response({"message": "File uploaded successfully", "file_path": file_path}, status=200)

        return Response(serializer.errors, status=400)