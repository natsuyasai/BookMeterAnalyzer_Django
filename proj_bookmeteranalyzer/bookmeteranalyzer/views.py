from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.files import File
from django.conf import settings
from django_cleanup import cleanup
from .models import Post
from .models import AnalyzeResult
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
    analyze_user_id = request.POST.get('user_id')
    execAnalyze(analyze_user_id)
    # 結果の画像を登録
    filename = analyze_user_id + '.png'
    img_open = open('./bookmeteranalyzer/analyzedata/image/' + filename, 'rb')
    analyze_rslt = AnalyzeResult()
    analyze_rslt.user_id = analyze_user_id
    analyze_rslt.img_file.save(filename, File(img_open), save=True)
    # 結果生成
    img_file = AnalyzeResult.objects.filter(user_id=analyze_user_id)
    return render(
        request,
        'bookmeteranalyzer/index.html',
        {'img_file':img_file, 'form': form},
    )