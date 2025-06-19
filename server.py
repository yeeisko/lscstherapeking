from flask import Flask, send_from_directory
import subprocess
import threading

app = Flask(__name__)

# Serve index.html at the root URL
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Serve index2.html at /uploads/index2.html
@app.route('/uploads/index2.html')
def serve_index2():
    return send_from_directory('uploads', 'index2.html')

# Serve index3.html at /uploads/index3.html
@app.route('/uploads/index3.html')
def serve_index3():
    return send_from_directory('uploads', 'index3.html')

# Serve index4.html at /uploads/index4.html
@app.route('/uploads/index4.html')
def serve_index4():
    return send_from_directory('uploads', 'index4.html')

# Function to run info.py in the background
def run_info_py():
    subprocess.run(['python', 'info.py'])

if __name__ == '__main__':
    threading.Thread(target=run_info_py, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
