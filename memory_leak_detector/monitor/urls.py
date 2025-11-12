from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start_run, name='start_run'),
    path('stop/<int:run_id>/', views.stop_run, name='stop_run'),
    path('samples/<int:run_id>/', views.samples_json, name='samples_json'),
    path('dash/', views.dashboard, name='dashboard'),
    path('api/logs/', views.get_logs, name='get_logs'),
]
