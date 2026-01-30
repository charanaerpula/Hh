import threading
import uuid
import time
from pathlib import Path
from typing import Dict

from m import run_job

_jobs: Dict[str, dict] = {}
jobs_lock = threading.Lock()


def create_job(url, start, end, output="ou_results.xlsx", protect_password=None, max_workers=10):
    job_id = uuid.uuid4().hex[:8]
    job = {
        "id": job_id,
        "url": url,
        "start": start,
        "end": end,
        "output": str(Path(output).name),
        "status": "queued",
        "progress": {"done": 0, "total": end - start + 1},
        "created_at": time.time(),
        "started_at": None,
        "finished_at": None,
        "error": None,
        "path": None,
    }
    with jobs_lock:
        _jobs[job_id] = job

    def _run():
        job["status"] = "running"
        job["started_at"] = time.time()

        def _progress(done, total):
            job["progress"]["done"] = done
            job["progress"]["total"] = total

        try:
            outp = run_job(url, start, end, output, protect_password=protect_password, max_workers=max_workers, progress_callback=_progress)
            job["status"] = "done"
            job["path"] = str(outp)
            job["finished_at"] = time.time()
        except Exception as e:
            job["status"] = "failed"
            job["error"] = str(e)
            job["finished_at"] = time.time()

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return job_id


def get_job(job_id):
    with jobs_lock:
        return _jobs.get(job_id)


def list_jobs():
    with jobs_lock:
        return list(_jobs.values())
