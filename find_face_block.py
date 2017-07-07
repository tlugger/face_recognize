from nio.block.base import Block
from nio.block.terminals import input
from nio.properties import VersionProperty, BoolProperty, IntProperty, StringProperty
from nio.signal.base import Signal

import face_recognition
import cv2
import pickle
import base64
import urllib.request
import numpy

@input('known')
@input('unknown')
class FindFace(Block):

    version = VersionProperty('2.0.0')
    image = BoolProperty(title='Input Image?', default=False)
    ipcam = BoolProperty(title='Use IP Camera?', default=False)
    ipcam_address = StringProperty(title='IP Camera Address', default='')
    location = BoolProperty(title='Output Face Location?', default=False)
    camera = IntProperty(title='Camera Index', default=0)

    def __init__(self):
        super().__init__()
        self.video_capture = None
        self.ref_names = []
        self.ref_encodings = []

    def start(self):
        if (not self.image() and not self.ipcam()):
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
                        self.ref_encodings.append(pickle.loads(base64.b64decode(encoding)))

            if input_id == 'unknown':
                if self.image():
                    try:
                        frame = pickle.loads(signal.capture)
                    except TypeError:
                        frame = pickle.loads(base64.b64decode(signal.capture))

                elif self.ipcam():
                    done = False
                    stream = urllib.request.urlopen(self.ipcam_address())
                    ipbytes = bytes()
                    while not done:
                        ipbytes+=stream.read(1024)
                        a = ipbytes.find(b'\xff\xd8')
                        b = ipbytes.find(b'\xff\xd9')
                        if a!=-1 and b!=-1:
                            done = True
                            jpg = ipbytes[a:b+2]
                            ipbytes= ipbytes[b+2:]
                            frame = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8), cv2.IMREAD_UNCHANGED)

                else:
                    # Grab a single frome form the webacm
                    try:
                        ret, frame = self.video_capture.read()
                    except:
                        break

                    # If the camera didn't give us anything, don't do anything
                    if (not ret):
                        break

                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)

                if self.location():
                    signal = Signal({
                        "found": ["None"],
                        "location": [[0,0,0,0]]
                    })
                else:
                    signal = Signal({
                        "found": ["None"]
                    })


                names = []
                locations = []
                if len(face_encodings) > 0:
                    for e in range(len(face_encodings)):
                        # See if the face is a match for the known face(s)
                        match = face_recognition.compare_faces(self.ref_encodings, face_encodings[e], 0.5)
                        name = "Unknown"

                        for i in range(len(match)):
                            if match[i]:
                                name = self.ref_names[i]

                        names.append(name)
                        location = [face_locations[e][0], face_locations[e][1], face_locations[e][2], face_locations[e][3]]
                        locations.append(location)

                    if self.location():
                        signal = Signal({
                            "found": names,
                            "location": locations
                        })
                    else:
                        signal = Signal({
                            "found": names
                        })

                self.notify_signals([signal])
