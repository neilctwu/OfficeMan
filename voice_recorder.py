import socket

from processor import Processor
from googleapi import S2T, T2S
from audio import Audio


class OfficeMan:
    def __init__(self, port):
        self.init_server(('localhost', port))
        self.processor = Processor(self.sample_rate)
        self.s2t = S2T(self.sample_rate)
        self.t2s = T2S()
        # TODO: independ speaker
        self.speaker = Audio('output', self.sample_rate, 1.0)

    def listen(self):
        queries = b''
        while True:
            query = self.conn.recv(4096)
            queries += query
            if len(queries)<(self.sample_rate*2):
                continue
            self.forward(queries)

    def forward(self, x):
        x = self.processor(x)
        print(x)
        x = self.s2t(x)
        x = self.t2s(x)

        voice_len = len(x.audio_content)
        for x in range(44, voice_len, self.speaker.chunk):
            self.speaker.stream.write(x.audio_content[x:(x + self.speaker.chunk)])

    def init_server(self, address):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(address)
        self.server_socket.listen()
        print("Listening for client . . .")
        self.conn, address = self.server_socket.accept()
        print("Connected to client at ", address)
        self.sample_rate = int(self.conn.recv(2048).decode().split(':')[-1])
        self.sample_width = int(self.conn.recv(2048).decode().split(':')[-1])
        print(f'Sample rate={self.sample_rate}, sample_width={self.sample_width}')


if __name__ == '__main__':
    OfficeMan(8220)