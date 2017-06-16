from nio.block.base import Block
from nio.properties import VersionProperty
from nio.signal.base import Signal

from face_recognition import face_encodings, face_locations, compare_faces, load_image_file
import picamera
import numpy as np
from firebase import firebase


class FaceRec(Block):

    version = VersionProperty('2.0.0')

    def __init__(self):
        super().__init__()
        self.locations = []
        self.encodings = []
        self.camera = None

    def start(self):
        print("Starting camera!")
        self.camera = picamera.PiCamera()
        self.camera.resolution = (320, 240)
        self.output = np.empty((240, 320, 3), dtype=np.uint8)
        self.firebase = firebase.FirebaseApplication('https://nio-facial-recognition.firebaseio.com', None)

    # Load a sample picture and learn how to recognize it.
        print("Loading known face image(s)")
        obama_image = load_image_file("obama_small.jpg")
        self.obama_face_encoding = face_encodings(obama_image)[0]

        tyler_image = load_image_file("Tyler.jpg")
        self.tyler_face_encoding = face_encodings(tyler_image)[0]

    def process_signals(self, signals):

        for signal in signals: 
            print("Capturing image.")
            
            try:
                self.camera.capture(self.output, format="rgb")
            except:
                return           

            self.locations = face_locations(self.output)
            print("Found {} faces in image.".format(len(self.locations)))
            self.encodings = face_encodings(self.output, self.locations)
            
            signal.name = "None"   
        
            for face_encoding in self.encodings:
                match = compare_faces([self.obama_face_encoding, self.tyler_face_encoding], face_encoding)
                name = "<Unknown Person>"

                print("Firebase query results: {}".format(self.firebase.get('/face_encodings', 'encoding')))


                if match[0]:
                    signal.name = "Barack Obama"
                elif match[1]:
                    signal.name = "Tyler Lugger"
                else:
                    signal.name = "Unknown person"
        

        self.notify_signals(signals)

