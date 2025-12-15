import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import csv

cred = credentials.Certificate("bmedesign.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://bmedesign-eeglab-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
while True:
    ref_heart_rate = db.reference('/Station 1 - NodeMCU 1/Heartrate/30-04-2023')
    ref_SpO2 = db.reference('/Station 1 - NodeMCU 1/SpO2/30-04-2023')

    data_heart_rate = ref_heart_rate.get()
    data_SpO2 = ref_SpO2.get()

    # with open('data_heart_rate_3.csv', 'w', newline='') as csvfile:
    #     header_key = ['Time', 'BPM']
    #     data_heart_rate_table = csv.DictWriter(csvfile, fieldnames= header_key)
    #
    #     data_heart_rate_table.writeheader()
    #     for key in data_heart_rate.keys():
    #         data_heart_rate_table.writerow({'Time': key, 'BPM': data_heart_rate[key]})

    with open('data_spo2_3.csv', 'w', newline='') as csvfile:
        header_key = ['Time', 'SpO2']
        data_spo2_table = csv.DictWriter(csvfile, fieldnames= header_key)

        data_spo2_table.writeheader()
        for key in data_SpO2.keys():
            data_spo2_table.writerow({'Time': key, 'SpO2': data_SpO2[key]})