import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
import speech_recognition as sr
import pyttsx3 as talk
import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import xml.etree.ElementTree as ET
import ast
from find_youtube_video import find_video
from GoogleSearchFunctions import whatQuestions, whereQuestions


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
        #if there are no longer any more specific subtypes
        if len(subTypes) == 0:
            return maxScoreKey
        #if they bet more specific
        else: 
            score, matchType = selectSubType(subTypes, tokens)
            
            if score == 0:
                maxScoreKey = diagnoseOptions(maxScoreKey, tokens)
            else:
                maxScoreKey = matchType

#takes in the subTypes you're currenlty at the the tokens from speech and returns the closest matching subtype and it's score
def selectSubType(subTypes, tokens):
    cntSTypes = {}
    #goes through each of the subtype's descriptors and sees if the statement can match to any of those
    for subType in subTypes:
        cntSTypes[subType] = 0
        for t in tokens:
            descrip = ast.literal_eval(subType[1].text)
            for td in descrip:
                if t == td:
                    cntSTypes[subType] += 1
    score = 0
    matchType = ""
    #sets matchtype to the highest scoring subtype and score to whatever the score for that was
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
    #prints out whatever the question element is
    q = type.find('Question')
    print(q.text)
    print("\nHere are the options:\n")
    counter = 0
    subTypes = type.findall('Type')
    #prints all of the options
    for st in subTypes:
        print(str(counter) + ". " + st[0].text + "\n")
        counter += 1
    while True:
        selection = input("\nWhich option is it?")
        isAQuestion = isQuestion(selection)
        while isAQuestion:
            result = diagnoseQuestionResponse(selection, subTypes)
            if result == 1:
                selection = input("\nWhich option is it?")
                if isQuestion(selection):
                    continue
                else:
                    isAQuestion = False
            else:
                selection = input("\nCould you please repeat that? We couldn't understand the question.")
                continue

        tokens = removeStopWords(selection)
        #gets the score and type from the given statement and checks if can reach a conclusion from that
        score, matchType = selectSubType(subTypes, tokens)
        if score == 0:
            print("Could you please repeat that? Please make sure to say the written option not the number associated with it. \n")
            continue
        else:
            return matchType

def diagnoseQuestionResponse(query, subTypes):
    tokens = nltk.word_tokenize(query.lower())
    plural = False
    if "these" in tokens or ("those" in tokens):
        plural = True

    if "where" in tokens:
        if plural:
            for st in subTypes:
                whereQuestionsCaller("where is the " + st[0].text)
                return 1
        else:
            matchType = selectSubType(subTypes, tokens)[1]
            whereQuestionsCaller("where is the " + matchType[0].text)
            return 1
            
    elif "what" in tokens:
        response = input("\n Would you also like to see images?")
        if response == "yes":
            pics = True
        else:
            pics = False

        if plural:
            for st in subTypes:
                whatQuestionsCaller("what is a " + st[0].text)
                if pics:
                    whereQuestionsCaller("what is a" + st[0].text)
            return 1
        else:
            matchType = selectSubType(subTypes, tokens)[1]
            whatQuestionsCaller("what is a " + matchType[0].text)
            if pics:
                whereQuestionsCaller("what is a" + st[0].text)
            return 1
    else:
        return 0
        

def whereQuestionsCaller(query):
    whereQuestions(query)

def whatQuestionsCaller(query):
    whatQuestions(query)

def howQuestions(query):
    find_video(query)

def isQuestion(query):
    questionWords = ["what", "where", "how"]
    tokens = nltk.word_tokenize(query.lower())
    for token in tokens:
        if token in questionWords:
            return True
        else:
            continue
    
    return False

def stepsQuestionResponse(query, step):
    tokens = nltk.word_tokenize(query.lower())
    if "that" in tokens or (len(tokens)<5):
        vague = True
    else: 
        vague = False
    
    if "where" in tokens:
        if vague:
            taggedQ = pos_tag(query.split())
            pNouns = [word for word,pos in taggedQ if pos == "NNP"]
            qString = ' '.join(pNouns)
            whereQuestionsCaller("where is the: " + qString)
        else:
            whereQuestionsCaller(qString)
        return 1
            
    elif "what" in tokens:
        if vague:
            taggedQ = pos_tag(query.split())
            pNouns = [word for word,pos in taggedQ if pos == "NNP"]
            qString = ' '.join(pNouns)
            whatQuestionsCaller("what is a: " + qString)
            response = input("\n Would you also like an image?")
            if response == "yes":
                whereQuestionsCaller("what is a" + qString)   
        else:
            whatQuestionsCaller(query)
            response = input("\n Would you also like an image?")
            if response == "yes":
                whereQuestionsCaller("what is a" + qString) 
        return 1

    elif "how" in tokens:
        if vague:
            whatQuestionsCaller("how to: " + step)
            response = input("\n Do you also want a video?")
            if response == "yes":
                howQuestions(query)
        else:
            whatQuestionsCaller("how to: " + step)
            response = input("\n Do you also want a video?")
            if response == "yes":
                howQuestions(query)
        return 1
    else:
        return 0


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
        elif isQuestion(response):
            stepsQuestionResponse(response, treatmentList[counter])
        else:
            print("I couldn't quite get that. Could you please repeat")
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
    stepThroughInstructions(emergencyType)

if __name__ == '__main__':
    main()
