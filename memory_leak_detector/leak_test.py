import time
leak = []
try:
    while True:
        leak.append('x' * 1024 * 50)  # allocate 50 KB repeatedly
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped")
