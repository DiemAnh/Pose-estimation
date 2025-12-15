import serial
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import csv
from datetime import datetime

ts = time.time()

now = datetime.now()
date_time = now.strftime("%d-%m-%Y, %H:%M:%S")
cred = credentials.Certificate("bmedesign.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://bmedesign-eeglab-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('/')

Dataserial = serial.Serial('/dev/cu.usbserial-1120', 115200)
print(Dataserial)
time.sleep(1)
while True:
    try:
        #while Dataserial.inWaiting() == 0:
        #    pass
        data = Dataserial.readline()
        data = str(data, 'utf-8')
        data = data.strip('\r\n')

        x = data.split(",")
        temp = {
            'temp': x[-1],
            'timestamp':{".sv": "timestamp"},
        }
        ref.child('Station 3 - Arduino Uno/').child('Acceleration X - Arduino Uno').child(date_time).push(x[0])
        ref.child('Station 3 - Arduino Uno/').child('Acceleration Y - Arduino Uno').child(date_time).push(x[1])
        ref.child('Station 3 - Arduino Uno/').child('Acceleration Z - Arduino Uno').child(date_time).push(x[2])
        ref.child('Station 3 - Arduino Uno/').child('Gyro X - Arduino Uno').child(date_time).push(x[3])
        ref.child('Station 3 - Arduino Uno/').child('Gyro Y - Arduino Uno').child(date_time).push(x[4])
        ref.child('Station 3 - Arduino Uno/').child('Gyro Z - Arduino Uno').child(date_time).push(x[5])
        ref.child('Station 3 - Arduino Uno/').child('Temp - Arduino Uno').child(date_time).push(x[-1])

        ref.child('Station 3 - Arduino Uno/').child('Acceleration X - Arduino Uno/Current').set(x[0])
        ref.child('Station 3 - Arduino Uno/').child('Acceleration Y - Arduino Uno/Current').set(x[1])
        ref.child('Station 3 - Arduino Uno/').child('Acceleration Z - Arduino Uno/Current').set(x[2])
        ref.child('Station 3 - Arduino Uno/').child('Gyro X - Arduino Uno/Current').set(x[3])
        ref.child('Station 3 - Arduino Uno/').child('Gyro Y - Arduino Uno/Current').set(x[4])
        ref.child('Station 3 - Arduino Uno/').child('Gyro Z - Arduino Uno/Current').set(x[5])
        ref.child('Station 3 - Arduino Uno/').child('Temp - Arduino Uno/Current').set(x[-1])
        ref.child('Station 3 - Arduino Uno/').child('Temp - Arduino Uno/Get data').push(temp)
    except Exception as e:
        continue