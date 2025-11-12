import os
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .models import MonitorRun
from . import sampling
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def index(request):
    runs = MonitorRun.objects.order_by('-started_at')[:10]
    return render(request, 'monitor/index.html', {'runs': runs})

@csrf_exempt
def start_run(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')
    try:
        payload = json.loads(request.body.decode())
        pid = int(payload.get('pid'))
        interval = float(payload.get('interval', 1.0))
    except Exception:
        return HttpResponseBadRequest('Invalid payload')
    run = MonitorRun.objects.create(pid=pid)
    sampling.start_monitor(run.id, interval=interval)
    return JsonResponse({'run_id': run.id})

@csrf_exempt
def stop_run(request, run_id):
    sampling.stop_monitor(int(run_id))
    return JsonResponse({'stopped': True})

def samples_json(request, run_id):
    try:
        run = MonitorRun.objects.get(id=run_id)
    except MonitorRun.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)
    samples = run.samples.all().values('timestamp', 'rss_kb')
    data = [{'timestamp': s['timestamp'].isoformat(), 'rss_kb': s['rss_kb']} for s in samples]
    return JsonResponse({'run_id': run.id, 'pid': run.pid, 'samples': data})

LOG_FILE = os.path.join(settings.BASE_DIR, 'monitor', 'memory_logs.json')

def dashboard(request):
    return render(request, 'monitor/dashboard.html')

def get_logs(request):
    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            for line in f.readlines()[-20:]:  # last 20 entries
                data.append(json.loads(line))
    return JsonResponse(data, safe=False)