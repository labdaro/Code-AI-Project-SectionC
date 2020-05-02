import cv2
import time
import json
import pika
import numpy as np
import sys
import face_recognition

def publish_data(encoding):
    print(encoding)
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='face_recognition_api', durable=True)
    res = encoding.tolist()
    channel.basic_publish(
        exchange='',
        routing_key='face_recognition_api',
        body=json.dumps(res),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    connection.close()
    
def cropFace():

    args_image = 'image/img_' + str(1) + '.jpg'
    image = cv2.imread(args_image)

        # if image is not a file move to next
    if image is None:
        print("Could not read input image")


        # apply face detection (cnn)
    try:

        faces_cnn = face_recognition.face_locations(image)
        for top, right, bottom, left in faces_cnn:
            x = left
            y = top
            w = right - x
            h = bottom - y

                # side of Face for cropping
            crop_ima = image[y:y + h, x:x + w]
                # save image face
            cv2.imwrite("face_128D/User_" + str(1) + '.jpg', crop_ima)
            try:             
                ENCODE = face_recognition.face_encodings(crop_ima)
                if ENCODE:
                    
                    publish_data(ENCODE[0])
                    
            except:
                pass

    except Exception as e:
        print ("Can not crop the image.....")

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)
    return_value, image_frame = camera.read()
    cv2.imwrite("image/img_" + str(1) + ".jpg", image_frame)
    # Stop video
    camera.release()
    # Close all started windows
    cv2.destroyAllWindows()

    print("Finish Save frame from Camera.")
    time.sleep(5)

    print("Start crop Face in image.")
    # Function call crop
    cropFace()  # number of user that can crop Face to return
    # time.sleep(5)

    # # encode 128-d from image crop of users.
    # encode_face(user_id)
