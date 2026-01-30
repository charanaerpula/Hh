import os
from pathlib import Path
import tempfile

from app import app
from jobs import _jobs, jobs_lock


def test_download_ready_file(tmp_path):
    client = app.test_client()

    # create a fake finished job with a real file
    job_id = 'testjob123'
    out = tmp_path / 'foo.xlsx'
    out.write_text('dummy')

    with jobs_lock:
        _jobs[job_id] = {
            'id': job_id,
            'status': 'done',
            'path': str(out),
            'output': out.name,
            'progress': {'done': 1, 'total': 1},
        }

    resp = client.get(f'/download/{job_id}')
    assert resp.status_code == 200
    # cleanup
    with jobs_lock:
        _jobs.pop(job_id, None)
