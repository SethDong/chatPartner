#!/usr/bin/python
# -*- coding: <encoding name> -*-
_author_ = 'Dongxu'
import openai
from TTS_moudle import write2wav
from playsound import playsound


def call_chat_api(message, apiKey):
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = apiKey

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # messages=[
        #     {"role": "user",
        #      "content": "hello, I need practice my English, "
        #                 "please work as a chatBot with me, "
        #                 "and if there is any errors in my grammar please correct them!"}
        # ]
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


if __name__ == '__main__':
    apiKey = apiInputer()
    init_by_prompt(apiKey=apiKey)
    while True:
        print("print your sentence:")
        usrInput = input()
        res = call_chat_api(usrInput + ", and please reply within 25 words", apiKey=apiKey)
        signal = write2wav(res)
        print(res)
        if signal == 1:
            playsound('TTS.wav')
        print()
