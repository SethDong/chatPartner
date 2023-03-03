#!/usr/bin/python
# -*- coding: <encoding name> -*-
_author_ = 'Dongxu'

import torch
# import re
import torchaudio
from speechbrain.pretrained import Tacotron2
from speechbrain.pretrained import HIFIGAN

# Intialize TTS (tacotron2) and Vocoder (HiFIGAN)
if torch.cuda.is_available():
    tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts",
                                       run_opts={"device": "cuda"})
    hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder",
                                    run_opts={"device": "cuda"})
else:
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


# def write2wav_nolimit_on_answer_len(content):
#     tacotron2 = Tacotron2.from_hparams(source="speechbrain/TTS_Tacotron2", savedir="tmpdir")
#     sentences = spliter(content)
#     print(sentences)
#     mel_outputs, mel_lengths, alignments = tacotron2.encode_batch(sentences)
#     # Running Vocoder (spectrogram-to-waveform)
#     combined_waveform = mel_outputs[0]
#     for i in range(1, len(mel_outputs)):
#         combined_waveform = torch.cat([combined_waveform, mel_outputs[i]], dim=1)
#
#     waveforms = hifi_gan.decode_batch(combined_waveform)
#     # Save the waverform
#     torchaudio.save('TTS.wav', waveforms.squeeze(1), 22050)
#     return 1


# def spliter(text):
#     # 使用正则表达式拆分文本
#     sentences = re.split(r'(?<=[^A-Z].[.?!]) +(?=[A-Z])', text)
#
#     # 将标点符号添加到每个句子的末尾
#     for i in range(len(sentences) - 1):
#         last_char = sentences[i][-1]
#         if last_char in ['.', '?', '!']:
#             continue
#         next_char = sentences[i + 1][0]
#         if next_char in ['.', '?', '!']:
#             sentences[i] += last_char
#     # 输出句子列表
#     return sentences
