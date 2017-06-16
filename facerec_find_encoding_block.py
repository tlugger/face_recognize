from nio.block.base import Block
from nio.properties import VersionProperty
from nio.signal.base import Signal

from face_recognition import face_encodings, face_locations
import picamera
import numpy as np

class FaceRecFindEncoding(Block):

    version = VersionProperty('2.0.0')

    def __init__(self):
        super().__init__()
        self.locations = []
        self.encodings = []
        self.camera = None

    def start(self):
        print("Starting camera")
        self.camera = picamera.PiCamera()
        self.camera.resolution = (320, 240)
        self.output = np.empty((240, 320, 3), dtype=np.uint8)

    def process_signals(self, signals):

        for signal in signals: 
            
            try:
                self.camera.capture(self.output, format="rgb")
                print("Capturing image")
            except:
                return           

            self.locations = face_locations(self.output)
            print("Found {} faces in image.".format(len(self.locations)))
            self.encodings = face_encodings(self.output, self.locations)
            
            signal.encoding = self.encodings

        self.notify_signals(signals)

