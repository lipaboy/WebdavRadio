import random
import os
import sys
import subprocess

import Player
import Signal

import disk
    
#-------------------
    
SONGS_COUNT = 4842
LOCAL_SONG_PATH = "./music/1.mp3"

#-------------------

def read_nth_line(nth: int) -> str:
    with open('db/song_list.txt', 'r', encoding="utf-8") as f:
        for _ in range(nth):
            f.readline()
        return f.readline().strip()
    return ""

#-------------------

def download_random_file(through_proxy: bool) -> int:
    line_num = random.randint(1, SONGS_COUNT) - 1
    song_name = read_nth_line(line_num)
    disk.openClientSession(through_proxy).download_sync(remote_path=song_name, local_path=LOCAL_SONG_PATH)
    return line_num

#-------------------

class RadioMoment:
    def __init__(self):
        self.filename = 'current.txt'
    
    def save(self, line: int, moment_ms: int):
        with open(self.filename, 'w', encoding="utf-8") as f:
            f.write(str(line) + '\n')
            f.write(str(moment_ms))
            
    def load(self) -> tuple[int, int]:
        with open(self.filename, 'r', encoding="utf-8") as f:
            line = int(f.readline())
            moment_ms = int(f.readline())
            return (line, moment_ms)
        return None

#-------------------

if __name__ == "__main__":
    Signal.register_signal()
    through_proxy = len(sys.argv) > 1 and sys.argv[1] == 'proxy'
    
    radio = RadioMoment()
    moment_opt = radio.load()
    if moment_opt is None:
        song_line_num = download_random_file(through_proxy)
    else:
        time = 
    
    try:
        song_audio_segment : Player.AudioSegment = Player.AudioSegment.from_mp3(LOCAL_SONG_PATH)

        if not through_proxy:
            FNULL = open(os.devnull, 'w')
            subprocess.run(f'mpv {LOCAL_SONG_PATH} &> /dev/null', stdout=FNULL, shell=True)
        else:
            os.remove(LOCAL_SONG_PATH)
            # song_audio_segment = song_audio_segment[10 * 1000:20 * 1000]
            elapsed_secs : float = Player.play(song_audio_segment)
            elapsed_ms : int = int(elapsed_secs * 1000)
            radio.save(song_line_num, elapsed_ms)
    except Exception as e:
        print(e)
        