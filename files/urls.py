from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('pylims/', views.index, name='index'),
    path('pylims/test', views.test, name='test'),
    path('pylims/savechange', views.savechange, name='savechange'),
    path('pylims/getflowcell', views.getflowcell, name='getflowcell'),
]
