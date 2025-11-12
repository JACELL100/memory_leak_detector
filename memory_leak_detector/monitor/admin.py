from django.contrib import admin
from .models import MonitorRun, Sample

@admin.register(MonitorRun)
class MonitorRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'pid', 'started_at', 'stopped')

@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ('id', 'run', 'timestamp', 'rss_kb')
    list_filter = ('run',)
