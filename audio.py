import pyaudio


class Audio:
    def __init__(self, io, sample_rate, sec_per_frame=1.0):
        self.format  = pyaudio.paInt16
        self.chunk = int(sample_rate*sec_per_frame)
        kwargs = {'format':self.format,
                  'channels':1,
                  'rate':sample_rate,
                  'frames_per_buffer':self.chunk,
                  'input': True if io == 'input' else False,
                  'output': True if io == 'output' else False}
        self.stream = pyaudio.PyAudio().open(**kwargs)
