import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
import speech_recognition as sr
import pyttsx3 as talk
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
    print(tokens)
    cntTypes = {}
    for types in root.iter('Type'):
        cntTypes[types] = 0
        for t in tokens:
            descrip = ast.literal_eval(types[1].text)
            for td in descrip:
                if t == td:
                    cntTypes[types] += 1

    maxScore = 0
    maxScoreKey = ""
    for key in cntTypes:
        if cntTypes[key] > maxScore:
            maxScoreKey = key
            maxScore = cntTypes[key]
        else:
            continue
    maxScoreKeyString = maxScoreKey[0].text
    if maxScore == 0:
        return 0
    else:
        firstLoop = True
        while True:
            check = maxScoreKey.find('Subtype')
            if check == None:
                print("here")
                return maxScoreKey
                maxScoreKeyString = maxScoreKey[0].text
            else: 
                cntSTypes = {}
                for subTypes in maxScoreKey.iter('Subtype'):
                    cntSTypes[subTypes] = 0
                    for t in tokens:
                        descrip = ast.literal_eval(subTypes[1].text)
                        for td in descrip:
                            if t == td:
                                cntSTypes[subTypes] += 1
                
                if not firstLoop:
                    del cntSTypes[maxScoreKey]

                maxScoreSub = 0
                maxScoreKeySub = ""
                for key in cntSTypes:
                    if cntSTypes[key] > maxScoreSub:
                        maxScoreKeySub = key
                        maxScoreSub = cntSTypes[key]
                    else:
                        continue
                
                if maxScoreSub == 0:
                    return maxScoreKey
                else:
                    maxScoreKey = maxScoreKeySub
                    maxScoreKeyString = maxScoreKey[0].text
                    firstLoop = False






def stepThroughInstructions(emergencyType):
    # engine = talk.init()
    treatment = emergencyType.findall('Treatment')
    treatmentList = ast.literal_eval(treatment[0].text)
    counter = 0
    while counter < len(treatmentList): 
        # engine.say(treatmentList[counter])
        # engine.runAndWait()
        # response = voice()
        #print(response)
        response = input("\n\nResponse?\n\n")
        if response in ["next step", "Next Step", "next Step", "Next step"]:
            counter += 1
            continue
        elif response in ["repeat", "Repeat"]:
            continue
        else:
            print("none of the cases")
            continue




def main():
    # engine = talk.init()
    # engine.say("Hi Kate")
    # engine.runAndWait()
    tree = ET.parse('ArmyFirstAidOrganized.xml')
    query = input("\n\nWhat's your emergency?\n\n")
    emergencyType = diagnose(query, tree)
    stepThroughInstructions(emergencyType)



if __name__ == '__main__':
    main()
