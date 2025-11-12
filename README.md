# Memory Leak Detector

A small Django app for monitoring memory usage of running Python processes and recording samples to a database. Useful for detecting memory growth over time during long-running processes.

This repository contains a Django project and a `monitor` app which provides:

- A `MonitorRun` model representing a monitoring session (process id, timestamps).
- A `Sample` model storing RSS (resident set size) samples in KB.
- A sampling module (`monitor/sampling.py`) that runs a background thread to periodically record memory usage using `psutil`.
- Views and templates for a simple dashboard.
- Middleware for injecting/monitoring memory usage during requests.

## Quick start

Prerequisites

- Python 3.8+
- pip
- (Optional) A virtual environment

Setup

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies from `requirements.txt`:

```powershell
pip install -r requirements.txt
```

3. Apply migrations and create the database:

```powershell
python manage.py migrate
```

4. (Optional) Create a superuser to access the admin UI:

```powershell
python manage.py createsuperuser
```

5. Run the development server:

```powershell
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the dashboard (or /monitor/ depending on URL config).

## Using the sampler

The project provides programmatic helpers to start and stop background sampling. Example usage from Django shell:

```powershell
python manage.py shell
```

```python
from monitor.sampling import start_monitor, stop_monitor

# Start sampling for a running PID
control = start_monitor(run_id=1, interval=1.0)  # returns control or None

# Stop sampling
stop_monitor(run_id=1)
```

Note: The `start_monitor` helper expects the `MonitorRun` model to exist in the database; create a `MonitorRun` instance first via the admin or shell.

## Running the provided leak test

There's a small `leak_test.py` provided for testing the sampler. Run it from the project root:

```powershell
python leak_test.py
```

If `psutil` is not installed, you will see import errors; install dependencies via `requirements.txt`.

## Troubleshooting

- psutil not found: ensure you installed the packages in `requirements.txt` and that your virtualenv is activated.
- "Process does not exist" messages: the monitored PID exited before or during sampling; the sampler will mark the run stopped.
- If the sampling thread doesn't start, check logs and ensure the Django ORM is reachable (migrations applied).

## Tests

The repository contains `monitor/tests.py`. Run tests with:

```powershell
python manage.py test
```

## Notes and next steps

- The sampler uses `psutil` to read process memory; for production use ensure `psutil` is available in your environment.
- Consider adding unit tests that mock `psutil.Process` and the ORM to make sampler behavior deterministic.
- You can extend `Sample` to capture additional metrics (RSS, VMS, CPU percent) as needed.

## License

This project is provided as-is. Add an appropriate open-source license file if you intend to publish.
