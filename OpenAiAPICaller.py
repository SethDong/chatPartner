#!/usr/bin/python
# -*- coding: <encoding name> -*-
import os

_author_ = 'Dongxu'
import openai
from TTS_moudle import write2wav
from playsound import playsound


def call_chat_api(message, apiKey):
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = apiKey

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": message
             }
        ]
    )
    return completion.choices[0].message["content"].replace("\n", "")
    # print(completion.choices[0].message)


def call_audio_api(apiKey):
    openai.api_key = apiKey
    audio_file = open("audio.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)


def apiInputer():
    apiKey = input("please parse your API key here:")
    if not len(apiKey) == 51:
        print("please check your apiKey")
        exit()
    return apiKey


def init_by_prompt(apiKey):
    print("model is initialing， please wait for a while...")
    call_chat_api("I am practicing my English, please help me with that, "
                  "and if you find my grammar error please let me know", apiKey=apiKey)
    print("model initial finished.")


def read_api_from_txt():
    print("loading apiKey from txt file...")
    if not os.path.isfile("apiKey.txt"):
        print("please create a txt file named 'apiKey', and parse your openAI APIkey into it.")
        exit()

    with open('apiKey.txt', 'r') as f:
        content = f.read()
        if not len(content) == 51:
            print("please check your apiKey")
            exit()
        return content


if __name__ == '__main__':
    apiKey = read_api_from_txt()
    init_by_prompt(apiKey=apiKey)
    while True:
        print("enter your sentence and press ENTER key in your keyboard")
        usrInput = input()
        res = call_chat_api(usrInput + ", and please reply no more than 25 words", apiKey=apiKey)
        # res = call_chat_api(usrInput, apiKey=apiKey)
        signal = write2wav(res)
        print(res)
        if signal == 1:
            playsound('TTS.wav')
        print()
