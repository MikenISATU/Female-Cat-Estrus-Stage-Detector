import numpy as np
from werkzeug.utils import secure_filename
import os
import cv2
from ultralytics import YOLO
import random
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov', 'mkv'}

# Load the YOLOv8 model for cat detection
yolov8_model_cat = YOLO('Models/M1YoloV8.pt')

# Load the YOLOv8 model for in-heat detection
yolov8_model_in_heat = YOLO('Models/M2YoloV8withNon_inheat.pt')

@app.route('/get_analysis_progress')
def get_analysis_progress():
    # Simulate progress for demonstration purposes
    progress = random.randint(0, 100)

    # Return progress as JSON to update the frontend
    return jsonify(progress=progress)

@app.route('/')
def index():
    return render_template('index.html', css_file='style.css')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'video' not in request.files:
            return render_template('Cerror.html', css_file=url_for('static', filename='Cerror.css'))

        video = request.files['video']

        if video.filename == '':
            return redirect(request.url)

        if video and allowed_file(video.filename):
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(video.filename))
            video.save(video_path)

            cap = cv2.VideoCapture(video_path)

            # Inside the loop where frames are processed for the first model
            cat_detected_frames = 0  # Counter for cat detection

            while True:
                ret, frame = cap.read()
                if frame is None:
                    break  # Break the loop when no more frames are available

                # Resize the frame to a smaller size (e.g., 400x400)
                frame_small = cv2.resize(frame, (400, 400))

                # MODEL 1 for cat detection
                results_cat = yolov8_model_cat.predict(source=frame_small, show=True, conf=0.5)

                # Print results to inspect structure
                for results_cat_instance in results_cat:
                    # Access bounding box coordinates
                    boxes = results_cat_instance.boxes

                    # CONFIDENCE 0.5
                    if len(boxes) > 0 and 'cat' in results_cat_instance.names[0]:
                        # Count the number of frames where "cat" is detected
                        cat_detected_frames += 1
                    print(f"Cat Frame - Total: {cat_detected_frames}")

                # BREAK the loop if at least 50 cat frames are detected
                if cat_detected_frames >= 50:
                    break

            # Release resources for the first model
            cap.release()

            # Check if there are at least 50 cat detections
            if cat_detected_frames >= 50:
                # Process the video with the second model
                result = process_video_with_second_model(video_path)

                # Render templates based on the result
                if result == 'inheat':
                    return render_template('medcatvad.html', css_file=url_for('static', filename='inheat.css'))
                elif result == 'non-inheat':
                    return render_template('no.html', css_file=url_for('static', filename='noninheat.css'))

            # If less than 50 cat detections, render 'catnotdetected.html'
            else:
                return render_template('catnotdetected.html', css_file=url_for('static', filename='Cerror.css'))

        else:
            return render_template('Cerror.html', css_file=url_for('static', filename='Cerror.css'))

    # Handle GET request (when the user initially visits the page)
    return render_template('Upload.html', css_file=url_for('static', filename='uploads.css'))

def process_video_with_second_model(video_path):
    cap = cv2.VideoCapture(video_path)
    in_heat_frames = 0
    non_inheat_frames = 0

    while True:
        ret, frame = cap.read()
        if frame is None:
            break  # Break the loop when no more frames are available

        # Resize the frame to a smaller size (e.g., 400x400)
        frame_small = cv2.resize(frame, (400, 400))

        # MODEL 2 for in-heat detection
        results_in_heat = yolov8_model_in_heat.predict(source=frame_small, show=True, conf=0.5)

        # Print results to inspect structure
        for results_in_heat_instance in results_in_heat:
            # Access bounding box coordinates
            boxes = results_in_heat_instance.boxes

            # CONFIDENCE 0.2
            if len(boxes) > 0:
                # Iterate through the boxes to get the class name for each detected object
                for box in boxes:
                    predicted_class_index = int(box.cls.item())
                    predicted_class_name = results_in_heat_instance.names[predicted_class_index]
                    print(f"Detected class: {predicted_class_name}")

                    if predicted_class_name == 'inheat':
                        # Increment the count for in-heat frames
                        in_heat_frames += 1
                        print(f"Inheat Frame - Total: {in_heat_frames}")
                    elif predicted_class_name == 'non-inheat':
                        # Increment the count for non-inheat frames
                        non_inheat_frames += 1
                        print(f"Non-Inheat Frame - Total: {non_inheat_frames}")

        # BREAK the loop if at least 50 in-heat or non-inheat frames are detected
        if in_heat_frames >= 50 or non_inheat_frames >= 50:
            break

    # Release resources for the second model
    cap.release()

    # Check if there are at least 50 in-heat or non-inheat detections
    if in_heat_frames > non_inheat_frames:
        return 'inheat'
    elif non_inheat_frames > in_heat_frames:
        return 'non-inheat'



# If video file is not present render this error
@app.route('/render_cerror')
def render_cerror():
    return render_template('FilenotFound.html', css_file=url_for('static', filename='FNF.css'))

# Handle user feedback
@app.route('/yes')
def yes():
    return render_template('yes.html', css_file=url_for('static', filename='yes.css'))

@app.route('/no')
def no():
    return render_template('no.html', css_file=url_for('static', filename='no.css'))

@app.route('/yes1')
def yes1():
    return render_template('no.html', css_file=url_for('static', filename='userfeedback.css'))

@app.route('/no2')
def no2():
    return render_template('userfeedbackwindow.html', css_file=url_for('static', filename='no.css'))

# Handle user feedback
@app.route('/About Us')
def about_us():
    return render_template('AboutUs.html', css_file=url_for('static', filename='abouts.css'))

@app.route('/Acknowledgement')
def acknowledgement():
    return render_template('Acknowledgement.html', css_file=url_for('static', filename='acknowledgement.css'))

@app.route('/Help')
def helps():
    return render_template('Help.html', css_file=url_for('static', filename='help.css'))

if __name__ == '__main__':
    app.run(debug=True)
