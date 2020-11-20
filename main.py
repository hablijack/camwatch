#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ManituMail import ManituMail
#from FaceRecognition import FaceRecognition
from apscheduler.schedulers.blocking import BlockingScheduler
from telegram import Bot
import os
import io


def watch_cam():
    telegram_bot_id = os.environ['TELEGRAM_BOT_ID']
    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    attachments = ManituMail().download_attachments()
    #FaceRecognition().check_persons(attachments)
    for photo in attachments:
        bot = Bot(telegram_bot_id)
        bot.send_photo(chat_id=telegram_chat_id, photo=io.BytesIO(photo['payload']))

if __name__ == "__main__":
    watch_cam()
    scheduler = BlockingScheduler()
    scheduler.add_job(watch_cam, 'interval', seconds=30)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
