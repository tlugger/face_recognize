from nio.block.base import Block
from nio.properties import VersionProperty, IntProperty
from nio.signal.base import Signal

import cv2
import pickle

class CaptureFrame(Block):

    version = VersionProperty('2.0.0')
    camera = IntProperty(title='Camera Index', default=0)


    def __init__(self):
        super().__init__()
        self.video_capture = None

    def start(self):
        self.video_capture = cv2.VideoCapture(self.camera())

    def process_signals(self, signals):

        for signal in signals:
            try:
                ret, frame = self.video_capture.read()
                sig = Signal({
                    "capture": pickle.dumps(frame)
                })
                self.notify_signals([sig])
            except:
                break
