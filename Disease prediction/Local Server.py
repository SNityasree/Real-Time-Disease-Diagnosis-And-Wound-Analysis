import os
import urllib.request
import http
import pandas as pd
import re
from time import sleep
from datetime import datetime

base = "http://192.168.137.167/" # change the id based on device

def transfer(my_url):   #use to send and receive data
    try:
        n = urllib.request.urlopen(base + my_url).read()
        n = n.decode("utf-8")
        return n
    except http.client.HTTPException as e:
        return e

# Specify the absolute path for the Excel file
excel_file_path = r"C:\Users\Hxtreme\Documents\Arduino\Multiplediseases_sweat_2025\sensor_data.xlsx"

# Create an empty list to store data
data_list = []

# Create a function to split and save data to Excel
def save_to_excel(te, bpm, spo2, ppg,ph):
    data_list.append([te, bpm, spo2, ppg,ph])
    df = pd.DataFrame(data_list, columns=['BPM', 'SPO2', 'TE', 'PPG','PH'])
    df.to_excel(excel_file_path, index=False)

ct = 0
while True:
    res = transfer(str(ct))
    response = str(res)
    print(response)
    
    # Split the received data
    values = response.split(',')
    if len(values) == 5:
        te, bpm, spo2, ppg,ph = values
        save_to_excel(te, bpm, spo2, ppg,ph)
    
    sleep(1)

