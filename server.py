# server.py
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def serve_index():
    # Serve index.html from the root directory
    return send_from_directory('.', 'index.html')

@app.route('/uploads/')
def serve_index2():
    # Serve index2.html from the uploads directory
    return send_from_directory('uploads', 'index2.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
