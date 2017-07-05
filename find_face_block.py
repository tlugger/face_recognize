from nio.block.base import Block
from nio.block.terminals import input
from nio.properties import VersionProperty, BoolProperty, IntProperty
from nio.signal.base import Signal

import face_recognition
import cv2
import pickle

@input('known')
@input('unknown')
class FindFace(Block):

    version = VersionProperty('2.0.0')
    image = BoolProperty(title='Input Image?', default=False)
    location = BoolProperty(title='Output Face Location?', default=False)
    camera = IntProperty(title='Camera Index', default=0)


    def __init__(self):
        super().__init__()
        self.video_capture = None
        self.ref_names = []
        self.ref_encodings = []

    def start(self):
        if not self.image():
            self.video_capture = cv2.VideoCapture(self.camera())

    def process_signals(self, signals, input_id):

        for signal in signals:
            if input_id == 'known':
                self.ref_names = []
                self.ref_encodings = []
                for face in signal.faces:
                    name = face['name']
                    for encoding in face['encoding']:
                        self.ref_names.append(name)
                        self.ref_encodings.append(pickle.loads(encoding))

            if input_id == 'unknown':
                if self.image():
                    frame = pickle.loads(signal.capture)
                else:
                    # Grab a single frome form the webacm
                    try:
                        ret, frame = self.video_capture.read()
                    except:
                        break

                    # If the camera didn't give us anything
                    if (not ret):
                        break

                # Resize frame of video to 1/3ish size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)

                if self.location():
                    signal = Signal({
                        "found": "None",
                        "location": [0,0,0,0]
                    })
                else:
                    signal = Signal({
                        "found": "None"
                    })


                #for face_encoding in face_encodings:
                for e in range(len(face_encodings)):
                    # See if the face is a match for the known face(s)
                    match = face_recognition.compare_faces(self.ref_encodings, face_encodings[e])
                    name = "Unknown"

                    for i in range(len(match)):
                        if match[i]:
                            name = self.ref_names[i]

                    if self.location():
                        signal = Signal({
                            "found": name,
                            "location": face_locations[e]
                        })
                    else:
                        signal = Signal({
                            "found": name
                        })

                self.notify_signals([signal])
