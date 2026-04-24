import cv2
import numpy as np
import time
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils


# ---------------- ANGLE FUNCTION ----------------
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


# ---------------- FRAME GENERATOR ----------------
def generate_frames(exercise_type):

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    counter = 0
    stage = None
    last_rep_time = 0
    start_time = time.time()

    # smoothing variables
    prev_pushup_angle = 0
    prev_knee_angle = 0

    # stability counters
    up_frames = 0
    down_frames = 0

    alpha = 0.7  # smoothing factor

    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=0
    ) as pose:

        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.resize(frame, (640, 480))

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            angle = 0  # safe default

            try:
                if result.pose_landmarks:

                    landmarks = result.pose_landmarks.landmark

                    shoulder = [landmarks[11].x, landmarks[11].y]
                    elbow = [landmarks[13].x, landmarks[13].y]
                    wrist = [landmarks[15].x, landmarks[15].y]
                    hip = [landmarks[23].x, landmarks[23].y]
                    knee = [landmarks[25].x, landmarks[25].y]
                    ankle = [landmarks[27].x, landmarks[27].y]

                    current_time = time.time()

                    # ================= PUSH-UP =================
                    if exercise_type == "pushup":

                        raw_angle = calculate_angle(shoulder, elbow, wrist)

                        angle = alpha * raw_angle + (1 - alpha) * prev_pushup_angle
                        prev_pushup_angle = angle

                        # stability detection
                        if angle > 160:
                            up_frames += 1
                            down_frames = 0
                        elif angle < 80:
                            down_frames += 1
                            up_frames = 0
                        else:
                            up_frames = 0
                            down_frames = 0

                        if up_frames > 5:
                            stage = "UP"

                        if down_frames > 5 and stage == "UP":
                            if current_time - last_rep_time > 1:
                                stage = "DOWN"
                                counter += 1
                                last_rep_time = current_time

                    # ================= SQUAT =================
                    elif exercise_type == "squat":

                        knee_angle = calculate_angle(hip, knee, ankle)

                        angle = alpha * knee_angle + (1 - alpha) * prev_knee_angle
                        prev_knee_angle = angle

                        hip_angle = calculate_angle(shoulder, hip, knee)

                        # standing
                        if angle > 160 and hip_angle > 160:
                            stage = "UP"

                        # squat
                        elif angle < 100 and hip_angle < 140 and stage == "UP":
                            if current_time - last_rep_time > 1.2:
                                stage = "DOWN"
                                counter += 1
                                last_rep_time = current_time

                    # ================= DISPLAY =================

                    elapsed_time = int(time.time() - start_time)

                    cv2.putText(image, f'Reps: {counter}', (10, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2)

                    cv2.putText(image, f'Stage: {stage}', (10, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (255, 255, 0), 2)

                    cv2.putText(image, f'Time: {elapsed_time}s', (10, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (255, 255, 255), 2)

                    cv2.putText(image, f'Angle: {int(angle)}', (10, 160),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (200, 200, 200), 2)

            except Exception as e:
                print("Error:", e)

            # draw skeleton
            if result.pose_landmarks:
                mp_draw.draw_landmarks(
                    image,
                    result.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_draw.DrawingSpec(color=(0, 0, 0), thickness=1, circle_radius=1)
                )

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()