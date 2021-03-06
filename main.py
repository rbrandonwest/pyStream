# main.py

from flask import Blueprint, render_template, send_file, Response
from flask_login import login_required, current_user
import cv2

main = Blueprint('main', __name__)
camera = cv2.VideoCapture(0)


def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/download')
def downloadFile():
    path = "C:/Users/Brandon/PycharmProjects/flaskProject\project/files/testNote.txt"
    return send_file(path, as_attachment=True)


@main.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
