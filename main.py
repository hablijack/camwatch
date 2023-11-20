#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Bot
from waitress import serve
from flask import Flask, request
import requests
from io import BytesIO
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

async def send_telegram_image(binary, chatid, botid):
    bot = Bot(botid)
    await bot.send_photo(chat_id=chatid, photo=binary)

async def fetch_current_webcam_image():
    WEBCAM_HOST = os.environ['WEBCAM_HOST']
    WEBCAM_USER = os.environ['WEBCAM_USER']
    WEBCAM_PASSWORD = os.environ['WEBCAM_PASSWORD']
    response = requests.get(
        "http://" + WEBCAM_HOST + "/tmpfs/snap.jpg?usr=" + 
        WEBCAM_USER + "&pwd=" + WEBCAM_PASSWORD)
    return response

### BIRDHOUSE CAMERA 
@app.route('/upload_picture', methods=['POST'])
async def upload_picture():
    logging.info("POST on birdhouse cam upload_picture method")
    imagefile = request.files.get('imageFile')
    await send_telegram_image(
        BytesIO(imagefile.read()),
        os.environ['TELEGRAM_BIRD_BOT_CHAT'],
        os.environ['TELEGRAM_BIRD_BOT_ID']
    )
    return {'msg': 'success'}

### HOUSE FRONT CAMERA 
@app.route('/send_alarm', methods=['GET'])
async def send_alarm():
    logging.info("GET on house front camera send_alarm")
    response = await fetch_current_webcam_image()
    await send_telegram_image(
        BytesIO(response.content),
        os.environ['TELEGRAM_HOME_BOT_CHAT'],
        os.environ['TELEGRAM_HOME_BOT_ID']
    )
    return {'msg': 'success'}

### TESTURL FOR BOTSETTINGS 
@app.route('/bottest', methods=['GET'])
async def bottest():
    logging.info("GET on bottest method to test telegram bots")
    response = await fetch_current_webcam_image()
    await send_telegram_image(
        BytesIO(response.content),
        os.environ['TELEGRAM_HOME_BOT_CHAT'],
        os.environ['TELEGRAM_HOME_BOT_ID']
    )
    await send_telegram_image(
        BytesIO(response.content),
        os.environ['TELEGRAM_BIRD_BOT_CHAT'],
        os.environ['TELEGRAM_BIRD_BOT_ID']
    )
    return {'msg': 'success'}

### SEND TEXT MESSAGE
@app.route('/send_text_message', methods=['POST'])
async def send_text_message():
    logging.info("POST on telegram send text message method")
    message = request.get_json()
    print(message)
    # bot = Bot(os.environ['TELEGRAM_GREENHOUSE_BOT_ID'])
    # await bot.send_message(
    #    chat_id=os.environ['TELEGRAM_GREENHOUSE_BOT_CHAT'], 
    #    text=message['text']
    # )

    return {'msg': 'success'}

@app.route('/health')
def health():
    return {'status': 'UP'}

@app.route('/')
def welcome():
    return {'status': 'UP'}

if __name__ == "__main__":
    try:
        serve(app, port=5000)
    except (KeyboardInterrupt, SystemExit):
        pass
