import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util
from answers import whatsTheTime, whatsTheWeather, whatsHourlyForecast
from voice import speak

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
    "current_weather": {
        "en": [
            "what's the weather like",
            "how's the weather",
            "what's the weather outside"
        ],
        "sk": [
            "aké je počasie",
            "ako je vonku",
            "aké je vonku počasie"
        ]
    },
    "hourly_forecast": {
        "en": [
            "what's the weather this evening",
            "what will the weather be like tonight",
            "forecast for later today"
        ],
        "sk": [
            "aké bude počasie večer",
            "bude pršať dnes večer",
            "predpoveď na dnešný večer"
        ]
    },
    "daily_forecast": {
        "en": [
            "what's the forecast for tomorrow",
            "weather for the weekend",
            "will it rain on friday"
        ],
        "sk": [
            "aká je predpoveď na zajtra",
            "aké bude počasie cez víkend",
            "bude pršať v piatok"
        ]
    }
}

wphraseEmbeddings = []
wphraseLabels = []
wphraseLanguages = []

for intent, lang_dict in weatherPhrases.items():
    for lang, phrases in lang_dict.items():
        for phrase in phrases:
            wphraseEmbeddings.append(phrase)
            wphraseLabels.append(intent)
            wphraseLanguages.append(lang)

weatherEmbeddings = model.encode(wphraseEmbeddings, convert_to_tensor=True)

def detectIntent(userInput, embedding, langs, threshold=0.6, labels=None):
    userEmbedding = model.encode(userInput, convert_to_tensor=True)
    similarityScores = util.cos_sim(userEmbedding, embedding)
    maxScore, bestIndex = similarityScores[0].max(dim=0)

    matched_label = labels[bestIndex.item()] if labels else None

    if maxScore.item() > threshold:
        return True, matched_label, langs[bestIndex.item()]
    else:
        return False, None, None

wakeWords = {
    "en": [
            "siri", 
            "hey siri"
        ],
    "sk": [
            "alexa",
            "hey alexa"
        ] 
    }

allWakeWords = []
langWakeWords = []

for lang, phrases in wakeWords.items():
    for phrase in phrases:
        allWakeWords.append(phrase)
        langWakeWords.append(lang)
        
wakingEmbeddings = model.encode(allWakeWords, convert_to_tensor=True)

def awakening(userInput, embedding, langs):
    userEmbedding = model.encode(userInput, convert_to_tensor=True)
    similarityScores = util.cos_sim(userEmbedding, embedding)
    maxScore, bestIndex = similarityScores[0].max(dim=0)
    if maxScore.item() > 0.6:
        detected_language = langs[bestIndex.item()]
        return True, detected_language
    else:
        return False, None

def waitForWaking():
    while True:
        userInput = speechRecognition()
        awakened, lang = awakening(userInput, wakingEmbeddings, langWakeWords)
        if awakened:
            return lang

async def listener():
    while True:
        awakenedLang = waitForWaking()
        if awakenedLang == "en":
            speak("What's up?", "en")
        elif awakenedLang == "sk":
            speak("Počúvam", "sk")
        userText = speechRecognition()
        timeCommand, lang = detectIntent(userText, timeEmbeddings, timePhrase_languages)
        if timeCommand:
           speak(whatsTheTime(lang), lang)
        else:
            weatherCommand, intent, lang = detectIntent(userText, weatherEmbeddings, wphraseLanguages, labels=wphraseLabels)
            if weatherCommand & intent=="current_weather":
                speak(await whatsTheWeather(lang), lang)
            elif weatherCommand & intent=="hourly_forecast":
                speak(await whatsHourlyForecast(lang), lang)