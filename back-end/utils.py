import os 
import base64
import cv2
import numpy as np

def createTempDirectory():
    # Leaf directory 
    directory = "temp"
    # Parent Directories 
    parent_dir = os.getcwd()
    # Path 
    path = os.path.join(parent_dir, directory) 
    if(os.path.exists(path)==False):
        os.mkdir(path)
        print("Directory '% s' created" % directory)

def convertBase64ToImage(frame_data):
    image_data = frame_data.decode('utf-8').replace('data:image/jpeg;base64,', '')
    # Decode the base64 string to bytes
    image_bytes = base64.b64decode(image_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

def convertImageToBase64(image):
    # Encode the image as a base64 string
    retval, buffer = cv2.imencode('.jpg', image)
    bytes_image = base64.b64encode(buffer)
    base64_image = "data:image/jpeg;base64,"+str(bytes_image.decode('utf-8'))
    return base64_image