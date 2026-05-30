import cv2
import face_recognition
import numpy as np
import time

# ✅ Load your registered face
print("Loading registered face...")
try:
    known_image = face_recognition.load_image_file("known_face.jpg")
    known_encodings = face_recognition.face_encodings(known_image)

    if len(known_encodings) == 0:
        print("❌ No face found in known_face.jpg! Run register_face.py again.")
        exit()

    known_encoding = known_encodings[0]
    print("✅ Registered face loaded!")

except FileNotFoundError:
    print("❌ known_face.jpg not found! Run register_face.py first.")
    exit()

# ✅ Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not found!")
    exit()

# States
LOCKED   = "LOCKED"
UNLOCKED = "UNLOCKED"
state    = LOCKED

unlock_time   = None
UNLOCK_DURATION = 5      # seconds to stay unlocked
scan_interval   = 0.5    # scan every 0.5 seconds
last_scan_time  = 0

attempt_message = ""
message_timer   = 0

print("🔒 Lock Screen Active!")
print("Look at the camera to unlock | Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame    = cv2.resize(frame, (800, 600))
    display  = frame.copy()
    current_time = time.time()

    # ✅ Auto lock after UNLOCK_DURATION seconds
    if state == UNLOCKED:
        elapsed = current_time - unlock_time
        remaining = UNLOCK_DURATION - elapsed
        if remaining <= 0:
            state = LOCKED
            print("🔒 Screen Locked Again!")

    # ✅ Scan face every 0.5 seconds
    if state == LOCKED and (current_time - last_scan_time) > scan_interval:
        last_scan_time = current_time

        # Shrink frame for faster recognition
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small   = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for face_encoding in face_encodings:
            matches   = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=0.5)
            face_dist = face_recognition.face_distance([known_encoding], face_encoding)

            if matches[0]:
                confidence = round((1 - face_dist[0]) * 100, 1)
                state       = UNLOCKED
                unlock_time = current_time
                attempt_message = f"✅ Unlocked! Confidence: {confidence}%"
                message_timer   = current_time
                print(f"🔓 Unlocked! Confidence: {confidence}%")
            else:
                attempt_message = "❌ Face Not Recognized!"
                message_timer   = current_time
                print("❌ Unknown face!")

    # =====================
    # ✅ DRAW LOCK SCREEN UI
    # =====================

    if state == LOCKED:
        # Dark overlay
        overlay = display.copy()
        cv2.rectangle(overlay, (0, 0), (800, 600), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.6, display, 0.4, 0, display)

        # Lock icon (circle + rectangle)
        cv2.circle(display, (400, 220), 60, (100, 100, 255), 4)
        cv2.rectangle(display, (340, 240), (460, 320), (100, 100, 255), -1)
        cv2.rectangle(display, (340, 240), (460, 320), (150, 150, 255), 3)

        # Lock text
        cv2.putText(display, "SCREEN LOCKED", (230, 390),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (100, 100, 255), 3)
        cv2.putText(display, "Look at camera to unlock", (220, 440),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)

        # Scanning animation text
        dots = "." * (int(current_time * 2) % 4)
        cv2.putText(display, f"Scanning{dots}", (310, 490),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    else:
        # ✅ UNLOCKED UI - green overlay
        overlay = display.copy()
        cv2.rectangle(overlay, (0, 0), (800, 600), (0, 40, 0), -1)
        cv2.addWeighted(overlay, 0.3, display, 0.7, 0, display)

        # Green border
        cv2.rectangle(display, (10, 10), (790, 590), (0, 255, 0), 4)

        # Unlocked text
        cv2.putText(display, "UNLOCKED", (270, 560),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        # Countdown timer
        elapsed   = current_time - unlock_time
        remaining = max(0, UNLOCK_DURATION - elapsed)
        cv2.putText(display, f"Locks in: {remaining:.1f}s", (300, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # ✅ Show attempt message for 2 seconds
    if attempt_message and (current_time - message_timer) < 2:
        color = (0, 255, 0) if "Unlocked" in attempt_message else (0, 0, 255)
        cv2.putText(display, attempt_message, (180, 540),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Lock Screen", display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()