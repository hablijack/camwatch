#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

""""
Read configuration from environment variables
"""

class Configuration:

    def security_camera_host(self):
        return os.getenv('SEC_CAM_HOST')

    def security_camera_user(self):
        return os.getenv('SEC_CAM_USER')
    
    def security_camera_password(self):
        return os.getenv('SEC_CAM_PASS')

    def telegram_home_bot_chat(self):
        return os.getenv('TELEGRAM_HOME_BOT_CHAT')

    def telegram_home_bot_id(self):
        return os.getenv('TELEGRAM_HOME_BOT_ID')

    def mobile_camera_stream_url(self):
        return os.getenv('MOBILE_CAMERA_STREAM_URL')