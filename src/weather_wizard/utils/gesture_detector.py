INDEX_TIP, INDEX_PIP = 8, 6
MIDDLE_TIP, MIDDLE_PIP = 12, 10
RING_TIP, RING_PIP = 16, 14

class GestureDetector:

    def detect_gesture(self, landmarks):
        # analyze hand landmarks to determine weather effect

        index_up = landmarks[INDEX_TIP].y < landmarks[INDEX_PIP].y
        middle_up = landmarks[MIDDLE_TIP].y < landmarks[MIDDLE_PIP].y
        ring_up = landmarks[RING_TIP].y < landmarks[RING_PIP].y

        '''
        old deprecated landmark logic

        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        index_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
        middle_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].y
        ring_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP].y
        
        '''

        if index_up and not middle_up and not ring_up:
            return "rain" # index finger up
        elif index_up and middle_up and not ring_up:
                    return "snow" # index and middle up
        elif index_up and middle_up and ring_up:
                    return "lightning" # index, middle, ring up

        return None