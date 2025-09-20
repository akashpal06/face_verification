import face_recognition
import cv2

def run_face_verification():
    # Load reference image
    uploaded_image = face_recognition.load_image_file("/Users/akashpal/Desktop/face_p/demon.jpg")
    face_encodings = face_recognition.face_encodings(uploaded_image)

    if len(face_encodings) == 0:
        return "No face found in reference image."

    uploaded_face_encoding = face_encodings[0]
    stop_video = False
    result_message = "No match found."

    def click_event(event, x, y, flags, param):
        nonlocal stop_video
        if event == cv2.EVENT_LBUTTONDOWN:
            if 20 <= x <= 150 and 20 <= y <= 70:
                stop_video = True

    video_capture = cv2.VideoCapture(0)
    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", click_event)

    while True:
        if stop_video:
            break

        ret, frame = video_capture.read()
        if not ret:
            result_message = "Failed to capture frame."
            break

        frame = cv2.flip(frame, 1)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces([uploaded_face_encoding], face_encoding)

            top *= 4; right *= 4; bottom *= 4; left *= 4

            if True in matches:
                result_message = "Face verified successfully!"
                cv2.putText(frame, "Verified", (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                result_message = "Face mismatch."
                cv2.putText(frame, "Mismatch", (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        # STOP button
        cv2.rectangle(frame, (20, 20), (150, 70), (0, 0, 250), -1)
        cv2.putText(frame, "STOP", (40, 55), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (251, 255, 255), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            result_message = "Verification stopped manually."
            break

    video_capture.release()
    cv2.destroyAllWindows()

    return result_message