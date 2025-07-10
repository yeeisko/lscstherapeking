from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create uploads folder if it doesn't exist

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Simple upload form with link after upload
HTML = '''
<!doctype html>
<title>Upload File</title>
<h1>Upload a file</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file required>
  <input type=submit value=Upload>
</form>
{% if file_url %}
<p>File uploaded! Download it <a href="{{ file_url }}" target="_blank">here</a></p>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Error: No file selected", 400
        file = request.files['file']
        if file.filename == '':
            return "Error: No file selected", 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        file_url = url_for('uploaded_file', filename=file.filename, _external=True)
        return render_template_string(HTML, file_url=file_url)
    return render_template_string(HTML)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
