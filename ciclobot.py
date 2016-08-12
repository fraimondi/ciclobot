import sys
import random
import traceback
import telepot
import subprocess
import logging
import os
import signal

from telepot.delegate import per_chat_id, create_open

class Player(telepot.helper.ChatHandler):

    parole = ['cycling', 'bici', 'bicycle', 'bike', 'ride', 'riding', 'train', 'ciclobot']

    def __init__(self, seed_tuple, timeout):
        super(Player, self).__init__(seed_tuple, timeout)
        self.logger = logging.getLogger('ciclobot')
        text_file = open("/home/pi/ciclobot/frasi.txt", "r")
        self.frasi = text_file.readlines()


    def open(self, initial_msg, seed):
        if ('text' in initial_msg.keys()):
          self.logger.info('New chat started with '+initial_msg['from']['first_name']+ " UID: "+str(initial_msg['from']['id']))
          self.logger.info('Message received from ID '+str(initial_msg['from']['id'])+': '+initial_msg['text'])

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        self.logger.info('Message received from ID '+str(msg['from']['id'])+
                         ' ('+msg['from']['first_name']+'): '+
                         msg['text'])
        if content_type == 'text':

          if any(x in msg['text'].lower() for x in self.parole):
            info_msg = random.choice(self.frasi)
            self.sender.sendMessage(info_msg)

logger = logging.getLogger('ciclobot')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('/home/pi/ciclobot/ciclobot.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

key_file = open("/home/pi/ciclobot/key.txt","r")
TOKEN = key_file.readline().rstrip()


bot = telepot.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(Player, timeout=600)),
])
bot.message_loop(run_forever=True)
