from django.db import models

class MonitorRun(models.Model):
    pid = models.IntegerField()
    started_at = models.DateTimeField(auto_now_add=True)
    stopped = models.BooleanField(default=False)

    def __str__(self):
        return f"Monitor #{self.id} (PID {self.pid})"

class Sample(models.Model):
    run = models.ForeignKey(MonitorRun, on_delete=models.CASCADE, related_name='samples')
    timestamp = models.DateTimeField(auto_now_add=True)
    rss_kb = models.IntegerField()

    class Meta:
        ordering = ['timestamp']
