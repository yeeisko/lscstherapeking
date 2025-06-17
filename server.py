from flask import Flask, send_from_directory

app = Flask(__name__)

# Serve index.html at the root URL
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Serve index2.html in the /uploads/ path
@app.route('/uploads/index2.html')
def serve_index2():
    return send_from_directory('uploads', 'index2.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
