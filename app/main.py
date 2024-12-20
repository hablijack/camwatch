#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from library.TelegramHelper import TelegramHelper
from waitress import serve
from flask import Flask, request, render_template, send_from_directory
from flask_executor import Executor
import requests
from io import BytesIO
import logging
from library.FaceRecognition import FaceRecognition
from library.Configuration import Configuration
from dotenv import load_dotenv
import numpy as np
from PIL import Image


load_dotenv()
app = Flask(__name__)
executor = Executor(app)
app.config['EXECUTOR_TYPE'] = 'thread'
logging.basicConfig(level=logging.INFO)


async def fetch_current_webcam_image():        
    config = Configuration()
    response = requests.get(
        "http://" + 
        config.security_camera_host() + 
        "/tmpfs/snap.jpg?usr=" + 
        config.security_camera_user() + 
        "&pwd=" + 
        config.security_camera_password())
    return response


async def face_recognition_worker(data):
    await FaceRecognition().detect_faces_in_image(data)

### POST A IMAGE FROM THE DOOR CAMERA
@app.route('/door_alarm', methods=['POST'])
def send_image():
    logging.info("POST a image from the door camera")
    fileStorage = request.files['imageFile']
    image = Image.open(fileStorage.stream)
    executor.submit(face_recognition_worker, np.asarray(image))
    return {'msg': 'success'}


### WEBHOOK TO FETCH IMAGE FROM CAM
@app.route('/send_alarm', methods=['GET'])
async def send_alarm():
    logging.info("GET on house front camera send_alarm")
    telegram_helper = TelegramHelper()
    response = await fetch_current_webcam_image()
    await telegram_helper.send_telegram_image(BytesIO(response.content), caption="Besucher am Eingangstor: ")
    return {'msg': 'success'}


@app.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('static', path)


@app.route('/health')
def health():
    return {'status': 'UP'}


@app.route('/')
def welcome():
    config = Configuration()
    return render_template(
        'home.html',
        sec_cam_host=config.security_camera_host(),
        sec_cam_user=config.security_camera_user(),
        sec_cam_pass=config.security_camera_password()
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s [%(name)s] %(message)s",
        datefmt='%d.%m.%Y %H:%M:%S',
        handlers=[
            logging.StreamHandler()
        ]
    )
    serve(app, port=5000)
