from nio.block.base import Block
from nio.properties import VersionProperty, StringProperty
from nio.signal.base import Signal

import face_recognition
import pickle
import rethinkdb as r

class Add_Face(Block):

    image_path = StringProperty(title='Image Path', default='')
    uid = StringProperty(title='User ID', defult='')
    sname = StringProperty(title='Save Name', default='')
    version = VersionProperty('2.0.0')

    def __init__(self):
        super().__init__()
        self.conn = []

    def start(self):
        self.conn = r.connect("localhost", 28015).repl()

    def save_encoding(self, file_path, save_name, user_id):
        image = face_recognition.load_image_file(file_path)
        face_encoding = face_recognition.face_encodings(image)[0]

        serialized_encoding = pickle.dumps(face_encoding)

        r.db('employees').table('faces').insert({
            'user_id': user_id,
            'name': save_name,
            'encoding': serialized_encoding
        }).run(self.conn)
        self.logger.info("Added {} to employee face database.".format(save_name))

    def process_signals(self, signals):
        for signal in signals:
            self.save_encoding(self.image_path(signal), self.sname(signal), self.uid(signal))
