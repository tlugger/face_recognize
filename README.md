# Face Recognize

Blocks for working with facial recognition and images

Get Encoding From File
========
Find a face encoding from an image file, send encoding and other data as signal

Properties
--------------
- Image Path: Full path to the image file that will be added
- User ID: Id of the face being added to the database
- Save Name: Name of the face being added to the database

Dependencies
----------------
- face_recognition
- pickle
- base64

Input
-------
- Any signal to trigger the block to run

Output
-------
- A signal containing the facial encoding, user id, and name

sample output:

```
{
 'encoding': 'gANjbnVtcHkuY29yZS5tdWx0aWFycmF5Cl9yZWNvbn...',
 'name': 'Barack',
 'user_id': 'bobama'
}
```

Capture Frame
=============
Grab a frame of video from a specified camera and send the frame data as a signal.

Dependencies
----------------
- opencv-python
- pickle
- base64

Input
------
- Any signal to trigger a frame being grabbed from the specified camera

Output
-------
- A signal containing the serialized and stringified video frame

Find Face
=========
Grab a frame of video from a specified camera, find a face encoding within the frame, compare the encoding with encoding of known faces from an input signal, output a signal containing the name of the found face.

Dependencies
----------------
- face_recognition
- opencv-python
- pickle
- base64
- urllib.request
- numpy

Input
-------
- A signal through "unknown" to begin collecting frames from the camera and search for faces.
- A signal through "known" to add the known face encodings and names to compare found faces against. Expects a 'faces' object which contains a list of objects with attributes `'name'`, `'user_id'`, `'id'`, and `'encoding'`.

sample known input:
```
{
 'faces': [
  {
   'name': 'Barack',
   'user_id': 'bobama',
   'id': '4999011a-8ded-49c4-a927-77a09dcdb578',
   'encoding': 'gANjbnVtcHkuY29yZS5tdWx0aWFycmF5Cl9yZWNvbn...'
  }
 ]
}
```

Output
-------
- A signal containing the name of the face identified from the webcam

sample output:

```
{
 'found': 'Barack'
}
```
