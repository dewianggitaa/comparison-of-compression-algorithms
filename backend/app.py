from flask import Flask, jsonify, request, send_file
import os
import urllib.request
from werkzeug.utils import secure_filename 

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        resp = jsonify({
            "message": "No file part in the request",
            "status": "failed"
        })
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')
    uploaded_files = []

    for file in files:
        if file.filename == '':
            continue
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_files.append(filename)

    if len(uploaded_files) == 0:
        resp = jsonify({
            "message": "No valid files uploaded",
            "status": "failed"
        })
        resp.status_code = 400
        return resp

    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_files[0]), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
