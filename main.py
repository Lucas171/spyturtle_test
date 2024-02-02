from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO

import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

app = Flask(__name__)
socketio = SocketIO(app)

model = YOLO("yolov8n-seg.pt")  # segmentation model
names = model.model.names

cap = cv2.VideoCapture(0)

w, h, fps = (
    int(cap.get(x))
    for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS)
)

process_every_n_frames = 6
frame_counter = 0
video_running = False  # Variable to track video processing state


def generate_frames():
    global frame_counter  # Declare frame_counter as a global variable

    while True:
        if video_running:
            ret, im0 = cap.read()
            if not ret:
                print(
                    "Video frame is empty or video processing has been successfully completed."
                )
                break

            if frame_counter % process_every_n_frames == 0:
                results = model.predict(im0)
                annotator = Annotator(im0, line_width=2)

                if results[0].masks is not None:
                    clss = results[0].boxes.cls.cpu().tolist()
                    masks = results[0].masks.xy
                    for mask, cls in zip(masks, clss):
                        annotator.seg_bbox(
                            mask=mask,
                            mask_color=colors(int(cls), True),
                            det_label=names[int(cls)],
                        )

                _, buffer = cv2.imencode(".jpg", im0)
                frame = buffer.tobytes()
                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )

            frame_counter += 1


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@socketio.on("start_video")
def start_video():
    global video_running
    video_running = True


@socketio.on("stop_video")
def stop_video():
    global video_running, frame_counter
    video_running = False
    frame_counter = 0


if __name__ == "__main__":
    socketio.run(app, debug=True)
