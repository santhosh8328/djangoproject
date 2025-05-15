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
    

UPLOAD_DIR2 = '/data'

# Ensure the directory exists
os.makedirs(UPLOAD_DIR2, exist_ok=True)

# New class to handle file saving
class FileStorageHandler2:
    def __init__(self, upload_dir):
        self.upload_dir = upload_dir

    def save_file(self, file):
        file_path = os.path.join(self.upload_dir, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return file_path

class FileUploadView2(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']

            try:
                storage_handler = FileStorageHandler2(UPLOAD_DIR2)
                file_path = storage_handler.save_file(file)
                return Response(
                    {"message": "File uploaded successfully", "file_path": file_path}, 
                    status=200
                )
            except Exception as e:
                return Response({"error": str(e)}, status=500)

        return Response(serializer.errors, status=400)


class ListUploadedFilesView2(APIView):
    def get(self, request):
        upload_dir = UPLOAD_DIR2
        
        # Check if the directory exists
        if not os.path.exists(upload_dir):
            return Response({"error": "Upload directory does not exist"}, status=404)
        
        # List all files in the directory
        files = os.listdir(upload_dir)

        return Response({
            "UPLOAD_DIR": upload_dir,
            "files": files if files else "No files uploaded yet."
        })
        
    
    
class ListUploadedFilesView(APIView):
    def get(self, request):
        upload_dir = settings.UPLOAD_DIR
        
        # Check if the directory exists
        if not os.path.exists(upload_dir):
            return Response({"error": "Upload directory does not exist"}, status=404)
        
        # List all files in the directory
        files = os.listdir(upload_dir)

        return Response({
            "UPLOAD_DIR": upload_dir,
            "files": files if files else "No files uploaded yet."
        })
        
        
class CheckHealthOfApplication(APIView):
    def get(self, request):
        return Response(
            {"status": "healthy", "message": "Application is running correctly"},
            status=status.HTTP_200_OK
        )

class CheckReadyOfApplication(APIView):
    def get(self, request):
        return Response(
            {"status": "healthy", "message": "Application is Ready to accept requests"},
            status=status.HTTP_200_OK
        )
        