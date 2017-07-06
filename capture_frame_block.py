from nio.block.base import Block
from nio.properties import VersionProperty, IntProperty, BoolProperty, StringProperty
from nio.signal.base import Signal

import cv2
import pickle
import base64
import urllib.request
import numpy

class CaptureFrame(Block):

    version = VersionProperty('2.0.0')
    camera = IntProperty(title='Camera Index', default=0)
    ipcam = BoolProperty(title='Use IP Camera?', default=False)
    ipcam_address = StringProperty(title='IP Camera Address', default='')

    def __init__(self):
        super().__init__()
        self.video_capture = None

    def start(self):
        if not self.ipcam():
            self.video_capture = cv2.VideoCapture(self.camera())

    def process_signals(self, signals):

        for signal in signals:
            if self.ipcam():
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
                try:
                    ret, frame = self.video_capture.read()
                except:
                    break

            sig = Signal({
                "capture": base64.b64encode(pickle.dumps(frame)).decode()
            })
            self.notify_signals([sig])
