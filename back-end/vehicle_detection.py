import cv2
import numpy as np
import math

def get_vehicles(image,net,classes):
    # Set input size and scale
    input_size = (416, 416)
    scale = 1 / 255.0
    # Preprocess image
    blob = cv2.dnn.blobFromImage(image, scale, input_size, (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Run inference
    try:
        output_layers = net.getUnconnectedOutLayersNames()
        outputs = net.forward(output_layers)
    except cv2.error as e:
        print("Error running inference:")
        print(e)
        exit(1)

    # Process detections
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if not math.isnan(confidence) and math.isfinite(confidence) and confidence > 0.5 and classes[class_id] == "person":
                center_x = int(detection[0] * image.shape[1])
                center_y = int(detection[1] * image.shape[0])
                width = int(detection[2] * image.shape[1])
                height = int(detection[3] * image.shape[0])

                x = int(center_x - width / 2)
                y = int(center_y - height / 2)

                # Draw bounding box
                cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
                label = f"{classes[class_id]}: {confidence:.2f}"
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display result
    # cv2.imshow("Vehicle Detection", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return image





