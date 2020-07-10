from audio import Audio
from dsp import get_rms

import socket
import time


class Recorder(Audio):
    def __init__(self, port, sample_rate, sec_per_frame=1.0):
        super().__init__('input', sample_rate, sec_per_frame)
        self.cache_size = int(sample_rate*sec_per_frame)
        self.sample_rate = sample_rate
        self.sentence_start = False
        self.wavs = []
        self.silent_count = 0
        self.init_socket(port)
        self.record()

    def init_socket(self, port):
        self.cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cli_socket.connect(("localhost", port))
        time.sleep(3)
        self.cli_socket.send(f'Sample Rate:{self.sample_rate}'.encode('utf-8'))
        self.cli_socket.send(f'Sample Width:{self.p.get_sample_size(self.format)}'.encode('utf-8'))
        print("* recording")

    def record(self):
        while True:
            data = self.stream.read(self.cache_size, exception_on_overflow=False)
            if not self.sentence_start:
                if self.check_rms(data):
                    self.sentence_start = True
                    self.wavs.append(data)
                    print('Recording start')
            else:
                if self.check_rms(data):
                    self.wavs.append(data)
                else:
                    if self.silent_count >= 2:
                        print('Recording finished')
                        self.cli_socket.send(b''.join(self.wavs))
                        self.reset_sentence_index()
                    else:
                        self.silent_count += 1
                        self.wavs.append(data)

    def reset_sentence_index(self):
        self.sentence_start = False
        self.wavs = []
        self.silent_count = 0

    @staticmethod
    def check_rms(queries, threshold=0.001):
        rms = get_rms(queries)
        print(f'RMS:{rms}')
        return rms > threshold


if __name__=='__main__':
    Recorder(8220, 44100)
