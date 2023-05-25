from flask import Flask, request, jsonify
import base64
import cv2
from flask_cors import CORS
import numpy as np
# from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
# socketio = SocketIO(app,cors_allowed_origins="*")

@app.route('/process_frame', methods=['POST'])
def process_frame():
    frame_data = request.get_data()
    # print(frame_data)
    # image_data = frame_data.replace('data:image/jpeg;base64,', '')
    image_data = frame_data.decode('utf-8').replace('data:image/jpeg;base64,', '')
    
    # Decode the base64 string to bytes
    image_bytes = base64.b64decode(image_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # cv2.imshow("Vehicle Detection", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Encode the image as a base64 string
    retval, buffer = cv2.imencode('.jpg', image)
    bytes_image = base64.b64encode(buffer)
    base64_image = bytes_image.decode('utf-8')

    response = {
        # 'message': str(frame_data.decode('utf-8'))
        'message': "data:image/jpeg;base64,"+str(base64_image)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)