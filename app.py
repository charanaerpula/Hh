from flask import Flask, request, redirect, url_for, render_template, send_from_directory, abort, jsonify
from pathlib import Path
import os

from jobs import create_job, get_job, list_jobs

app = Flask(__name__)

OUTPUT_DIR = Path.cwd()

@app.route('/')
def index():
    jobs = list_jobs()
    return render_template('index.html', jobs=jobs)

@app.route('/start', methods=['POST'])
def start():
    url = request.form.get('url')
    start = request.form.get('start')
    end = request.form.get('end')
    output = request.form.get('output') or 'ou_results.xlsx'
    protect = request.form.get('protect') or None

    if not (url and start and end):
        return "url, start and end are required", 400
    try:
        start_i = int(start)
        end_i = int(end)
    except ValueError:
        return "start and end must be integers", 400

    job_id = create_job(url, start_i, end_i, output=output, protect_password=protect)
    return redirect(url_for('status_page', job_id=job_id))

@app.route('/status/<job_id>')
def status_page(job_id):
    job = get_job(job_id)
    if not job:
        abort(404)
    return render_template('status.html', job=job)

@app.route('/api/status/<job_id>')
def api_status(job_id):
    job = get_job(job_id)
    if not job:
        return jsonify({"error":"not found"}), 404
    return jsonify(job)

@app.route('/download/<job_id>')
def download(job_id):
    job = get_job(job_id)
    if not job:
        abort(404)
    if job['status'] != 'done' or not job['path']:
        return "Not ready", 400
    path = Path(job['path'])
    if not path.exists():
        return "File missing", 404
    return send_from_directory(directory=str(path.parent), filename=path.name, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
