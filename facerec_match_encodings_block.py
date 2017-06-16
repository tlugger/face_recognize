from nio.block.base import Block
from nio.properties import VersionProperty
from nio.signal.base import Signal

from face_recognition import compare_faces
import numpy as np

class FaceRecMatchEncodings(Block):

    version = VersionProperty('2.0.0')

    def __init__(self):
        super().__init__()

    def process_signals(self, signals):

        for signal in signals:
            encoding = signal['encoding']
            print(encoding)

        self.notify_signals(signals)

