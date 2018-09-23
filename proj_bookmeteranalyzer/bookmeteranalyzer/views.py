from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Post
from .forms import PostForm
from .script.analyzer import execAnalyze


# Create your views here.
def index(request):
    posts = Post.objects.all()
    form = PostForm()
    context = {'posts': posts, 'form': form, }
    return render(request, 'bookmeteranalyzer/index.html', context)
    
def analyze(request):
    form = PostForm(request.POST)
    execAnalyze(request.POST.get('userID'))
    #form.save(commit=True)
    return HttpResponseRedirect(reverse('bookmeteranalyzer:index'))
