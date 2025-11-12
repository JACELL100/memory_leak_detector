import os, time, psutil, json
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

LOG_FILE = os.path.join(settings.BASE_DIR, 'monitor', 'memory_logs.json')

class MemoryLeakMiddleware(MiddlewareMixin):
    def process_request(self, request):
        self.start_time = time.time()
        self.process = psutil.Process(os.getpid())
        self.start_mem = self.process.memory_info().rss / (1024 * 1024)

    def process_response(self, request, response):
        end_time = time.time()
        end_mem = self.process.memory_info().rss / (1024 * 1024)
        diff = end_mem - self.start_mem
        duration = end_time - self.start_time

        log_entry = {
            "path": request.path,
            "memory_before": round(self.start_mem, 2),
            "memory_after": round(end_mem, 2),
            "diff": round(diff, 2),
            "duration": round(duration, 2),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Write to log file
        with open(LOG_FILE, 'a+') as f:
            f.write(json.dumps(log_entry) + "\n")

        # Alert threshold
        if diff > 5:
            print(f"[⚠️ MEMORY ALERT] {request.path}: +{diff:.2f} MB in {duration:.2f}s")

        return response
