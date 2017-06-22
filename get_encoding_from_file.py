from nio.block.base import Block
from nio.properties import VersionProperty, StringProperty, ListProperty
from nio.signal.base import Signal
from nio.types.string import StringType

import face_recognition
import pickle

class GetEncodingFromFile(Block):

    image_paths = ListProperty(StringType, title='Image Path', default=[])
    uid = StringProperty(title='User ID', defult='')
    sname = StringProperty(title='Save Name', default='')
    version = VersionProperty('2.0.0')

    def __init__(self):
        super().__init__()

    def save_encoding(self, file_path, save_name, user_id, file2_path=None):
        serialized_encoding = []

        for f in file_path:
            image = face_recognition.load_image_file(f)
            face_encoding = face_recognition.face_encodings(image)[0]
            serialized_encoding.append(pickle.dumps(face_encoding))

        entry = {
            'user_id': user_id,
            'name': save_name,
            'encoding': serialized_encoding
        }

        return entry

    def process_signals(self, signals):
        add_face_signals = []
        for signal in signals:
            confirmation = self.save_encoding(self.image_paths(signal),self.sname(signal), self.uid(signal))
            add_face_signals.append(Signal(confirmation))

        self.notify_signals(add_face_signals)
