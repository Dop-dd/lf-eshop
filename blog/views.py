from django.shortcuts import render
from .models import Blog

def all_blog(request):
    blogs = Blog.object.all()
    return render(request, 'blog/all_blog.html', {'blogs': blogs})


# Create your views here.
