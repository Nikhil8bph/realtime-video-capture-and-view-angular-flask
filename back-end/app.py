from flask import Flask, request, jsonify
import base64
import cv2
from flask_cors import CORS
import numpy as np
import utils
import vehicle_detection
from ultralytics import YOLO
# from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)

model = YOLO('yolov8s.pt')  # load a pretrained YOLOv8n detection model
names = model.names

@app.route('/process_frame', methods=['POST'])
def process_frame():
    frame_data = request.get_data()
    image = utils.convertBase64ToImage(frame_data)
    imageProcessed = vehicle_detection.get_vehicles(image,model,names)
    response = {
        'message': utils.convertImageToBase64(image)
    } 
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)