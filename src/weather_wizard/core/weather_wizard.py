import random
import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

from weather_wizard.utils.gesture_detector import GestureDetector
from weather_wizard.core.particle_system import Particle

# mp docs: hand landmarker tasks requires trained model that is compatible w task
model_path = "src/weather_wizard/models/hand_landmarker.task"

class WeatherWizard:
    
    def __init__(self):
        # initialize mediapipe
        print("Attempting to init mp...")

        # mp docs: building and configuring task
        BaseOptions = python.BaseOptions
        HandLandmarker = vision.HandLandmarker
        HandLandmarkerOptions = vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        self.latest_result = None # this will be updated with the hand signal everytime it changes, hence "latest" result

        
        # create hand landmarker with VIDEO mode
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self._on_result, # only for live stream mode

            # custom settings from that dude's video
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
        )
        
        self.landmarker = HandLandmarker.create_from_options(options)
        self.mp_draw = mp.tasks.vision.drawing_utils
        self.mp_drawing_styles = mp.tasks.vision.drawing_styles
        self.mp_hands = mp.tasks.vision.HandLandmarksConnections

        # initialize camera
        print("Attempting to open camera...")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise ValueError("failed")
        print("camera opened successfully")

        # initialize components
        success, image = self.cap.read()
        self.height, self.width = image.shape[:2]
        self.particle_system = Particle(self.width, self.height)
        self.gesture_detector = GestureDetector()

        # initialize state
        self.particles = []
        self.max_particles = 100
        self.current_effect = None

        # define colors
        self.RAIN_COLOR = (200, 200, 255)
        self.SNOW_COLOR = (255, 255, 255)
        self.LIGHTNING_COLOR = (255, 255, 100)

    # function to update result everytime it changes
    def _on_result(self, result, _output_image, _timestamp_ms):
        self.latest_result = result

    def run(self):

        start_time = time.time()

        # main loop to keep app running
        while True:
            success, image = self.cap.read()
            if not success:
                print("failed to read from camera")
                break

            image = cv2.flip(image, 1) # flip for selfie like display

            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # color opt
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
            timestamp_ms = int((time.time() - start_time) * 1000)

            # FIX: get landmarks -> hands.process deprecated
            # results = self.hands.process(rgb_image) # get hand landmarks by mediapipe

            self.landmarker.detect_async(mp_image, timestamp_ms)

            # draw hand w detect gestures

            if self.latest_result and self.latest_result.hand_landmarks:
                for hand_landmarks in self.latest_result.hand_landmarks:
                    # draw hand landmarks
                    self.mp_draw.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )

                    # detect gesture and update current effect
                    gesture = self.gesture_detector.detect_gesture(hand_landmarks)
                    if gesture:
                        self.current_effect = gesture

                        index_tip = hand_landmarks[8]
                        x_pos = int(index_tip.x * self.width)

                        # create new particle at finger position
                        if len(self.particles) < self.max_particles:
                            self.particles.append(
                                self.particle_system.create_particle(gesture, x_pos)
                            )
            self._update_particles(image)

            # show the image
            cv2.imshow('Weather Wizard', image)

            # break loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # clean up
        self.cap.release()
        cv2.destroyAllWindows()
        self.landmarker.close()

    '''
    particle logic that changes overlay in camera, image param signals change in particles
    '''
    def _update_particles(self, image):
        # update and draw all particles
        new_particles = []
        overlay = np.zeros_like(image)

        for particle in self.particles:
            if particle['type'] == "rain":
                # update rain particle position
                particle['y'] += particle['speed']
                if particle['y'] < self.height:
                    cv2.line(
                        overlay,
                        (int(particle['x']), int(particle['y'])),
                        (int(particle['x']), int(particle['y'] - 30)),
                        self.RAIN_COLOR,
                        3
                    )
                    new_particles.append(particle)
            elif particle['type'] == "snow":
                # update snow particle position
                particle['y'] += particle['speed']
                particle['x'] += particle['drift']
                if  0 < particle['y'] < self.height and 0 < particle['x'] < self.width:
                    cv2.circle(
                        overlay,
                        (int(particle['x']), int(particle['y'])),
                        15,
                        self.SNOW_COLOR,
                        -1
                    )
                    new_particles.append(particle)
            elif particle['type'] == "lightning":
                # update lightning particle
                particle['lifetime'] -= 0.2
                if particle['lifetime'] > 0:
                    # draw main lightning bolt
                    for i in range(len(particle['branches']) - 1):
                        start = particle['branches'][i]
                        end = particle['branches'][i + 1]

                        # ensure points are within screen bounds
                        start_x = max(0, min(self.width, int(start[0])))
                        start_y = max(0, min(self.height, int(start[1])))
                        end_x = max(0, min(self.width, int(end[0])))
                        end_y = max(0, min(self.height, int(end[1])))

                        # draw main bolt
                        cv2.line(overlay,
                                 (start_x, start_y),
                                 (end_x, end_y),
                                 self.LIGHTNING_COLOR, 4)

                        # add branches with 30% probability
                        if random.random() < 0.3:
                            branch_end_x = end_x + random.randint(-40, 40)
                            branch_end_y = end_y + random.randint(-20, 20)
                            branch_end_x = max(0, min(self.width, branch_end_x))
                            branch_end_y = max(0, min(self.height, branch_end_y))
                            cv2.line(overlay,
                                    (end_x, end_y),
                                    (branch_end_x, branch_end_y),
                                    self.LIGHTNING_COLOR, 2)

                        # add flash effect
                        if particle['lifetime'] > 4:
                            flash_overlay = np.full_like(overlay, 255)
                            overlay = cv2.addWeighted(overlay, 1, flash_overlay, particle['flash_intensity'], 0)
                        new_particles.append(particle)

        result = cv2.addWeighted(image, 1, overlay, 0.7, 0)
        image[:] = result[:]
        self.particles = new_particles