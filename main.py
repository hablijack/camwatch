#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Bot
from waitress import serve
from flask import Flask, request
import requests
from io import BytesIO
import os

app = Flask(__name__)

async def send_telegram_image(binary):
    TELEGRAM_BOT_ID = os.environ['TELEGRAM_BOT_ID']
    TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
    bot = Bot(TELEGRAM_BOT_ID)
    await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=binary)

async def fetch_current_webcam_image():
    WEBCAM_HOST = os.environ['WEBCAM_HOST']
    WEBCAM_USER = os.environ['WEBCAM_USER']
    WEBCAM_PASSWORD = os.environ['WEBCAM_PASSWORD']
    response = requests.get(
        "http://" + WEBCAM_HOST + "/tmpfs/snap.jpg?usr=" + 
        WEBCAM_USER + "&pwd=" + WEBCAM_PASSWORD)
    return response

@app.route('/upload_picture', methods=['POST'])
async def upload_picture():
    imagefile = request.files.get('imageFile')
    await send_telegram_image(BytesIO(imagefile.read()))
    return {'msg': 'success'}

@app.route('/send_alarm', methods=['GET'])
async def send_alarm():
    response = await fetch_current_webcam_image()
    await send_telegram_image(BytesIO(response.content));
    return {'msg': 'success'}

@app.route('/health')
def health():
    return {'status': 'UP'}

if __name__ == "__main__":
    try:
        serve(app, port=5000)
    except (KeyboardInterrupt, SystemExit):
        pass
