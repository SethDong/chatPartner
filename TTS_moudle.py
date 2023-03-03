#!/usr/bin/python
# -*- coding: <encoding name> -*-
_author_ = 'Dongxu'

import torchaudio
from speechbrain.pretrained import Tacotron2
from speechbrain.pretrained import HIFIGAN
import re

# Intialize TTS (tacotron2) and Vocoder (HiFIGAN)
tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts")
hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder")


def write2wav(content):
    # Running the TTS
    mel_output, mel_length, alignment = tacotron2.encode_text(content)
    # Running Vocoder (spectrogram-to-waveform)
    waveforms = hifi_gan.decode_batch(mel_output)
    # Save the waverform
    torchaudio.save('TTS.wav', waveforms.squeeze(1), 22050)
    # print("wav file saved")
    return 1
