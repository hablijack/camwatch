#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import face_recognition
from pathlib import Path
import logging
import os
from library.TelegramHelper import TelegramHelper
from numpy import uint8
from PIL import Image
from io import BytesIO


""""
Supply methods to recognize faces from a image
"""

class FaceRecognition:


    def __init__(self):
        pathlist = Path('./known_faces').glob('*.jpg')
        self.known_faces = []
        self.known_names = []
        self.telegram_helper = TelegramHelper()
        for path in pathlist:
            known_face = face_recognition.load_image_file(str(path))
            self.known_faces.append(face_recognition.face_encodings(known_face)[0])
            basename = os.path.splitext(os.path.basename(path))[0]
            self.known_names.append(basename)

    async def detect_faces_in_image(self, image_file):
        try:
            found_face_names = []
            unknown_encoding = face_recognition.face_encodings(image_file)
            if len(unknown_encoding) > 0:
                results = face_recognition.compare_faces(self.known_faces, unknown_encoding[0])
                for index, result in enumerate(results):
                    if result == True:
                        found_face_names.append(self.known_names[index])
                image = Image.fromarray(uint8(image_file))
                in_memory_image = BytesIO()
                image.save(in_memory_image, 'JPEG')
                in_memory_image.seek(0)
                if len(found_face_names) > 0:
                    # known person detected -> tell the names and print the image to telegram
                    await self.telegram_helper.send_telegram_image(
                        image=in_memory_image, 
                        caption=str.join(', ', found_face_names) + " an der Haustür gesehen: "
                    )
                else:
                    # unknown person detected -> tell about the unknown and print the image to telegram
                    await self.telegram_helper.send_telegram_image(
                        image=in_memory_image, 
                        caption="Unbekannte Person an der Haustür gesehen: "
                    )        
            else:
                logging.info("Keine gesichter gefunden...")
        except Exception as ex:
            logging.error(ex)