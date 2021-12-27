#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import sys
import signal
import importlib
from chatbot import Bot
import glob
# TTS imports
from tts import MyTTS

# On first run, attempt to load config.py Module
try:
    print('** Getting config.py Module **')
    sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
    config = importlib.import_module('config')
    if config.Debug:
        print('** Debug Enabled! **')
    else:
        print('** Debug Not Enabled! **')
except Exception as e:
    print(e)
    print('[ERROR!] Please make [config.py] and place it in the same directory of twitchTransFN')
    input() # stop for error!!

def main_cleanup():
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    if config.Debug:
        print(f'_MEI base path: {base_path}')

    base_path = base_path.split("\\")
    base_path.pop(-1)
    temp_path = ""
    for item in base_path:
        temp_path = temp_path + item + "\\"

    mei_folders = [f for f in glob.glob(temp_path + "**/", recursive=False)]
    for item in mei_folders:
        if item.find('_MEI') != -1 and item != sys._MEIPASS + "\\":
            rmtree(item)

# sig handler
def sig_handler(signum, frame) -> None:
    sys.exit(1)

# Main Entry Point
def main():
    signal.signal(signal.SIGTERM, sig_handler)

    #print('twitchTransFreeNext (Version: {})'.format(version))
    print('tTFN+                    : Version 0.1')
    print('Connect to the channel   : {}'.format(config.Twitch_Channel))
    print('Translator Username      : {}'.format(config.Trans_Username))
    print('Translator ENGINE        : {}'.format(config.Translator))
    print('Google Translate         : translate.google.com')

    try:
        # Spin up the TTS
        my_tts = MyTTS(config.ReadOnlyTheseLang)
        # Initiate the twitchio bot
        bot = Bot(config)
        bot.set_tts(my_tts)
        bot.run()
    except Exception as e:
        print(e)
        input()
    finally:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        print('** Cleaning Up **')
        bot.cleanup() # chatbot cleanup
        my_tts.stop() # tts thread cleanup
        # main_cleanup() # _mei cleanup
        time.sleep(3)
        print('** Done Cleaning **')
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
    sys.exit(main())