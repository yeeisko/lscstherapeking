from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/uploads/index1.html')
def serve_index2():
    return send_from_directory('uploads', 'index1.html')

@app.route('/uploads/test.html')
def serve_key_matcher():
    return send_from_directory('uploads', 'test.html')

@app.route('/app-access.html')
def serve_app_access():
    return send_from_directory('.', 'app-access.html')

# Serve server.js located in file-uploader directory
@app.route('/file-uploader/server.js')
def serve_server_js():
    return send_from_directory('file-uploader', 'server.js')

# Serve public.html located in file-uploader directory
@app.route('/file-uploader/public.html')
def serve_public_html():
    return send_from_directory('file-uploader', 'public.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
