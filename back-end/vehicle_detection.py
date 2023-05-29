# Load YOLOv8n, train it on COCO128 for 3 epochs and predict an image with it
import cv2
# model.train(data='coco128.yaml', epochs=3)  # train the model

def object_detection(image,model,names):
    results = model.predict(image, device='cpu')  # predict on an image
    print("length of results : ", len(results))
    for result in results:
      print("length of cls : ",len(result.boxes.cls))
      print("length of results boxes : ",len(result.boxes))
      for res_class,res_boundingbox in zip(result.boxes.cls,result.boxes):
          x1=res_boundingbox.xyxy[0].cpu().numpy()[0]
          y1=res_boundingbox.xyxy[0].cpu().numpy()[1]
          x2=res_boundingbox.xyxy[0].cpu().numpy()[2]
          y2=res_boundingbox.xyxy[0].cpu().numpy()[3]
          cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            # Put label and score on the bounding box
          text = f"{names[int(res_class)]}: {res_boundingbox.conf[0].cpu().numpy():.2f}"
          cv2.putText(image, text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image