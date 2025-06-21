from flask import Flask, request, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os
import uuid
import threading
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024  # 300 MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'ipa'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_old_files(days=60):
    while True:
        now = time.time()
        cutoff = now - days * 86400
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff:
                try:
                    os.remove(filepath)
                except Exception:
                    pass
        time.sleep(24 * 3600)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part."
        file = request.files['file']
        if file.filename == '':
            return "No selected file."
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            download_link = url_for('download_file', filename=unique_filename, _external=True)
            return f"File uploaded successfully!\nDownload link: [Download]({download_link})"
        else:
            return "Invalid file type, only .ipa allowed."
    return render_template('index5.html')

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    cleaner_thread = threading.Thread(target=delete_old_files, daemon=True)
    cleaner_thread.start()
    app.run(debug=True)
