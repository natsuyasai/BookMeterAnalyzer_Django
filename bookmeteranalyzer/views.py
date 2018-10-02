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
from celery.result import AsyncResult
import os

# Create your views here.
def index(request):
    """ デフォルトページ表示
    """
    posts = Post.objects.all()
    form = PostForm()
    context = {'posts': posts, 'form': form, }
    return render(request, 'bookmeteranalyzer/index.html', context)


def index_nontwitter(request):
    """ デフォルトページ表示(連絡先なし)
    """
    posts = Post.objects.all()
    form = PostForm()
    context = {'posts': posts, 'form': form, }
    return render(request, 'bookmeteranalyzer/index_nontwitter.html', context)
    
def analyze(request):
    """ 解析処理実行
    """
    try:
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
        img_url_str = settings.MEDIA_ROOT + img_file_to_json.replace('"','')
        csv_url_str = settings.MEDIA_ROOT + csv_file_to_json.replace('"','')
        # 結果をjsonとして返す
        return JsonResponse({'img_file_url' : img_url_str, 'csv_file_url' : csv_url_str})
    except:
        import traceback
        traceback.print_exc()
    """
    return render(
        request,
        'bookmeteranalyzer/index.html',
        {'img_file':img_file, 'form': form},
    )
    """


def async_analyze(request):
    """ 解析処理実行
    """
    try:
        print('async_analyze')
        form = PostForm(request.POST)
        analyze_user_id = request.POST.get('user_id')
        # 文字列が数値でなければ処理終了
        if analyze_user_id.isdigit() == False:
            print('failed')
            return JsonResponse({'' : ''})
        # 解析実施
        task = execAnalyze.delay(analyze_user_id)
        # 実行しているタスクIDを返す
        print(task.id)
        print(analyze_user_id)
        return JsonResponse({'task_id' : task.id, 'user_id':analyze_user_id})
    except:
        import traceback
        traceback.print_exc()
        return JsonResponse({'' : ''})


def get_async_analyze_result(request):
    """ 非同期結果取得
    """
    try:
        # 結果取得
        taks_rslt = AsyncResult(request.POST.get('task_id'))
        if taks_rslt.successful() == False:
            # まだ実行中なら即空の結果を返す
            return JsonResponse({'img_file_url' : '', 'csv_file_url' : ''})
        analyze_user_id = request.POST.get('user_id')
        print(taks_rslt)
        print(analyze_user_id)

        # 結果生成
        # 指定ユーザIDの画像をDBから取得
        user_data = AnalyzeResult.objects.filter(user_id=analyze_user_id).first()
        # ImgaeFiledとFileFildをjson化
        img_file_to_json = json.dumps(str(user_data.img_file))
        csv_file_to_json = json.dumps(str(user_data.csv_file))
        # URL生成
        root_path = settings.MEDIA_ROOT
        if settings.DEBUG == True:
            root_path = settings.MEDIA_ROOT_LOCAL
        img_url_str = root_path + img_file_to_json.replace('"','')
        csv_url_str = root_path + csv_file_to_json.replace('"','')
        print(img_url_str)
        print(csv_url_str)
        # 結果をjsonとして返す
        return JsonResponse({'img_file_url' : img_url_str, 'csv_file_url' : csv_url_str})
    except:
        import traceback
        traceback.print_exc()
        # エラー時は再度
        return JsonResponse({'task_id' : taks_rslt.id, 'user_id':analyze_user_id, 'img_file_url':''})