from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class Post_Wallpaper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who uploaded the image
    image = models.ImageField(upload_to='uploads/')  # Upload directory for images
    description = models.TextField(default=None)  # Field for the image description
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of upload

    def __str__(self):
        return f"Image uploaded by {self.user.username} on {self.created_at}"
    
@receiver(post_delete, sender=Post_Wallpaper)
def delete_image_files(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
