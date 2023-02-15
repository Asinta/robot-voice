#!/usr/bin/env python3
import ssl

import speech_recognition as sr

from slack_agent import SlackClient
from utils import say

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


slack = SlackClient('TOKEN_STR', 'CHANNEL_ID', ssl_context)


def voice_callback(recognizer: sr.Recognizer, audio):
    try:
        content = recognizer.recognize_google(audio)
        print(content)
        if 'name' in content:
            say('我的中文名叫司马替，是你的项目全能管家', lang_version=1)
            say('My name is Robot, and it\'s your project all-rounder', lang_version=0)
        elif 'detective' in str(content).lower():
            say('真実はいつもひとつ', lang_version=2)
        elif 'hi' in content or 'hey' in content:
            say('私の名前はRobotです、あなたのプロジェクトのオールラウンドバトラーです', lang_version=2)
        elif 'awesome' in content:
            say('Thank you, you are the best coder')
        elif 'tired' in content:
            say('don\'t be worry, be happy')
            say('頑張れ', lang_version=2)
        elif 'great' in content:
            say('山东菏泽曹县 牛叉 6 6 6', lang_version=1)
        elif 'another' in content or 'more' in content or 'again' in content:
            slack.post_message('@Robot lucky')
        elif 'else' in content:
            say('唱，跳，rap和篮球', lang_version=1)
        elif 'dog' in content or 'girl' in content or 'boy' in content:
            say('ありがとうございました, あなたは最高です', lang_version=2)
        elif 'go' in content:
            say('wang wang wang! prepare launch to the sun!')
            slack.post_message('message you want to post')
        else:
            # send recognised content to Robot
            content = content.replace('robot', '@Robot')
            if 'pipeline' in content:
                index = str(content).rfind('pipeline')
                content = content[0: index + 8]
                print(content)
                content += 'sample-repo-name'
            slack.post_message(content)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service;")


def main():
    try:
        r = sr.Recognizer()
        m = sr.Microphone()
        r.energy_threshold = 550

        stop_listening = r.listen_in_background(m, voice_callback)

        slack.listen_for_message()
    except KeyboardInterrupt:
        stop_listening(wait_for_stop=True)


if __name__ == '__main__':
    main()
