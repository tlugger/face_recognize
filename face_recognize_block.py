from nio.block.base import Block
from nio.properties import VersionProperty
from nio.signal.base import Signal

import face_recognition
import cv2
import pyrealsense as pyrs

class Face_Recognize(Block):

    version = VersionProperty('2.0.0')

    def __init__(self):
        super().__init__()
        self.dev = None
        self.process_this_frame = True
        face_locations = []
        face_encodings = []
        face_names = []


    def start(self):
        pyrs.start()
        self.dev = pyrs.Device()

        obama_image = face_recognition.load_image_file("obama.jpg")
        self.obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        tyler_image = face_recognition.load_image_file("tyler.jpg")
        self.tyler_face_encoding = face_recognition.face_encodings(tyler_image)[0]

    def stop(self):
        self.dev.stop()

    def process_signals(self, signals):

        for signal in signals:
            self.dev.wait_for_frames()
            c = self.dev.color
            c = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)
            # Grab a single frame of video

            frame = c

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Only process every other frame of video to save time
            if self.process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    match = face_recognition.compare_faces([self.obama_face_encoding, self.tyler_face_encoding], face_encoding)
                    name = "Stranger!!!"

                    if match[0]:
                        name = "Barack"
                    elif match[1]:
                        name = "Tyler"

                    print(name)

                    face_names.append(name)

            self.process_this_frame = not self.process_this_frame

        self.notify_signals(signals)
