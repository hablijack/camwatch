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
            typ1, data1 = imapSession.search(None,'(FROM "camera@online.de")')
            msg_id_array = data1[0].split() + data2[0].split()

            for msgId in msg_id_array:
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
