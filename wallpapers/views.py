from django.shortcuts import HttpResponse, render
from auth_app.models import Post_Wallpaper

def home(request):
    uploaded_images = Post_Wallpaper.objects.all().order_by('-created_at')  # Get all uploaded images, ordered by creation date
    return render(request, 'home.html', {'uploaded_images': uploaded_images})