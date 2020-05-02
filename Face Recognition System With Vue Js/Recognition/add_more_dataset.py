import psycopg2
import face_recognition as fr
import os
import cv2
import time



try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "face_recognition_api")

    cursor = connection.cursor()
    TABLE_NAME = "report_dataset"
    COL_REPORT_ID = "report_id"
    COL_NAME = "report_name"

    def take_photo(dataset_name):
        time.sleep(5)
        camera = cv2.VideoCapture(0)
        return_value, image_frame = camera.read()
        cv2.imwrite("CameraImage/" + dataset_name + ".jpg", image_frame)
        # Stop video
        camera.release()
        cv2.destroyAllWindows()
        try:
            args_image = 'CameraImage/' + dataset_name + '.jpg'
            print(args_image)
            image = cv2.imread(args_image)
            faces_cnn = face_recognition.face_locations(image)
            for top, right, bottom, left in faces_cnn:
                x = left
                y = top
                w = right - x
                h = bottom - y

                    # side of Face for cropping
                crop_ima = image[y:y + h, x:x + w]
                    # save image face
                cv2.imwrite("FaceCrop/" + dataset_name + '.jpg', crop_ima)
                             
                ENCODE = face_recognition.face_encodings(crop_ima)
                insert_data(dataset_name,ENCODE)
                return True
        except:
            return False

    #add more dataset
    def insert_data(name,encoding):
        report_id = 234   
        insert = f"insert into {TABLE_NAME} ({COL_REPORT_ID},{COL_NAME}) values({report_id},'{name}')"
        cursor.execute(insert) 
        connection.commit()      
        j=1
        for i in encoding:
            COLUMN = "point" + str(j)
            insert1 = f"update {TABLE_NAME} set {COLUMN} = {i} where {COL_NAME} = '{name}' "             
            cursor.execute(insert1)
            connection.commit()
            j +=1      

    #The Program start here
    while True:
        name = input("Enter Your Name:")
        TakePhoto = take_photo(name)
        if TakePhoto == True:
            print('Insert Dataset Successfully....')
        else:
            print('Can not read the image.....')
        chooice = input('Do you want to Continue adding more dataset? Y/N')
        if chooice == 'N':
            break

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
