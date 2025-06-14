from flask import Flask, request, send_from_directory, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Upload IPA File</title>
    </head>
    <body>
      <h1>Upload your IPA file</h1>
      <form id="uploadForm" enctype="multipart/form-data" method="post">
        <input type="file" id="ipaFile" name="ipa" accept=".ipa" required />
        <button type="submit">Upload</button>
      </form>
      <p id="result"></p>

      <script>
        document.getElementById('uploadForm').addEventListener('submit', async function(e) {
          e.preventDefault();
          const fileInput = document.getElementById('ipaFile');
          if (!fileInput.files.length) {
            alert('Please select an IPA file');
            return;
          }

          const file = fileInput.files[0];
          if (!file.name.toLowerCase().endsWith('.ipa')) {
            alert('Only .ipa files are allowed');
            return;
          }

          const formData = new FormData();
          formData.append('ipa', file);

          try {
            const response = await fetch('/upload', {
              method: 'POST',
              body: formData
            });

            if (!response.ok) {
              const errorText = await response.text();
              document.getElementById('result').innerText = 'Error: ' + errorText;
              return;
            }

            const text = await response.text();
            document.getElementById('result').innerHTML = text;
          } catch (err) {
            document.getElementById('result').innerText = 'Upload failed: ' + err.message;
          }
        });
      </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'ipa' not in request.files:
        return "No file part", 400

    file = request.files['ipa']
    if file.filename == '':
        return "No selected file", 400

    if not file.filename.lower().endswith('.ipa'):
        return "Only .ipa files are allowed", 400

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    download_link = f'<a href="/download/{filename}" download>Download {filename}</a>'
    return download_link, 200

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
