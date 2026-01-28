import random
import os
import time
import sys
import signal
import subprocess

from pydub import AudioSegment
from pydub import playback

import disk
    
#-------------------
    
SONGS_COUNT = 4842
LOCAL_SONG_PATH = "./music/1.mp3"
HAS_INTERRUPT_OCCURED = False

#-------------------

def custom_keyboard_interrupt_handler(signum, frame):
    global HAS_INTERRUPT_OCCURED
    HAS_INTERRUPT_OCCURED = True

#-------------------

def read_nth_line(nth: int) -> str:
    with open('db/song_list.txt', 'r', encoding="utf-8") as f:
        for i in range(nth):
            f.readline()
        return f.readline().strip()
    return ""

#-------------------

def download_random_file(through_proxy: bool):
    line_num = random.randint(1, SONGS_COUNT) - 1
    song_name = read_nth_line(line_num)
    disk.openClientSession(through_proxy).download_sync(remote_path=song_name, local_path=LOCAL_SONG_PATH)

#-------------------

def play(seg : AudioSegment):
    import pyaudio
    from pydub.utils import make_chunks

    portAudio = pyaudio.PyAudio()
    stream = portAudio.open(format=portAudio.get_format_from_width(seg.sample_width),
                    channels=seg.channels,
                    rate=seg.frame_rate,
                    output=True)

    # Just in case there were any exceptions/interrupts, we release the resource
    # So as not to raise OSError: Device Unavailable should play() be used again
    try:
        # break audio into half-second chunks (to allows keyboard interrupts)
        i = 0
        for chunk in make_chunks(seg, 500):
            # print("chunk: " + str(i))
            i += 1
            stream.write(chunk._data, exception_on_underflow=True)
            if HAS_INTERRUPT_OCCURED:
                print("Interrupt the audio")
                break
    except Exception as e:
            print(e)
    finally:
        stream.stop_stream()
        stream.close()
        portAudio.terminate()

#-------------------

if __name__ == "__main__":
    signal.signal(signal.SIGINT, custom_keyboard_interrupt_handler)
    
    try:
        through_proxy = len(sys.argv) > 1 and sys.argv[1] == 'proxy'
        download_random_file(through_proxy)

        song_audio_segment : AudioSegment = AudioSegment.from_mp3(LOCAL_SONG_PATH)

        os.remove(LOCAL_SONG_PATH)

        if not through_proxy:
            subprocess.run(f'mpv ./music/1.mp3 &> /dev/null', shell=True, check=True, text=True)
        else:
            play(song_audio_segment)
    except Exception as e:
        print(e)
        

