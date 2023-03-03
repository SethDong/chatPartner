#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

import sounddevice as sd
import soundfile as sf

duration = 10  # 录音时长为20秒
fs = 44100  # 采样率


def record_audio():
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    print("recording starting...")
    sd.wait()
    print("recording ended.")

    audio_file = "temp.wav"
    sf.write(audio_file, myrecording, fs)
    print("records write finished.")
