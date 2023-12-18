"""
Flask app using socketio to serve the log files
"""

from file_watcher import FileWatcher

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time


LOG_FILE_PATH = r"./log.txt"
app = Flask(__name__)
socket = SocketIO(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@socket.on("get_log", namespace="/tail")
def get_logs(input_data):
    watcher = FileWatcher(LOG_FILE_PATH)
    emit('log_resp', {'data': watcher.get_logs(input_data['lines'])})
    while True:
        time.sleep(0.5)
        emit('log_resp', {'data': watcher.watch()})


if __name__ == "__main__":
    print("Starting server...")
    socket.run(app, host='localhost', port=5000, debug=True, use_reloader=True)

