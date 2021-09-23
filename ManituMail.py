#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import email
import getpass
import imaplib
import os
import sys


class ManituMail:

    def __init__(self):
        self.mail_server_url = os.environ['MAIL_SERVER_URL']
        self.mail_server_addr = os.environ['MAIL_SERVER_ADDR']
        self.mail_server_pwd = os.environ['MAIL_SERVER_PWD']

    def download_attachments(self):
        attachments = []
        try:
            imapSession = imaplib.IMAP4_SSL(self.mail_server_url)
            imapSession.login(self.mail_server_addr, self.mail_server_pwd)
            imapSession.select('INBOX')
            typ, data = imapSession.search(None,'(FROM "camera@diehabels.de" FROM "christoph.habel@googlemail.com")')

            for msgId in data[0].split():
                typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
                emailBody = messageParts[0][1]
                raw_email_string = emailBody.decode('utf-8')
                mail = email.message_from_string(raw_email_string)
                for part in mail.walk():
                    if part.get('Content-Disposition') and part.get_content_maintype() != 'multipart':
                        fileName = part.get_filename()
                        if bool(fileName):
                            attachments.append({'name': fileName, 'payload': part.get_payload(decode=True)})
                            imapSession.store(msgId, '+FLAGS', r'(\Deleted)')
            imapSession.expunge()
            imapSession.close()
            imapSession.logout()
        except:
            print('ERROR: no processing of mails possible!')
        return attachments
