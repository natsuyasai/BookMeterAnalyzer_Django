from django.urls import path

from . import views

app_name = 'bookmeteranalyzer'

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze', views.analyze, name='analyze'),
]