import streamlit as st
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# Directory to store face images
IMAGE_DIR = "registered_faces"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Load known faces
def load_registered_faces():
    encodings = []
    names = []
    for filename in os.listdir(IMAGE_DIR):
        path = os.path.join(IMAGE_DIR, filename)
        img = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(img)
        if encoding:
            encodings.append(encoding[0])
            names.append(os.path.splitext(filename)[0])
    return encodings, names

known_encodings, known_names = load_registered_faces()

# Save attendance
def mark_attendance(name):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("Attendance.csv", "a") as f:
        f.write(f"{name},{dt_string}\n")

# Streamlit UI
st.title("🎭 Face Recognition Attendance System")

option = st.sidebar.radio("Select Mode", ["Register Face", "Recognize & Mark Attendance"])

# Register Faces
if option == "Register Face":
    st.subheader("Register a New Face")
    name = st.text_input("Enter Name:")
    if st.button("Capture & Save"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            path = os.path.join(IMAGE_DIR, f"{name}.jpg")
            cv2.imwrite(path, frame)
            st.success(f"Face Registered for {name}")
            known_encodings, known_names = load_registered_faces()
        cap.release()
        cv2.destroyAllWindows()

# Recognize Faces & Mark Attendance
elif option == "Recognize & Mark Attendance":
    st.subheader("Recognizing Faces...")
    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"
            
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match = np.argmin(face_distances)
                if matches[best_match]:
                    name = known_names[best_match]
                    mark_attendance(name)

            y1, x2, y2, x1 = face_location
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        frame_placeholder.image(frame, channels="BGR")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
