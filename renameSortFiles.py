from datetime import datetime
import re
import openpyxl
from openpyxl import load_workbook
import numbers
import pandas as pd
import numpy as np
import os
from os.path import dirname, abspath
import sys
import shutil

directory = os.fsencode("c:/capstone/sky images/")

d = dirname(dirname(dirname(abspath(__file__))))

dataFilePath = d + "\data\SkyImageTrainingLabels.xlsx"

wb = load_workbook(dataFilePath)
sheet = wb["Sheet1"]

data = sheet.values
columns = next(data) [0:]
df = pd.DataFrame(data, columns=columns)

df_dict = df.to_dict('records')

typeHyphenCount = 0
typeNoHyphenCount = 0
typeIMGCount = 0
typeUnknownCount = 0
total = 0
matches = 0

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    fullPath = "c:/capstone/sky images/" + filename

    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
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
        key = filename[0:4] + filename[5:7] + filename[8:10] + "_" + filename[11:13]
    elif type == "not_hyphenated":
        key = filename[0:11]
    elif type == "IMG":
        key = filename[4:15]
    else:
        key = None

    print(filename)
    print(key)

    for row in df_dict:
        if row['KEY'] == key:
            matches = matches + 1
            # Copy the file to image quality classification class folders
            if row['POOR_IMAGE_IND'] == 1 and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/image quality classification images/poor quality/" + filename
            elif pd.isnull(row['POOR_IMAGE_IND']) and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/image quality classification images/good quality/" + filename
            try:
                shutil.copyfile(fullPath, newFullPath)
            except:
                pass

            # Copy the file to long lived contrails classification class folders
            if row['LONG_LIVED_CONTRAIL_CT'] == 0 and row['EXCLUDE_IND'] != 1 and row['POOR_IMAGE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/long lived contrails classification images/0 Long Lived Contrails/" + filename
            elif row['LONG_LIVED_CONTRAIL_CT'] == 1 and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/long lived contrails classification images/1 Long Lived Contrail/" + filename
            elif row['LONG_LIVED_CONTRAIL_CT'] == 2 and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/long lived contrails classification images/2 Long Lived Contrails/" + filename
            elif row['LONG_LIVED_CONTRAIL_CT'] == 3 and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/long lived contrails classification images/3 Long Lived Contrails/" + filename
            elif row['LONG_LIVED_CONTRAIL_CT'] == 4 and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/long lived contrails classification images/4 Long Lived Contrails/" + filename
            elif row['LONG_LIVED_CONTRAIL_CT'] == 5 and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/long lived contrails classification images/5 Long Lived Contrails/" + filename
            try:
                shutil.copyfile(fullPath, newFullPath)
            except:
                pass

            # Copy the file to cirrus contrails classification class folders
            if row['CIRRUS_CONTRAIL_CT'] == 0 and row['EXCLUDE_IND'] != 1 and row['POOR_IMAGE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/cirrus contrails classification images/0 Cirrus Contrails/" + filename
            if row['CIRRUS_CONTRAIL_CT'] == 1 and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/cirrus contrails classification images/1 Cirrus Contrail/" + filename
            if row['CIRRUS_CONTRAIL_CT'] == 2 and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/cirrus contrails classification images/2 Cirrus Contrails/" + filename
            if row['CIRRUS_CONTRAIL_CT'] == 3 and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/cirrus contrails classification images/3 Cirrus Contrails/" + filename
            if row['CIRRUS_CONTRAIL_CT'] == 4 and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/cirrus contrails classification images/4 Cirrus Contrails/" + filename
            if row['CIRRUS_CONTRAIL_CT'] == 5 and row['EXCLUDE_IND'] != 1:
                newFullPath = "c:/capstone/sky images/cirrus contrails classification images/5 Cirrus Contrails/" + filename
            try:
                shutil.copyfile(fullPath, newFullPath)
            except:
                pass

print("Number of images matched with training data: " + str(matches))
print("Number of hyphenated files: " + str(typeHyphenCount))
print("Number of non-hyphenated files: " + str(typeNoHyphenCount))
print("Number of IMG type files: " + str(typeIMGCount))
print("Number of Unknown type files: " + str(typeUnknownCount))
print("Total number of jpeg-jpg files found: " + str(total))
