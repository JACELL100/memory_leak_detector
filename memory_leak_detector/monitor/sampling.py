import threading
import time
import psutil

# import models lazily inside functions to avoid Django import-time issues
REGISTRY = {}

class SamplerControl:
    def __init__(self, run, interval=1.0):
        self.run = run
        self.interval = interval
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self._loop, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self._stop.set()
        try:
            self.run.stopped = True
            self.run.save()
        except Exception:
            pass

    def _loop(self):
        from .models import Sample
        pid = self.run.pid
        try:
            proc = psutil.Process(pid)
        except psutil.NoSuchProcess:
            self.run.stopped = True
            try:
                self.run.save()
            except Exception:
                pass
            return
        while not self._stop.is_set():
            try:
                rss = proc.memory_info().rss // 1024  # KB
            except psutil.NoSuchProcess:
                self.run.stopped = True
                try:
                    self.run.save()
                except Exception:
                    pass
                break
            try:
                Sample.objects.create(run=self.run, rss_kb=rss)
            except Exception:
                # ignore DB errors in lab prototype
                pass
            time.sleep(self.interval)

def start_monitor(run_id: int, interval=1.0):
    from django.apps import apps
    MonitorRun = apps.get_model('monitor', 'MonitorRun')
    try:
        run = MonitorRun.objects.get(id=run_id)
    except MonitorRun.DoesNotExist:
        return None
    control = SamplerControl(run, interval)
    REGISTRY[run_id] = control
    control.start()
    return control

def stop_monitor(run_id: int):
    ctrl = REGISTRY.get(run_id)
    if not ctrl:
        return False
    ctrl.stop()
    REGISTRY.pop(run_id, None)
    return True
