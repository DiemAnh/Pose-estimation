import cv2
import mediapipe as mp
import time
import math
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
# import serial
# import serial.tools.list_ports

# ports = serial.tools.list_ports.comports()
# for port, desc, hwid in sorted(ports):
#     if desc.find("Arduino Uno") != -1:
#         arduino_port = port
# serialPort = serial.Serial(port = arduino_port, baudrate=9600,
#                            bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
#
# serialString = ""                           # Used to hold data coming over UART

class poseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList
    def findAngle(self, img, p1, p2, p3, draw=True):
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        if angle > 180:
            angle = 360 - angle
        # print(angle)
        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

def main():
    # angle_list = pd.DataFrame()
    pointCoor = pd.DataFrame()

    # cap = cv2.VideoCapture('Videos/punch1.mp4')
    cap = cv2.VideoCapture(0)

    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            print(lmList[14], '--', type(lmList[14][1]))
            # lmList[14]
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (lmList[12][1], lmList[12][2]), 15, (0, 0, 255), cv2.FILLED)
            arm_angle = detector.findAngle(img, 12, 14, 16)
            wrist_angle = detector.findAngle(img, 14, 16, 18)
            shoulder_angle = detector.findAngle(img, 14, 12, 24)
            print(arm_angle)
            print(wrist_angle)
            print(shoulder_angle)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)

        #joint_list = lmList[14] + list([arm_angle]) + lmList[16] + list([wrist_angle]) + lmList[12] + list([shoulder_angle]) + list([cTime])
        #pointCoor = pd.concat([pointCoor, pd.Series(joint_list)], axis=1)

        # Wait until there is data waiting in the serial buffer
        # if (serialPort.in_waiting > 0):
        #     # Read data out of the buffer until a carraige return / new line is found
        #     serialString = serialPort.readline()
        #
        #     # Print the contents of the serial data
        #     print(serialString.decode('Ascii'))
        #     angle_point = pd.Series(serialString.decode('Ascii'))
        #     angle_list = pd.concat([angle_list, angle_point])
        #
        #     # Tell the device connected over the serial port that we recevied the data!
        #     # The b at the beginning is used to indicate bytes!
        #     # serialPort.write(b"Thank you for sending data \r\n")

        if cv2.waitKey(1) & 0xFF == ord('d'):
            break
    pointCoor = pointCoor.T
    pointCoor.columns = ['14', 'arm_x', 'arm_y', 'arm_angle', '16', 'wrist_x', 'wrist_y', 'wrist_angle', '12','shoulder_x', 'shoulder_y', 'shoulder_angle', 'time']
    pointCoor.to_csv(r'ex_1.csv', index=None, header=True)

    # angle_list.to_csv(r'Data Record\mpu.csv', index=None, header=True)
    #
    # print(angle_list.shape)
    # while True:
    #     cv2.imshow('Image', img)
    #     if cv2.waitKey(1) & 0xFF == ord('s'):
    #         break

if __name__ == "__main__":
    main()
    df = pd.read_csv('ex_1.csv')
    print(df.describe())
    print(df.head())

    # df2 = pd.read_csv('Data Record/mpu.csv', sep='\r\n')

    fig = plt.figure(figsize=(14,7))
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    ax1.plot(df['time'], df['arm_angle'])
    ax1.plot(df['time'][0], 0)
    ax1.plot(df['time'][0], 180)
    ax1.title.set_text('Arm')

    ax2.plot(df['time'], df['wrist_angle'])
    ax2.plot(df['time'][0], 0)
    ax2.plot(df['time'][0], 180)
    ax2.title.set_text('Wrist')

    ax3.plot(df['time'], df['shoulder_angle'])
    ax3.plot(df['time'][0], 0)
    ax3.plot(df['time'][0], 180)
    ax3.title.set_text('Shoulder')

    # ax4.plot(df2.iloc[:, 0], df2.iloc[:, 1])
    # print(df2)
    plt.show()