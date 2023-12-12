# Import necessary modules
from flask import Flask, render_template, request, jsonify, send_file, Response
from werkzeug.utils import secure_filename
import os
import cv2
from ultralytics import YOLO
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import base64

# Initialize Flask app
app = Flask(__name__)

# Configuration for file upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv'}

# Load the YOLOv8 model for detection
yolov8_model = YOLO('Models/M1YoloV8.pt')

# Function to check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to handle video upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return render_template('Cerror.html', css_file=url_for('static', filename='Cerror.css'))

    video = request.files['video']

    if video.filename == '':
        return redirect(request.url)

    if video and allowed_file(video.filename):
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(video.filename))
        video.save(video_path)

        return render_template('Upload1.html', video_path=video_path, css_file=url_for('static', filename='uploads.css'))
    else:
        return render_template('Cerror.html', css_file=url_for('static', filename='Cerror.css'))

# Route to handle real-time detection
@app.route('/video_feed')
def video_feed():
    video_path = request.args.get('video_path', 0, type=str)
    return Response(process_video(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to process video frames and perform YOLOv8 detection
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform YOLOv8 detection on the frame
        results = yolov8_model.predict(frame)

        # Draw bounding boxes on the frame
        for result in results:
            frame = result.render()[0]

        # Convert the frame to JPEG format
        _, jpeg = cv2.imencode('.jpg', frame)

        # Yield the frame as bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    cap.release()

# Route to render the upload form
@app.route('/')
def index():
    return render_template('Upload1.html', css_file=url_for('static', filename='style.css'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
