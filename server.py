from flask import Flask, send_from_directory

app = Flask(name)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/uploads/index1.html')
def serve_index2():
    return send_from_directory('uploads', 'index1.html')

@app.route('/uploads/test.html')
def serve_key_matcher():
    return send_from_directory('uploads', 'test.html')

# Serve app-access.html from the current directory instead of uploads
@app.route('/app-access.html')
def serve_app_access():
    return send_from_directory('.', 'app-access.html')

if name == 'main':
    app.run(host='0.0.0.0', port=5000)
