import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util
from answers import whatsTheTime, whatsTheWeather

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

timeAll_phrases = []
timePhrase_languages = []

for lang, phrases in timePhrases.items():
    for phrase in phrases:
        timeAll_phrases.append(phrase)
        timePhrase_languages.append(lang)

timeEmbeddings = model.encode(timeAll_phrases, convert_to_tensor=True)

weatherPhrases = {
    "en": [
        "what's the weather like",
        "how's the weather",
        "how's the weather outside"
    ],
    "sk": [
        "aké je počasie",
        "ako je vonku",
        "aké je vonku počasie"
    ]
}

weatherAll_phrases = []
weatherPhrase_languages = []

for lang, phrases in weatherPhrases.items():
    for phrase in phrases:
        weatherAll_phrases.append(phrase)
        weatherPhrase_languages.append(lang)

weatherEmbeddings = model.encode(weatherAll_phrases, convert_to_tensor=True)

def isXCommand(userInput, embedding, langs):
    userEmbedding = model.encode(userInput, convert_to_tensor=True)
    similarityScores = util.cos_sim(userEmbedding, embedding)
    maxScore, bestIndex = similarityScores[0].max(dim=0)
    if maxScore.item() > 0.6:
        detected_language = langs[bestIndex.item()]
        return True, detected_language
    else:
        return False, None

async def listener():
    while True:
        print("pocuvam ta")
        userText = speechRecognition()
        timeCommand, lang = isXCommand(userText, timeEmbeddings, timePhrase_languages)
        if timeCommand:
           print(whatsTheTime(lang))
        else:
            weatherCommand, lang = isXCommand(userText, weatherEmbeddings, weatherPhrase_languages)
            if weatherCommand:
                print(await whatsTheWeather(lang))