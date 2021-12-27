from datetime import datetime
import threading
from gtts import gTTS
from playsound import playsound
import queue
import time
import os
import shutil

class MyTTS:
    def __init__(self, read_these_langs):
        self.read_these_langs = read_these_langs
        self.gTTS_queue = queue.Queue()
        self.sound_queue = queue.Queue()
        self.TMP_DIR = './tmp/'
        self.thread_gTTS = threading.Thread(target=self.play)
        self.thread_sound = threading.Thread(target=self.sound_play)
        self._stop = threading.Event()

        print('** [MyTTS] Creating temp dir **')
        try:
            if os.path.exists(self.TMP_DIR):
                shutil.rmtree(self.TMP_DIR)
                time.sleep(0.3)
            os.mkdir(self.TMP_DIR)
        except Exception as e:
            print(f'**[MyTTS:init] Failed to make tem dir: {e} **')

    def run(self):
        self.thread_gTTS.start()
        self.thread_sound.start()

    # stop the queue and clean up
    def stop(self):
        print('** [MyTTS] Is stopping and cleaning up...')
        self._stop.isSet()
        try:
            os.rmdir('.\\tmp')
        except Exception as e:
            print(f'**[MyTTS:stop] Error while stopping: {e}')

    def put(self, in_text, lang_detect):
        self.gTTS_queue.put([in_text, lang_detect])

    def play(self):
        while True:
            q = self.gTTS_queue.get()
            if q is None:
                time.sleep(1)
            else:
                text = q[0]
                tl   = q[1]

                if self.read_these_langs and (tl not in self.read_these_langs):
                    continue

                # try creating the mp3
                try:
                    tts = gTTS(text, lang=tl)
                    tts_file = '.\\tmp\\tts-{}.mp3'.format(datetime.now().microsecond)
                    tts.save(tts_file)
                except Exception as e:
                    print('** [TTS::play] TTS sound file not generated **')
                    print(e)
                    return

                # try playing the sound
                try:
                    playsound(tts_file, True)
                except Exception as e:
                    print('** [TTS::play] Error playing generated TTS sound file **')
                    print(e.args)
                    return

                # finally, try to safely remove file
                try:
                    os.remove(tts_file)
                except Exception as e:
                    print('** [TTS::play] Error deleting TTS file **')
                    print(e)
                    return

    def sound_play(self):
        while True:
            q = self.sound_queue.get()
            if q is None:
                time.sleep(1)
            else:
                try:
                    playsound('.\\tmp\\{}.mp3'.format(q), True)
                except Exception as e:
                    print('** [TTS::sound_play] command cannot play file. **')
                    print(e.args)

