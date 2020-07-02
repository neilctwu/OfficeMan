from audio import Audio

import socket
import time


class VoiceCatcher(Audio):
    def __init__(self, port, sample_rate, sec_per_frame=1.0):
        super().__init__('input', sample_rate, sec_per_frame)
        self.cache_size = int(sample_rate*sec_per_frame)
        self.cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_socket(port)
        time.sleep(3)
        self.cli_socket.send(f'Sample Rate:{sample_rate}'.encode('utf-8'))
        self.cli_socket.send(f'Sample Width:{self.p.get_sample_size(self.format)}'.encode('utf-8'))
        print("* recording")
        self.listen()

    def set_socket(self, port):
        self.cli_socket.connect(("localhost", port))

    def listen(self):
        while True:
            data = self.stream.read(self.cache_size)
            self.cli_socket.send(data)


if __name__=='__main__':
    VoiceCatcher(8220, 44100)