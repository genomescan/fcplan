from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('pylims/', views.index, name='index'),
    path('pylims/test', views.test, name='test'),
    path('pylims/getflowcell', views.getflowcell, name='getflowcell'),
    path('pylims/stagesample', views.stagesample, name='stagesample'),
    path('pylims/getsampleinfo/<id>', views.getsampleinfo, name='getsampleinfo'),
    path('pylims/get_sequencable_lanes/<platform>/<fctype>', views.get_sequencable_lanes, name='get_sequencable_lanes'),
    path('pylims/getstage', views.getstage, name='getstage'),
    path('pylims/getstage/<seq_type>/<seq_fc>', views.getstage, name='getstage'),
    path('pylims/remove_sample', views.remove_sample, name='remove_sample'),
    path('pylims/save_remark', views.save_remark, name='save_remark'),
    path('pylims/save_on_stage', views.save_on_stage, name='save_on_stage'),
    path('pylims/remove_lanes_from_stage', views.remove_lanes_from_stage, name='remove_lanes_from_stage')
]
