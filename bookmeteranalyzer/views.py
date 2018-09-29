from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.urls import reverse
from django.core.files import File
from django.conf import settings
from django_cleanup import cleanup
import json
from .models import Post
from .models import AnalyzeResult
from .forms import PostForm
from .script.analyzer import execAnalyze


# Create your views here.
def index(request):
    """ デフォルトページ表示
    """
    posts = Post.objects.all()
    form = PostForm()
    context = {'posts': posts, 'form': form, }
    return render(request, 'bookmeteranalyzer/index.html', context)
    
def analyze(request):
    """ 解析処理実行
    """
    form = PostForm(request.POST)
    analyze_user_id = request.POST.get('user_id')
    # 文字列が数値でなければ処理終了
    if analyze_user_id.isdigit() == False:
        return render(
            request,
            'bookmeteranalyzer/index.html',
            {'img_file': None, 'form': form},
            )
    # 解析実施
    execAnalyze(analyze_user_id)
    # 結果の画像を登録
    img_filename = analyze_user_id + '.png'
    img_open = open('./bookmeteranalyzer/analyzedata/image/' + img_filename, 'rb')
    # 解析用csv登録
    csv_filename = analyze_user_id + '.csv'
    csv_open = open('./bookmeteranalyzer/analyzedata/csv/' + csv_filename, 'rb')
    analyze_rslt = AnalyzeResult()
    analyze_rslt.user_id = analyze_user_id
    analyze_rslt.img_file.save(img_filename, File(img_open), save=True)
    analyze_rslt.csv_file.save(csv_filename, File(csv_open), save=True)
    # 結果生成
    # 指定ユーザIDの画像をDBから取得
    user_data = AnalyzeResult.objects.filter(user_id=analyze_user_id).first()
    # ImgaeFiledとFileFildをjson化
    img_file_to_json = json.dumps(str(user_data.img_file))
    csv_file_to_json = json.dumps(str(user_data.csv_file))
    # URL生成
    img_url_str = "media/" + img_file_to_json.replace('"','')
    csv_url_str = "media/" + csv_file_to_json.replace('"','')
    # 結果をjsonとして返す
    return JsonResponse({'img_file_url' : img_url_str, 'csv_file_url' : csv_url_str})
    """
    return render(
        request,
        'bookmeteranalyzer/index.html',
        {'img_file':img_file, 'form': form},
    )
    """