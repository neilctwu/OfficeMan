from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud import texttospeech


class S2T:
    def __init__(self, sample_rate):
        self.client = speech_v1p1beta1.SpeechClient()
        self.sample_rate = sample_rate

    def __call__(self, data):
        language_code = "en-US"
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        config = {
            "language_code": language_code,
            "sample_rate_hertz": self.sample_rate,
            "encoding": encoding,
        }
        audio = {"content": data}
        result = self.client.recognize(config, audio)
        return result.results[0].alternatives[0].transcript  # pick first of first


class T2S:
    def __init__(self, sample_rate):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        self.audio_config = texttospeech.AudioConfig(
            sample_rate_hertz = sample_rate,
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

    def __call__(self, text):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )
        return response

