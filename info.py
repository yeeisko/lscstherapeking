from flask import Flask, request, render_template_string, send_from_directory, abort
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
  <title>Upload Image</title>
</head>
<body>
  <h2>Upload Image</h2>
  <form method="POST" action="/uploads/upload" enctype="multipart/form-data">
    <input type="file" name="image" accept="image/*" required>
    <button type="submit">Upload</button>
  </form>
  {% if url %}
    <p>Image uploaded successfully! Access it here: <a href="{{ url }}" target="_blank">{{ url }}</a></p>
  {% endif %}
</body>
</html>
'''

@app.route('/uploads/index4.html')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/uploads/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file part", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    ext = os.path.splitext(file.filename)[1].lower()
    allowed = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    if ext not in allowed:
        return "Unsupported file type", 400

    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    url = f"https://lscstherapeking.xyz/uploads/{filename}"
    return render_template_string(HTML_PAGE, url=url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    allowed = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
    if not filename.lower().endswith(allowed):
        abort(404)
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
