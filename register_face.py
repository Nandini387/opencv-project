import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not found!")
    exit()

print("Look at the camera...")
print("Press SPACE to register your face | Q to quit")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (800, 600))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Your Face Detected!", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Info text
    cv2.rectangle(frame, (0, 0), (800, 50), (50, 50, 50), -1)
    cv2.putText(frame, "Press SPACE to register face", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):
        if len(faces) == 0:
            print("No face detected! Try again.")
        else:
            # Save the full frame
            cv2.imwrite("known_face.jpg", frame)
            print("✅ Face registered successfully! Run lock_screen.py now.")
            break

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()