import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util
from answers import whatsTheTime

recognizer = sr.Recognizer()

def speechRecognition():
    with sr.Microphone() as source:
        print(" ovor...")
        recognizer.energy_threshold=1500
        recognizer.adjust_for_ambient_noise(source)  
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="sk-SK")
        text = text.strip().lower()
        print(text)
        return text
    except Exception as e:
        print(f"chybicka {e}")
        return None


#listener pre commandy
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
timePhrases = {
    "en": [
        "what's the time",
        "what time is it"
    ],
    "sk": [
        "koľko je hodín",
        "aký je čas",
        "koľko je teraz"
    ]
}

all_phrases = []
phrase_languages = []

for lang, phrases in timePhrases.items():
    for phrase in phrases:
        all_phrases.append(phrase)
        phrase_languages.append(lang)

timeEmbeddings = model.encode(all_phrases, convert_to_tensor=True)

def isTimeCommand(userInput):
    userEmbedding = model.encode(userInput, convert_to_tensor=True)
    similarityScores = util.cos_sim(userEmbedding, timeEmbeddings)
    maxScore, bestIndex = similarityScores[0].max(dim=0)
    if maxScore.item() > 0.6:
        detected_language = phrase_languages[bestIndex.item()]
        return True, detected_language
    else:
        return False, None
def listener():
    while True:
        print("pocuvam ta")
        userText = speechRecognition()
        timeCommand, lang = isTimeCommand(userText)
        if timeCommand:
           print(whatsTheTime(lang))