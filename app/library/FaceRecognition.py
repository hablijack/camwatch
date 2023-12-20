#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import face_recognition
import cv2
import logging
from library.Configuration import Configuration
from pathlib import Path

""""
Supply methods to recognize faces from a video stream
"""

class FaceRecognition:

    def __init__(self):
        self.config = Configuration()
        pathlist = Path('./known_faces').glob('*.jpg')
        self.known_faces = []
        self.known_names = []
        for path in pathlist:
            known_face = face_recognition.load_image_file(str(path))
            self.known_faces.append(face_recognition.face_encodings(known_face)[0])
            self.known_names.append(known_face)

    def search_in_stream(self):
        face_locations = []
        face_encodings = []
        found_face_names = []
        process_this_frame = True
        video_capture = cv2.VideoCapture(self.config.mobile_camera_stream_url())
        while True:
            ret, frame = video_capture.read()
            if process_this_frame:
                rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
               
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                    if True in matches:
                        found_face_names.append(self.known_names[matches.index(True)])
                    else: 
                        found_face_names.append("Unbekanntes Gesicht")
                
                if len(found_face_names) > 0:
                    logging.info(found_face_names)
                    break

            process_this_frame = not process_this_frame    
            # DURATION QUIT!
