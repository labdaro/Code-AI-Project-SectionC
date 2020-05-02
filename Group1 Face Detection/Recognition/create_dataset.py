import psycopg2
import face_recognition as fr
import os
import cv2


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

    # create column only ID and NAME 
    def create_table():
       create = f"create table {TABLE_NAME} ({COL_REPORT_ID} int,{COL_NAME} varchar(50))"
       cursor.execute(create)
       connection.commit()
       return "sucessfully to create table"

    #add 128 column 
    def add_128Col():
        for i in range(1,129):
            COLUMN = "point" + str(i)
            add = f"alter table {TABLE_NAME} add column {COLUMN} float(50)" 
            cursor.execute(add)
            connection.commit()
        return "sucessfully to create 128 column"

    # Insert data into Column Name,Id,point128
    def insert_data():
        path = "dataset"
        report_id = 1021
        for dataset_img in os.listdir(path):
            insert = f"insert into {TABLE_NAME} ({COL_REPORT_ID},{COL_NAME}) values({report_id},'{dataset_img[:-4]}')"
            cursor.execute(insert) 
            connection.commit()      

            img = cv2.imread("dataset/"+dataset_img)
            load = fr.face_locations(img)
            for top, right, bottom, left in load:
                x = left
                y = top
                w = right - x
                h = bottom - y
                crop_ima = img[y:y + h, x:x + w]
                try:
                    ENCODE = fr.face_encodings(crop_ima)[0]
                    print(ENCODE)
                    j=1
                    for i in ENCODE:
                        COLUMN = "point" + str(j)
                        insert1 = f"update {TABLE_NAME} set {COLUMN} = {i} where {COL_NAME} = '{dataset_img[:-4]}' "             
                        cursor.execute(insert1)
                        connection.commit()
                        j +=1
                    print(dataset_img)
                except:
                    pass
                
        return "add already"

    

    Table_Create =  create_table()
    print(Table_Create)
    more_column = add_128Col()
    print(more_column)    


    add_data = insert_data()
    print(add_data)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
