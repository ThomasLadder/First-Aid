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
    if maxScore == 0:
        return 0
    else:
        while True:
            subTypes = maxScoreKey.findall('Subtype')
            if len(subTypes) == 0:
                return maxScoreKey
            else: 
                cntSTypes = {}
                for subType in subTypes:
                    cntSTypes[subType] = 0
                    for t in tokens:
                        descrip = ast.literal_eval(subType[1].text)
                        for td in descrip:
                            if t == td:
                                cntSTypes[subType] += 1
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
    root = tree.getroot()
    tokens = nltk.word_tokenize(query.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    emergencyType = diagnose(tokens, root)
    stepThroughInstructions(emergencyType)



if __name__ == '__main__':
    main()
