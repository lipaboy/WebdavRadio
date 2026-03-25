import random
import os
import sys
import subprocess

import Player
import Signal

import disk
    
#-------------------
    
SONGS_COUNT = 4842
LOCAL_SONG_PATH = sys.path[0] + "/music/1.mp3"

#-------------------

def read_nth_line(nth: int) -> str:
    with open(sys.path[0] + '/db/song_list.txt', 'r', encoding="utf-8") as f:
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

if __name__ == "__main__":
    Signal.register_signal()
    
    try:
        through_proxy = len(sys.argv) > 1 and sys.argv[1] == 'proxy'
        download_random_file(through_proxy)

        song_audio_segment : Player.AudioSegment = Player.AudioSegment.from_mp3(LOCAL_SONG_PATH)

        if not through_proxy:
            FNULL = open(os.devnull, 'w')
            subprocess.call(['mpv', f'{LOCAL_SONG_PATH}'], stdout=FNULL)
            os.remove(LOCAL_SONG_PATH)
        else:
            os.remove(LOCAL_SONG_PATH)
            Player.play(song_audio_segment)
    except Exception as e:
        print(e)
        