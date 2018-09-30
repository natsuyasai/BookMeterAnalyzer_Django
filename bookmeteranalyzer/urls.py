from django.urls import path

from . import views

app_name = 'bookmeteranalyzer'

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze', views.analyze, name='analyze'),
    path('async_analyze', views.async_analyze, name='async_analyze'),
    path('get_async_analyze_result', views.get_async_analyze_result, name='get_async_analyze_result'),
]