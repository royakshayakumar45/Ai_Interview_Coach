import streamlit as st

def show_emotion():

    st.title("🧠 Real-Time Emotion & Body Language Analyzer")

    import cv2
    import mediapipe as mp
    import time
    from deepface import DeepFace

    start = st.button("Start Camera")
    stop = st.button("Stop Camera")

    FRAME_WINDOW = st.image([])

    if start:

        cap = cv2.VideoCapture(0)

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()

        mp_draw = mp.solutions.drawing_utils

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                st.error("Camera error")
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            results = pose.process(rgb)

            body_score = 50

            if results.pose_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )

                landmarks = results.pose_landmarks.landmark

                shoulder_left = landmarks[11].y
                shoulder_right = landmarks[12].y

                diff = abs(shoulder_left - shoulder_right)

                if diff < 0.03:
                    body_score = 90
                elif diff < 0.07:
                    body_score = 70
                else:
                    body_score = 40

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(30,30)
            )

            for (x,y,w,h) in faces:

                face_img = frame[y:y+h, x:x+w]

                try:

                    result = DeepFace.analyze(
                        face_img,
                        actions=['emotion'],
                        enforce_detection=False
                    )

                    emotion = result[0]["dominant_emotion"]
                    score = result[0]["emotion"][emotion]

                    if score > 80:
                        conf_label = "High Confidence"
                        color = (0,255,0)

                    elif score > 50:
                        conf_label = "Medium Confidence"
                        color = (0,255,255)

                    else:
                        conf_label = "Low Confidence"
                        color = (0,0,255)

                    overall_score = int((score + body_score)/2)

                    label = f"{emotion} | {conf_label}"

                    cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)

                    cv2.putText(frame,label,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,color,2)

                    cv2.putText(frame,f"Emotion Score: {int(score)}",(10,30),
                                cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

                    cv2.putText(frame,f"Body Language Score: {body_score}",(10,60),
                                cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

                    cv2.putText(frame,f"Overall Confidence: {overall_score}",(10,90),
                                cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

                    # ===============================
                    # ✅ ADD THIS (STORE RESULT)
                    # ===============================
                    st.session_state["emotion_result"] = {
                        "emotion": emotion,
                        "emotion_score": int(score),
                        "body_score": body_score,
                        "overall_score": overall_score,
                        "confidence_level": conf_label
                    }

                except:
                    pass

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            FRAME_WINDOW.image(frame)

            if stop:
                break

        cap.release()
