# Face Recognize

Blocks for working with facial recognition

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

Input
-------
- Any signal to trigger the block to run

Output
-------
- A signal containing the facial encoding, user id, and name

sample output: 

```
{
 'encoding': <binary, 1182 bytes, '80 03 63 6e 75 6d...'>, 
 'name': 'Barack', 
 'user_id': 'bobama'
}
```

Find Face
========
Grab a frame from an intel realsense camera, find a face encoding within the frame, compare the encoding with encoding of known faces from an input signal, output a signal containing the name of the found face.

Dependencies
----------------
- face_recognition
- opencv-python
- pyrealsense
- pickle

Input
-------
- A signal through "unknown" to begin collecting frames from the camera and search for faces.
- A signal through "known" to add the known face encodings and names to compare found faces against. Expects a 'faces' object wihch contains a list of objects with attributes `'name'`, `'user_id'`, `'id'`, and `'encoding'`.

sample known input:
```
{
 'faces': [
  {
   'name': 'Barack', 
   'user_id': 'bobama', 
   'id': '4999011a-8ded-49c4-a927-77a09dcdb578', 
   'encoding': <binary, 1182 bytes, '80 03 63 6e 75 6d...'>
  }
 ]
}
```

Output
-------
- A signal containing the name of the face identified from the realsense camera

sample output: 

```
{
 'face': 'Barack'
}
```
