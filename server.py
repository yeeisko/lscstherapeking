from flask import Flask, send_from_directory

app = Flask(__name__)  # Use __name__, not name

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/uploads/index1.html')
def serve_index2():
    return send_from_directory('uploads', 'index1.html')

@app.route('/uploads/Chibadirectinstall.html')
def serve_key_matcher():
    return send_from_directory('uploads', 'Chibadirectinstall.html')

@app.route('/app-access.html')
def serve_app_access():
    return send_from_directory('.', 'app-access.html')

@app.route('/uploads/arabbank.html')
def serve_arabbank():
    return send_from_directory('uploads', 'arabbank.html')

if __name__ == '__main__':  # Use __name__ and '__main__'
    app.run(host='0.0.0.0', port=5000)
