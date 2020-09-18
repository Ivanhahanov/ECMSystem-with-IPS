from flask import Flask, render_template, jsonify, redirect, request, url_for
from werkzeug.utils import secure_filename
from redis import Redis
from rq import Queue
from task import background_task
from flask_cors import CORS, cross_origin
import logging
import os

UPLOAD_FOLDER = 'sandbox/files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_folder='static', static_url_path='')
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some secret key'

app.config['CORS_HEADERS'] = 'Content-Type'
logging.basicConfig(level=logging.DEBUG)
q = Queue(connection=Redis(host='redis', port=6379, db=0, password="sOmE_sEcUrE_pAsS"))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            logging.info('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            logging.info('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/run_task')
@cross_origin()
def run_task():
    # job = q.enqueue(background_task, "12")
    #
    # return jsonify({"data": f"Task ({job.id}) added to queue at {job.enqueued_at}"})

    return jsonify({"data": f"Task ({1}) added to queue at {1}"})


@app.template_filter()
def vue(item):
    # If you see anything about "raw", blame the blog engine, not me. If not,
    # ignore these comments.
    return "{{ " + item + " }}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
