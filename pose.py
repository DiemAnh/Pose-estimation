import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np

plt.ion()
fig = plt.figure()


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a) # First - joint 11
    b = np.array(b) # Mid - joint 13
    c = np.array(c) # End - joint 15
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle  
# # Curl counter variables
# counter = 0 
# stage = None

# For webcam input:
cap = cv2.VideoCapture(0)
# set up mediapipe instance
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
  
    # Recolor image to RGB  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    # Make detection
    results = pose.process(image)

    # Extract landmarks
    try:
        landmarks = results.pose_landmarks.landmark
            
        # Get coordinates
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
        # Calculate angle
        angle = calculate_angle(shoulder, elbow, wrist)
            
        # Visualize angle
        cv2.putText(image, str(angle), 
                           tuple(np.multiply(elbow, [640, 480]).astype(int)), #[640, 480] is position of webcam
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )         
        # # Curl counter logic
        # if angle > 160:
        #     stage = "down"
        # if angle < 30 and stage =='down':
        #     stage="up"
        #     counter +=1
        #     print(counter)         
    except:
        pass

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Render detections
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
  
  
    img = cv2.flip(image, 1)
    plt.imshow(image[:,:,::-1])
    fig.canvas.draw()
    fig.canvas.flush_events()
    
    
cap.release()