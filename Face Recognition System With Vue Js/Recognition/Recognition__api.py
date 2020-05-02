import psycopg2
import face_recognition
import math
import os
import pika
import json
import datetime
import numpy as np 
try:
    #Create the connection into the Rabbitmq
    # creddentail = pika.PlainCredentials('lyhov', '123456')
    # connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='10.1.33.186', port=5672, virtual_host='/', credentials=creddentail))
    # channel = connection.channel()
    # channel.queue_declare(queue='abc', durable=True)
    

    # Demo the local 
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel() 
    channel.queue_declare(queue='face_recognition_api', durable=True)

    # create the connection into the postgresql 
    connection1 = psycopg2.connect(user = "postgres",
                                  password = "1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "face_recognition_api")

    cursor = connection1.cursor()

    #Dataset from the database
    TABLE_NAME = "report_dataset"
    TABLE_REPORT = "report"
   

    def callback(ch, method,properties, body):
        #Get the current time 
        dateTimeObj = datetime.datetime.now()
        date = dateTimeObj.strftime("%A-%d-%B-%Y")
        time = dateTimeObj.strftime("%I:%M %p")  
        try:
            #Recieve the data from queue and convert into the numpy
            recieveData = json.loads(body)
            numpyArray =np.array(recieveData)
            convertString = numpyArray.tostring()
            ENCODE = np.fromstring(convertString, dtype=float)
            query = f'select * from {TABLE_NAME}'
            cursor.execute(query)
            records = cursor.fetchall()
            for encode in records:
                i = 0  
                dist = 0
                #checking for one people face
                for data in range(2,130):
                    dist += pow((ENCODE[i] - encode[data]),2)
                    i += 1
                result = math.sqrt(dist)
                print(result)
                if result < 0.459:
                    name = encode[1]
                    print(name)
                    id = encode[0]
                    insert_report = f"insert into {TABLE_REPORT}(report_id,fullname,report_time,report_date) values({id},'{name}','{time}','{date}')"
                    cursor.execute(insert_report)
                    connection1.commit()
                else:
                    print("Have no Matching.... ")
         
                

                
                
                        
            
            # channel.stop_consuming()
            print("----------------------------------------------------------")
            # print(LIST_NAME_PRESENT)     
                                         

        except Exception as e: 
            print(e)
            
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)



    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='face_recognition_api', on_message_callback=callback)
    channel.start_consuming()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection1):
            cursor.close()
            connection1.close()
            print("PostgreSQL connection is closed")


    









