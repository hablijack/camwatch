#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Bot
from library.Configuration import Configuration
import logging


class TelegramHelper:
    
    def __init__(self):
        self.config = Configuration()

    async def send_telegram_image(self, image, caption):
        await Bot(self.config.telegram_home_bot_id()).send_photo(
            chat_id=self.config.telegram_home_bot_chat(), 
            caption=caption,
            photo=image
        )

    async def send_telegram_message(self, message):
        await Bot(self.config.telegram_home_bot_id()).send_message(
            chat_id=self.config.telegram_home_bot_chat(), 
            text=message
        )
