from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/uploads/index1.html')
def serve_index2():
    return send_from_directory('uploads', 'index1.html')

@app.route('/uploads/key-matcher.html')
def serve_key_matcher():
    return send_from_directory('uploads', 'key-matcher.html')

# Serve app-access.html from the current directory instead of uploads
@app.route('/app-access.html')
def serve_app_access():
    return send_from_directory('.', 'app-access.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
