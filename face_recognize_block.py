from nio.block.base import Block
from nio.block.terminals import input
from nio.properties import VersionProperty
from nio.signal.base import Signal

import face_recognition
import cv2
import pyrealsense as pyrs
import pickle

@input('known')
@input('unknown')
class FaceRecognize(Block):

    version = VersionProperty('2.0.0')

    def __init__(self):
        super().__init__()
        self.dev = None
        self.ref_names = []
        self.ref_encodings = []

    def start(self):
        pyrs.start()
        self.dev = pyrs.Device()

    def stop(self):
        self.dev.stop()

    def process_signals(self, signals, input_id):

        for signal in signals:
            if input_id == 'known':
                for face in signal.faces:
                    self.ref_names.append(face['name'])
                    self.ref_encodings.append(pickle.loads(face['encoding']))

            if input_id == 'unknown':
                try:
                    self.dev.wait_for_frames()
                except AttributeError:
                    break

                c = self.dev.color
                frame = c

                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    match = face_recognition.compare_faces(self.ref_encodings, face_encoding)
                    name = "Unknown"

                    for i in range(len(match)):
                        if match[i]:
                            name = self.ref_names[i]

                    signal = Signal({
                        "found": name
                    })

                    self.notify_signals([signal])
