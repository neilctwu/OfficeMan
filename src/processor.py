from utils.dsp import bp_filter


class Processor:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate

    def __call__(self, input):
        x = self.bp_filter(input)

    def bp_filter(self, input):
        if len(input) < self.sample_rate*6: # 2bit for a sample, 3 blocks for detection
            return
        bp_bwav = bp_filter(input)
        return bp_bwav