import struct
import math
from scipy.signal import butter, lfilter

from utils import clock

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

@clock # 0.18sec
def bp_filter(binary_wav_list: list):
    bwav = b''.join(binary_wav_list)
    frames = int(len(bwav)/2)
    wav = list(struct.unpack('{}h'.format(frames), bwav))
    bp_wav = butter_bandpass_filter(wav, 300, 3600,
                                    (frames*2)/len(binary_wav_list), order=5)
    bp_wav = [int(x) for x in bp_wav]
    bp_bwav = struct.pack('{}h'.format(frames), *tuple(bp_wav))
    return bp_bwav


def get_rms(block):
    count = len(block) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, block)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0 / 32768.0)
        sum_squares += n * n
    return math.sqrt(sum_squares / count)
