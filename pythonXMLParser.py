import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
import speech_recognition as sr
import pyttsx3 as talk
import nltk
from nltk.corpus import stopwords
import xml.etree.ElementTree as ET
import ast


#Call this function whenever you're using the voice functionality
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



#The initial diagonse
#iterates through until lands on the most specific option
#returns the xml element
def diagnose(tokens, root):
    maxScoreKey = root
    while True:
        subTypes = maxScoreKey.findall('Type')
        if len(subTypes) == 0:
            return maxScoreKey
        else: 
            score, matchType = selectSubType(subTypes, tokens)
            
            if score == 0:
                maxScoreKey = diagnoseOptions(maxScoreKey, tokens)
            else:
                maxScoreKey = matchType

#takes in the subTypes you're currenlty at the the tokens from speech and returns the closest matching subtype and it's score
def selectSubType(subTypes, tokens):
    cntSTypes = {}
    for subType in subTypes:
        cntSTypes[subType] = 0
        for t in tokens:
            descrip = ast.literal_eval(subType[1].text)
            for td in descrip:
                if t == td:
                    cntSTypes[subType] += 1
    score = 0
    matchType = ""
    for key in cntSTypes:
        if cntSTypes[key] > score:
            matchType = key
            score = cntSTypes[key]
        else:
            continue

    return score, matchType

#called when the user hasn't given enough initial information to get to a specific diagnoses
#returns the diagnoses at the next level of specificity
def diagnoseOptions(type, tokens):
    q = type.find('Question')
    print(q.text)
    print("\nHere are the options:\n")
    counter = 0
    subTypes = type.findall('Type')
    for st in subTypes:
        print(str(counter) + ". " + st[0].text + "\n")
        counter += 1
    while True:
        selection = input("which option is it?")
        tokens = removeStopWords(selection)
        score, matchType = selectSubType(subTypes, tokens)
        if score == 0:
            print("Could you please repeat that? \n")
            continue
        else:
            return matchType





#steps through the instructions
def stepThroughInstructions(emergencyType):
    # engine = talk.init()
    treatment = emergencyType.findall('Treatment')
    treatmentList = ast.literal_eval(treatment[0].text)
    counter = 0
    while counter < len(treatmentList): 
        print(treatmentList[counter])
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

#removes irrelevant words and returns a list of the token words
def removeStopWords(query):
    tokens = nltk.word_tokenize(query.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens
    



def main():
    # engine = talk.init()
    # engine.say("Hi Kate")
    # engine.runAndWait()
    tree = ET.parse('ArmyFirstAidOrganized.xml')
    query = input("\n\nWhat's your emergency?\n\n")
    root = tree.getroot()
    tokens = removeStopWords(query)
    emergencyType = diagnose(tokens, root)
    print(emergencyType[0].text)
    # stepThroughInstructions(emergencyType)



if __name__ == '__main__':
    main()
