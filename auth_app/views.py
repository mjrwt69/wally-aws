from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm, UserRegisterForm
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from .models import Post_Wallpaper
from .forms import UserImageUploadForm
from django.shortcuts import render, redirect, get_object_or_404

@unauthenticated_user
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


@method_decorator(unauthenticated_user, name='dispatch')
class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        """Called when the form is valid. Logs the user in and displays a success message."""
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        """Called when the form is invalid. Displays an error message."""
        messages.error(self.request, "Invalid username or password. Please try again.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """Redirects the user after successful login."""
        return '/'  # Change '/' to your target URL (e.g., 'home' or another view)


def logout_view(request):
    logout(request)
    return redirect('home') 

@login_required  
def upload_image(request):
    if request.method == 'POST':
        form = UserImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save(commit=False) 
            user_image.user = request.user  # Assign the current user to the image
            user_image.save()  
            return redirect('/')  
    else:
        form = UserImageUploadForm()
    
    return render(request, 'post_wallpaper.html', {'form': form})



@login_required
def profile_view(request):
    """View function for the user's profile page."""
    uploaded_images = Post_Wallpaper.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        action = request.POST.get('action')

        if action == 'delete':
            image = get_object_or_404(Post_Wallpaper, id=image_id, user=request.user)
            if image.image:  # Check if there's an image associated
                image.image.delete(save=False)  # delete the image from storage
            image.delete()  # Delete the image record from the database
            return redirect('profile')

    return render(request, 'profile.html', {'uploaded_images': uploaded_images})

@login_required
def edit_description(request, image_id):
    """View function to edit the description of an uploaded image."""
    image = get_object_or_404(Post_Wallpaper, id=image_id, user=request.user)

    if request.method == 'POST':
        form = UserImageUploadForm(request.POST, instance=image)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserImageUploadForm(instance=image)

    return render(request, 'edit_description.html', {'form': form, 'image': image})