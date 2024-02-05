import socketio
import base64

# Initialize SocketIO client
sio = socketio.Client()


@sio.event
def connect():
    print("Socket.IO connection established")


@sio.event
def disconnect():
    print("Disconnected from Socket.IO server")


# Function to send image over Socket.IO
def send_image(image_path):
    with open(image_path, "rb") as image_file:
        img_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        sio.emit("video_frame", {"data": "data:image/jpeg;base64," + img_base64})


if __name__ == "__main__":
    # Connect to the Socket.IO server
    sio.connect("http://localhost:5000")

    # Example: send an image
    send_image("image.jpg")

    # Placeholder for additional code (e.g., keep the app running, handle input)

    # Disconnect from the server before shutting down
    sio.disconnect()
    print("Socket.IO client disconnected")
