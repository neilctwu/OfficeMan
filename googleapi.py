from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud import texttospeech
import wave

from audio import Audio

f = wave.open('male.wav', 'r')
sample_rate_hertz = f.getframerate()
data = f.readframes(f._nframes)


class S2T:
    def __init__(self):
        self.client = speech_v1p1beta1.SpeechClient()

    def __call__(self, sample_rate, data):
        language_code = "en-US"
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        config = {
            "language_code": language_code,
            "sample_rate_hertz": sample_rate_hertz,
            "encoding": encoding,
        }
        audio = {"content": data}
        return self.client.recognize(config, audio)


class T2S:
    def __init__(self):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        self.audio_config = texttospeech.AudioConfig(
            sample_rate_hertz = sample_rate_hertz,
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

    def __call__(self, text):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )
        return response

s2t = S2T()
text_response = s2t(sample_rate_hertz, data)

# First alternative is the most probable result
text = text_response.results[0].alternatives[0].transcript

t2s = T2S()
voice_response = t2s(text)

voice_len = len(voice_response.audio_content)
player = Audio('output', sample_rate_hertz, 1.0)
for x in range(44, voice_len, player.chunk):
    player.stream.write(voice_response.audio_content[x:(x+player.chunk)])