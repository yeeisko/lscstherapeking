from flask import Flask, send_from_directory

app = Flask(__name__)  # corrected to __name__

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/uploads/index1.html')
def serve_index2():
    return send_from_directory('uploads', 'index1.html')

if __name__ == '__main__':  # corrected to __name__ and __main__
    app.run(host='0.0.0.0', port=5000)
