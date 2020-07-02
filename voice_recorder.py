import wave
import socket
import time
from datetime import datetime

from audio import Audio
from dsp import bp_filter, get_rms


class YAMABIKO(Audio):
    def __init__(self, sample_rate):
        super().__init__('output', int(sample_rate/3))
        self.rate = sample_rate

    def __call__(self, bwavs):
        time.sleep(1)
        self.stream.write(bwavs)


class Recorder:
    def __init__(self, port):
        self.set_server(('localhost', port))
        self.sample_rate = int(self.conn.recv(2048).decode().split(':')[-1])
        sample_width = int(self.conn.recv(2048).decode().split(':')[-1])
        print(f'Sample rate={self.sample_rate}, sample_width={sample_width}')

    def record(self):
        sentence_start = False
        queries = b''
        self.reset_sentence_index()
        speaker = YAMABIKO(self.sample_rate)
        while True:
            query = self.conn.recv(4096)
            queries += query
            if len(queries)<(self.sample_rate*2):
                continue
            print(f'Recieving data len:{len(queries)}')
            if not sentence_start:
                if self.check_rms(queries):
                    sentence_start = True
                    self.reset_sentence_index()
                    self.wavs.append(queries)
                    print('NOW')
            else:
                if not self.check_rms(queries):
                    if self.count == 2:
                        sentence_start = False
                        bp_bwav = self.voice_process(self.sample_rate)
                        # self.save_sentence(bp_bwav, sample_rate, sample_width)
                        speaker(bp_bwav)
                        print('QUIT')
                    self.count += 1
                self.wavs.append(queries)
            queries = b''

    def reset_sentence_index(self):
        self.wavs = []
        self.count = 0
        self.time = datetime.now().strftime('%Y%m%d_%H%M%S')

    def check_rms(self, queries, threshold=0.0008):
        rms = get_rms(queries)
        print(f'RMS:{rms}')
        return rms>threshold

    def voice_process(self, sample_rate):
        if len(self.wavs)<3:
            return
        TOTAL_FRAMES = len(self.wavs) * sample_rate
        bp_bwav = bp_filter(self.wavs)
        print(len(bp_bwav))
        return bp_bwav

    def save_sentence(self, bwav, sample_rate, sample_width):
        wf = wave.open(f'{self.time}.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(bwav)
        wf.close()

    def set_server(self, address):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(address)
        self.server_socket.listen()
        print("Listening for client . . .")
        self.conn, address = self.server_socket.accept()
        print("Connected to client at ", address)


if __name__ == '__main__':
    Recorder(8220)