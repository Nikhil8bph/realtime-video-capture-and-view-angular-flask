from flask import Flask, request, jsonify
import base64
import cv2
from flask_cors import CORS
import numpy as np
import utils
import vehicle_detection
# from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)

# Load YOLOv4-tiny model
net = cv2.dnn.readNet("data/yolov4-tiny.weights", "data/yolov4-tiny.cfg")

# Load class names
with open("data/coco.names", "r") as f:
    classes = f.read().splitlines()

@app.route('/process_frame', methods=['POST'])
def process_frame():
    frame_data = request.get_data()
    image = utils.convertBase64ToImage(frame_data)
    # imageProcessed = vehicle_detection.get_vehicles(image,net,classes)
    response = {
        'message': utils.convertImageToBase64(image)
    } 
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)