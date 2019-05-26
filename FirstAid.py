#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 16:28:17 2019

@author: Clari
"""
import speech_recognition as sr
import nltk
from nltk.corpus import stopwords
import xml.etree.ElementTree as ET
import ast

def voice():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        return str(r.recognize_google(audio))
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)
    
def diagnose(tokens, root):
    cnt = {}
    i = -1
    for mt in root.iter('Type'):
        i += 1
        cnt[mt] = 0
        for t in tokens:
            descrip = root[i][1].text.replace('"', "").replace("[", "").replace("]", "").replace(",", "").split()
            for td in descrip:
                if t == td:
                    cnt[mt] += 1
        if cnt[mt] != 0: # search for subtype
            for st in root[i].iter('Subtype'):
                cnt[st] = cnt[mt]
                descrip = st[1].text.replace('"', "").replace("[", "").replace("]", "").replace(",", "").split()
                for t in tokens:
                    for d in descrip:
                        if t == d:
                            cnt[st] += 1
                if cnt[st] == cnt[mt]: # not a valid subtype
                    cnt[st] = 0
    return max(cnt, key=cnt.get)

if __name__ == "__main__":
    tree = ET.parse('ArmyFirstAidOrganized.xml')
    root = tree.getroot()
    descrip = {}
    print("What is your emergency?")
    #s = voice()
    s = str(input("Enter your emergency: "))
    #s = 'A black spider bit me'
    tokens = nltk.word_tokenize(s.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    Type = diagnose(tokens, root)
    print(Type[0].text)