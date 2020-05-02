import face_recognition
import os
import psycopg2
import math
import cv2
import numpy as np

TABLE_NAME = "report_dataset"
try:
    # create the connection into the postgresql 
    connection1 = psycopg2.connect(user = "postgres",
                                  password = "1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "face_recognition_api")

    cursor = connection1.cursor()
    img_path ="img_1.jpg"
    # img = cv2.imread(img_path)
    # load = face_r  ecognition.face_locations(img)
    # for top, right, bottom, left in load:
    #     x = left
    #     y = top
    #     w = right - x
    #     h = bottom - y
    #     crop_ima = img[y:y + h, x:x + w]
    #     try:             
    #         ENCODE = face_recognition.face_encodings(crop_ima)[0]
    #     except:
    #         pass
    load = face_recognition.load_image_file(img_path)
    ENCODE = face_recognition.face_encodings(load)[0]
       

    query = f'select * from {TABLE_NAME}'
    cursor.execute(query)
    records = cursor.fetchall()
    for encode in records:
        i = 0  
        dist = 0
        for data in range(2,130):
            dist += pow((ENCODE[i] - encode[data]),2)
            i += 1
        result = math.sqrt(dist)
        print(result)
        if result < 0.44:
            print(encode[1])
        # else:
        #     print('No matching....')
   

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection1):
            cursor.close()
            connection1.close()
            print("PostgreSQL connection is closed")
        