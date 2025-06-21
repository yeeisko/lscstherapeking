import subprocess
from flask import Flask, send_from_directory

app = Flask(__name__)  # corrected __name__

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/uploads/index2.html')
def serve_index2():
    return send_from_directory('uploads', 'index2.html')

@app.route('/uploads/index3.html')
def serve_index3():
    return send_from_directory('uploads', 'index3.html')

@app.route('/uploads/index5.html')  # new route for index5.html
def serve_index5():
    return send_from_directory('uploads', 'index5.html')

@app.route('/run-upload')
def run_upload():
    result = subprocess.run(['python3', 'uploads/upload.py'], capture_output=True, text=True)

    if result.returncode == 0:
        return f"upload.py ran successfully!\nOutput:\n{result.stdout}"
    else:
        return f"Error running upload.py:\n{result.stderr}", 500

if __name__ == '__main__':  # corrected __name__ and __main__
    app.run(host='0.0.0.0', port=5000)
