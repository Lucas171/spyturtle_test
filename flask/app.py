from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def home():
    return render_template("index.html")


@socketio.on("video_frame")
def handle_video_frame(data):
    # Broadcast the received video frame to all connected clients
    socketio.emit("display_frame", data)


if __name__ == "__main__":
    socketio.run(app, debug=True)
