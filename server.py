from flask import Flask, render_template, request, jsonify
import asyncio
import threading
from spam import spam_user

app = Flask(__name__)
active_spams = {}

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_spam', methods=['POST'])
def start_spam():
    data = request.json
    chat_id = data.get('chat_id')
    username = data.get('username')

    if not chat_id or not username:
        return jsonify({'status': 'error', 'message': 'chat_id and username required'}), 400

    if chat_id not in active_spams:
        loop = asyncio.new_event_loop()
        task = loop.create_task(spam_user(chat_id, username))
        active_spams[chat_id] = (task, loop)
        threading.Thread(target=start_loop, args=(loop,), daemon=True).start()
        return jsonify({'status': 'started'})
    else:
        return jsonify({'status': 'already_running'})

if __name__ == '__main__':
    app.run(debug=True)
