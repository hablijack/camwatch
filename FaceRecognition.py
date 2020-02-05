#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import face_recognition
import PIL.image


class FaceRecognition:

    def __init__(self):
        barbara_img = face_recognition.load_image_file("barbara.jpg")
        barbara_encoding = face_recognition.face_encodings(barbara_img)[0]
        christoph_img = face_recognition.load_image_file("christoph.jpg")
        christoph_encoding = face_recognition.face_encodings(christoph_img)[0]
        self.known_faces = [
            barbara_encoding,
            christoph_encoding
        ]

    def check_persons(self, pictures):
        known_persons = []
        for picture in pictures:
            image = PIL.Image.open(picture.payload).convert('RGB')
            detection_results = self.recognize_in_picture(image)
            if detection_results[0]:
                known_persons.append("Barbara")
            if detection_results[1]:
                known_persons.append("Christoph")
        return known_persons

    def recognize_in_picture(self, unknown_image):
        results = [] 
        face_locations = face_recognition.face_locations(unknown_image)
        if len(face_locations) > 0:
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            results = face_recognition.compare_faces(self.known_faces, unknown_encoding)
        return results