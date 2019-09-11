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
    path('pylims/getstage', views.getstage, name='getstage'),
    path('pylims/remove_sample', views.remove_sample, name='remove_sample'),
    path('pylims/save_remark', views.save_remark, name='save_remark'),
]
