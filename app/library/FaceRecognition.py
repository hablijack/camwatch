#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from pathlib import Path
import logging
import os
from library.TelegramHelper import TelegramHelper
from uniface import FaceAnalyzer
from PIL import Image
from io import BytesIO
from numpy import uint8


class FaceRecognition:

    def __init__(self):
        pathlist = Path('./known_faces').glob('*.jpg')
        self.known_embeddings = []
        self.known_names = []
        self.telegram_helper = TelegramHelper()
        self.analyzer = FaceAnalyzer()
        for path in pathlist:
            image = np.array(Image.open(str(path)))
            faces = self.analyzer.analyze(image)
            if faces:
                self.known_embeddings.append(faces[0].embedding)
                basename = os.path.splitext(os.path.basename(path))[0]
                self.known_names.append(basename)

    async def detect_faces_in_image(self, image_file):
        try:
            faces = self.analyzer.analyze(image_file)
            if faces:
                unknown_embedding = faces[0].embedding
                found_face_names = []
                for known_embedding, name in zip(self.known_embeddings, self.known_names):
                    similarity = np.dot(unknown_embedding, known_embedding) / (
                        np.linalg.norm(unknown_embedding) * np.linalg.norm(known_embedding)
                    )
                    if similarity > 0.5:
                        found_face_names.append(name)
                image = Image.fromarray(uint8(image_file))
                in_memory_image = BytesIO()
                image.save(in_memory_image, 'JPEG')
                in_memory_image.seek(0)
                if found_face_names:
                    await self.telegram_helper.send_telegram_image(
                        image=in_memory_image,
                        caption=str.join(', ', found_face_names) + " an der Haustür gesehen: "
                    )
                else:
                    await self.telegram_helper.send_telegram_image(
                        image=in_memory_image,
                        caption="Unbekannte Person an der Haustür gesehen: "
                    )
            else:
                logging.info("Keine gesichter gefunden...")
        except Exception as ex:
            logging.error(ex)
