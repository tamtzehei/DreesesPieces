# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 21:01:06 2019

@author: Romik
"""

import os
import requests
import time
from xml.etree import ElementTree

from playsound import playsound

oid = 0

class TextToSpeech(object):
    def __init__(self):
        self.subscription_key = 'ae06249641924ee8bfebd863b121f33c'
        self.access_token = None
        self.count = 0
        self.oid = oid + 1
        
    def get_token(self):
        fetch_token_url = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)
    
    def save_audio(self, text):
        base_url = 'https://eastus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set(
            'name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)')
        voice.text = text
        body = ElementTree.tostring(xml_body)
    
        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open('sample' + str(self.count) + str(self.oid) + '.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) +
                      "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) +
                  "\nSomething went wrong. Check your subscription key and headers.\n")
            
        playsound('sample' + str(self.count) + str(self.oid) + '.wav')
        
        self.count += 1