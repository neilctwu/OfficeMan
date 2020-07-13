from encoder import EncoderRNN
from decoder import LuongAttnDecoderRNN
from eval import GreedySearchDecoder, evaluate
from utils import loadPrepareData, normalizeString
from params import *

from torch import nn
import torch
import os

ckpt = 'ckpt/39900_checkpoint.tar'

class ChatMan:
    def __init__(self, ckpt):
        self.ckpt = ckpt
        self._data_prep()
        self.embedding = nn.Embedding(self.voc.num_words, hidden_size)
        self.encoder = EncoderRNN(hidden_size, self.embedding, encoder_n_layers, dropout)
        self.decoder = LuongAttnDecoderRNN(attn_model, self.embedding, hidden_size, self.voc.num_words, decoder_n_layers, dropout)
        self._load_ckpt()
        self.to(device)
        self.eval()
        self.searcher = GreedySearchDecoder(self.encoder, self.decoder)

    def __call__(self, input_sentence):
        return self.predict(input_sentence)

    def _data_prep(self):
        self.datafile = os.path.join(corpus_name, "formatted_movie_lines.txt")
        self.voc, _ = loadPrepareData(corpus_name, self.datafile, MAX_LENGTH)

    def _load_ckpt(self):
        checkpoint = torch.load(self.ckpt)
        encoder_sd = checkpoint['en']
        decoder_sd = checkpoint['de']
        embedding_sd = checkpoint['embedding']
        self.voc.__dict__ = checkpoint['voc_dict']

        self.embedding.load_state_dict(embedding_sd)
        self.encoder.load_state_dict(encoder_sd)
        self.decoder.load_state_dict(decoder_sd)

    def predict(self, input_sentence):
        input_sentence = normalizeString(input_sentence)
        # Evaluate sentence
        output_words = evaluate(self.encoder, self.decoder, self.searcher, self.voc, input_sentence)
        # Format and print response sentence
        output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
        return ' '.join(output_words)

    def to(self, device):
        self.encoder = self.encoder.to(device)
        self.decoder = self.decoder.to(device)

    def eval(self):
        self.encoder.eval()
        self.decoder.eval()

