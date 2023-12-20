#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Bot
from waitress import serve
from flask import Flask, render_template, send_from_directory
from flask_executor import Executor
import requests
from io import BytesIO
import logging
from library.FaceRecognition import FaceRecognition
from library.Configuration import Configuration
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
executor = Executor(app)
app.config['EXECUTOR_TYPE'] = 'thread'
logging.basicConfig(level=logging.INFO)

async def send_telegram_image(binary, chatid, botid):
    await Bot(botid).send_photo(chat_id=chatid, photo=binary)

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

def fetch_stream_and_detect_faces():
    try: 
        FaceRecognition().search_in_stream()
    except Exception as ex:
        logging.error(ex)

### WEBHOOK TO TRIGGER VIDEO FACE RECOGNITION
@app.route('/motion_detection', methods=['GET'])
def motion_detection():
    logging.info("GET on mobile camera start stream")
    executor.submit(fetch_stream_and_detect_faces)
    return {'msg': 'initiated'}

### WEBHOOK TO FETCH IMAGE FROM CAM
@app.route('/send_alarm', methods=['GET'])
async def send_alarm():
    logging.info("GET on house front camera send_alarm")
    config = Configuration()
    response = await fetch_current_webcam_image()
    await send_telegram_image(
        BytesIO(response.content),
        config.telegram_home_bot_chat(),
        config.telegram_home_bot_id()
    )
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
