#import oracledb
import mysql.connector
import os
import pandas as pd
from os.path import dirname, abspath
from roboflow import Roboflow
import time
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.ttk import *
from tkinter import _setit
from tkinter import filedialog
import tkinter.font as tkfont

def main():
    global model, typeHyphenCount, typeNoHyphenCount, typeIMGCount, typeUnknownCount, total, c, threshold

    # Set confidence threshold for contrail detection
    threshold = 40

    # MySQL Connection
    conn = mysql.connector.connect(host="mysql-db.cxau2zpfepp1.us-east-1.rds.amazonaws.com", user="admin", password="contrails1234", database='CONTRAILS')
    c = conn.cursor()
    print("Connection to MySQL Database Instance on RDS Successful.")
    c.execute("SELECT IMAGE_FILENAME FROM CONTRAILS.IMAGE_CONTRAIL_DATA")

    filename_list = []

    for i in c:
        filename_list.append(i[0])

    # Load Roboflow Models
    rf = Roboflow(api_key="zRb8LZg63cFvJMrp0GyO")
    #project1 = rf.workspace().project("contrails-multi-class")
    project = rf.workspace().project("contrails-50-50-object-det.")
    #model1 = project1.version(7).model
    model = project.version(2).model

    # Define directory with source sky images for detection
    directory = 'Sky Images for Prediction'

    typeHyphenCount = 0
    typeNoHyphenCount = 0
    typeIMGCount = 0
    typeUnknownCount = 0
    total = 0

    #Open New GUI window with dimensions w, h and open in center of screen
    global window
    window = Tk()
    w = 470
    h = 110
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    window.title("Contrail Detection Tool")

    def clicked_predict_new():
        user_input = simpledialog.askstring("Contrail Detection Confidence Threshold", "Enter a whole number 1-99 for the model confidence threshold. A higher number will detect fewer contrails. A lower number will detect more but may result in more false positive detections:")
        try:
            threshold = int(user_input)
            if threshold < 1 or threshold > 99:
                messagebox.showinfo("Error","Threshold must be between 1 and 99. Please try again.")
                return
        except:
            messagebox.showinfo("Error",'Threshold must be a whole number between 1 and 99. Please try again.')
            return

        print("Now predicting all NEW image files in directory...")
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            print(filename)
            print(f)

            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                if filename not in filename_list:
                    try:
                        predict_image(f, filename)
                    except:
                        print("There was an error when predicting file " + filename + " and it will be skipped.")
            else:
                print("A non-jpeg file was found in the source folder. Currently, only .jpg or .jpeg images are accepted for prediction.")
        print("Predictions complete.")
            
    def clicked_predict_all():
        user_input = simpledialog.askstring("Contrail Detection Confidence Threshold", "Enter a whole number 1-99 for the model confidence threshold. A higher number will detect fewer contrails. A lower number will detect more but may result in more false positive detections:")
        try:
            threshold = int(user_input)
            if threshold < 1 or threshold > 99:
                messagebox.showinfo("Error","Threshold must be between 1 and 99. Please try again.")
                return
        except:
            messagebox.showinfo("Error",'Threshold must be a whole number between 1 and 99. Please try again.')
            return

        print("Now predicting all image files in directory...")
        c.execute("TRUNCATE TABLE CONTRAILS.IMAGE_CONTRAIL_DATA")
        c.execute("COMMIT")

        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            print(filename)
            print(f)

            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                try:
                    predict_image(f, filename)
                except:
                    print("There was an error when predicting file " + filename + " and it will be skipped.")
            else:
                print("A non-jpeg file was found in the source folder. Currently, only .jpg or .jpeg images are accepted for prediction.")
        print("Predictions complete.")

    def clicked_delete_all():
        c.execute("TRUNCATE TABLE CONTRAILS.IMAGE_CONTRAIL_DATA")
        c.execute("COMMIT")
        print("All current prediction data successfully deleted from database.")

    def clicked_export():
        df = pd.read_sql("SELECT * FROM CONTRAILS.IMAGE_CONTRAIL_DATA", conn)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        df.to_excel("Contrail Prediction Exports/Export_" + timestamp + ".xlsx")
        print("Excel export successful and save as Contrail Prediction Exports/Export_" + timestamp + ".xlsx")

    #Add form elements and define commands
    label = Label(window, text="   Predict and Log New Image Files Only:   ")
    label.grid(column=1, row=1, sticky=W)

    btn = Button(window, text="Predict New Files", command=clicked_predict_new)
    btn.grid(column=2, row=1, sticky=E)

    label = Label(window, text="   Predict and Log ALL Image Files (will delete previous records):   ")
    label.grid(column=1, row=2, sticky=W)

    btn = Button(window, text="Predict All Files", command=clicked_predict_all)
    btn.grid(column=2, row=2, sticky=E)

    label = Label(window, text="   Delete All Image Predictions from Database:   ")
    label.grid(column=1, row=3, sticky=W)

    btn = Button(window, text="Delete Predictions", command=clicked_delete_all)
    btn.grid(column=2, row=3, sticky=E)

    label = Label(window, text="   Export Current Predictions to Excel File:   ")
    label.grid(column=1, row=4, sticky=W)

    btn = Button(window, text="Export", command=clicked_export)
    btn.grid(column=2, row=4, sticky=E)

    

    window.mainloop()

def count_object_occurrences(predictions, target_class):
    object_count = 0
    for prediction in predictions:
        if prediction['class'] in target_class:
            object_count += 1
    return object_count

def predict_image(f, filename):
    global typeHyphenCount, typeNoHyphenCount, typeIMGCount, typeUnknownCount, total
    #cirrus_confidence = 0
    #longlived_confidence = 0
    cirrus_ind = 0
    longlived_ind = 0
    contrail_ind = 0
    #image_width = 0
    #image_height = 0
    city = "Fairfax"
    state = "VA"
    country = "USA"
    zip = "22030"

    total = total + 1
    if filename[4] == "-":
        type = "hyphenated"
        typeHyphenCount = typeHyphenCount + 1
    elif filename[4] in ("0","1"):
        type = "not_hyphenated"
        typeNoHyphenCount = typeNoHyphenCount + 1
    elif filename[0:3] == "IMG":
        type = "IMG"
        typeIMGCount = typeIMGCount + 1
    else:
        type = "unknown"
        typeUnknownCount = typeUnknownCount + 1

    if type == "hyphenated":
        year = int(filename[0:4])
        month = int(filename[5:7])
        day = int(filename[8:10])
        hour = int(filename[11:13])
        key = filename[0:4] + filename[5:7] + filename[8:10] + "_" + filename[11:13]
    elif type == "not_hyphenated":
        year = int(filename[0:4])
        month = int(filename[4:6])
        day = int(filename[6:8])
        hour = int(filename[9:11])
        key = filename[0:11]
    elif type == "IMG":
        year = int(filename[4:8])
        month = int(filename[8:10])
        day = int(filename[10:12])
        hour = int(filename[13:15])
        key = filename[4:15]
    else:
        print("Could not get date and time from file " + filename + ". Unrecognized format.")
        year = 'NULL'
        month = 'NULL'
        day = 'NULL'
        hour = 'NULL'
        key = 'UNKNOWN'

    start = datetime.now()
    ## Detect image with model 1
    ##print(model.predict(filename, confidence=40, overlap=30).json())
    #print("Model 1 Predictions")
    #predictions1 = model1.predict(f)
    #print(predictions1)
    #time = predictions1[0]['time']
    #image_width = int(predictions1[0]['image']['width'])
    #image_height = int(predictions1[0]['image']['height'])
    #cirrus_confidence = float(predictions1[0]['predictions']['Cirrus']['confidence'])
    #longlived_confidence = float(predictions1[0]['predictions']['LongLived']['confidence'])

    # Detect image with model
    print("Model Predictions")
    predictions = model.predict(f, confidence=threshold, overlap=30)
    print(predictions)
    cirrus_count = count_object_occurrences(predictions, 'Cirrus')
    longlived_count = count_object_occurrences(predictions, 'LongLived')
    total_contrail_count = cirrus_count + longlived_count

    print("Cirrus Count: " + str(cirrus_count))
    print("LongLived Count: " + str(longlived_count))

    if cirrus_count > 0:
        cirrus_ind = 1
    else:
        cirrus_ind = 0

    if longlived_count > 0:
        longlived_ind = 1
    else:
        longlived_ind = 0

    if cirrus_ind + longlived_ind > 0:
        contrail_ind = 1
    else:
        contrail_ind = 0

    # save out image with predicted contrails only on images which have contrails found
    if contrail_ind == 1:
        if total_contrail_count == 1:
            model.predict(f, confidence=40, overlap=30).save("Predicted Sky Images/1 Contrail/predict_" + filename)
        elif total_contrail_count == 2:
            model.predict(f, confidence=40, overlap=30).save("Predicted Sky Images/2 Contrails/predict_" + filename)
        elif total_contrail_count == 3:
            model.predict(f, confidence=40, overlap=30).save("Predicted Sky Images/3 Contrails/predict_" + filename)
        elif total_contrail_count == 4:
            model.predict(f, confidence=40, overlap=30).save("Predicted Sky Images/4 Contrails/predict_" + filename)
        elif total_contrail_count == 5:
            model.predict(f, confidence=40, overlap=30).save("Predicted Sky Images/5 Contrails/predict_" + filename)
        elif total_contrail_count == 6:
            model.predict(f, confidence=40, overlap=30).save("Predicted Sky Images/6 Contrails/predict_" + filename)
        elif total_contrail_count > 6:
            model.predict(f, confidence=40, overlap=30).save("Predicted Sky Images/More Than 6 Contrails/predict_" + filename)

    end = datetime.now()
    prediction_time = (end - start).total_seconds()

    # Log results in MySQL DB Instance on RDS
    sql = '''INSERT INTO IMAGE_CONTRAIL_DATA
                (IMAGE_FILENAME,
                WEATHER_DATETIME_ID,
                YEAR,
                MONTH,
                DAY,
                HOUR,
                CITY,
                STATE,
                COUNTRY,
                ZIP,
                CIRRUS_CONTRAIL_CT,
                CIRRUS_CONTRAIL_IND,
                LONG_LIVED_CONTRAIL_CT,
                LONG_LIVED_CONTRAIL_IND,
                CONTRAIL_IND,
                PREDICTION_TIME)
                VALUES
                (\'''' + filename + '''\',
                \'''' + key + '''\',
                ''' + str(year) + ''',
                ''' + str(month) + ''',
                ''' + str(day) + ''',
                ''' + str(hour) + ''',
                \'''' + city + '''\',
                \'''' + state + '''\',
                \'''' + country + '''\',
                \'''' + zip + '''\',
                ''' + str(cirrus_count) + ''',
                ''' + str(cirrus_ind) + ''',
                ''' + str(longlived_count) + ''',
                ''' + str(longlived_ind) + ''',
                ''' + str(contrail_ind) + ''',
                ''' + str(prediction_time) + ''')'''

    c.execute(sql)
    c.execute("COMMIT")


if __name__ == "__main__":
    main()