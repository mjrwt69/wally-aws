from django.shortcuts import HttpResponse, render
from auth_app.models import Post_Wallpaper
from django.views.generic import ListView
from auth_app.models import Post_Wallpaper
from django.template.loader import render_to_string
from django.http import JsonResponse

# def home(request):
#     uploaded_images = Post_Wallpaper.objects.all().order_by('-created_at')  # Get all uploaded images, ordered by creation date
#     return render(request, 'home.html', {'uploaded_images': uploaded_images})

class home(ListView):
    model = Post_Wallpaper
    template_name = 'home.html'  # Replace with your actual template name
    context_object_name = 'uploaded_images'
    paginate_by = 10 # Number of items per page
    ordering = ['-id']

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('image_list.html', context, request=request)
            return JsonResponse({
                'images_html': html,
                'has_next': context['page_obj'].has_next()
            })
        return self.render_to_response(context)