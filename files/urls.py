from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('pylims/', views.index, name='index'),
    path('pylims/test', views.test, name='test'),
    path('pylims/savechange', views.savechange, name='savechange'),
    path('pylims/getflowcell', views.getflowcell, name='getflowcell'),
    path('pylims/stagesample', views.stagesample, name='stagesample'),
    path('pylims/getsampleinfo/<id>', views.getsampleinfo, name='getsampleinfo'),
    path('pylims/get_sequencable_lanes/<platform>/<fctype>', views.get_sequencable_lanes, name='get_sequencable_lanes'),
]
