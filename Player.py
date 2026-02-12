import time

from pydub import AudioSegment
from pydub import playback

import pyaudio
from pydub.utils import make_chunks

import Signal

#-------------------

def strip_metadata_completely(audio_segment):
    """
    Полностью удалить метаданные, создавая новый AudioSegment
    """
    # Получаем параметры аудио
    channels = audio_segment.channels
    sample_width = audio_segment.sample_width
    frame_rate = audio_segment.frame_rate
    
    # Получаем сырые аудиоданные
    raw_audio_data = audio_segment.raw_data
    
    # Создаем новый AudioSegment без метаданных
    clean_audio = AudioSegment(
        data=raw_audio_data,
        sample_width=sample_width,
        frame_rate=frame_rate,
        channels=channels
    )
    
    return clean_audio

#-------------------

def play(seg : AudioSegment) -> float:
    portAudio = pyaudio.PyAudio()
    # удалить все метаданные
    # seg = strip_metadata_completely(seg)  
    stream = portAudio.open(format=portAudio.get_format_from_width(seg.sample_width),
                    channels=seg.channels,
                    rate=seg.frame_rate,
                    output=True)
    
    end_play : float = 0

    # Just in case there were any exceptions/interrupts, we release the resource
    # So as not to raise OSError: Device Unavailable should play() be used again
    try:
        start_play : float = time.time()
        for chunk in make_chunks(seg, 500):
            stream.write(chunk._data, exception_on_underflow=True)
            if Signal.HAS_INTERRUPT_OCCURED:
                print("Interrupt the audio")
                break
        end_play : float = time.time() - start_play
    except Exception as e:
            print(e)
    finally:
        stream.stop_stream()
        stream.close()
        portAudio.terminate()
        return end_play