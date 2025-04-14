import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util
import answers as an
from voice import speak
import re
from datetime import datetime, timedelta
import spotify as spot

recognizer = sr.Recognizer()

def speechRecognition():
    with sr.Microphone() as source:
        recognizer.energy_threshold=1500
        recognizer.adjust_for_ambient_noise(source)  
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="sk-SK")
        text = text.strip().lower()
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

musicPhrases = {
    "play_song": {
        "en": [
            "play", "play song", "play music"
        ],
        "sk": [
            "pusti", "prehraj", "zapni hudbu", "pusti pesničku"
        ]
    },
    "pause": {
        "en":[
            "pause the music", "stop the music"
        ],
        "sk": [
            "zastav hudbu", "pauzni hudbu"
        ]
    },
    "start": {
        "en": [
            "resume", "continue the music"
        ],
        "sk": [
            "pokračuj", "pusti hudbu"
        ]
    }
}

musicEmbeddings = []
musicLabels = []
musicLanguages = []

for intent, lang_dict in musicPhrases.items():
    for lang, phrases in lang_dict.items():
        for phrase in phrases:
            musicEmbeddings.append(phrase)
            musicLabels.append(intent)
            musicLanguages.append(lang)

musicEmbeddings_ = model.encode(musicEmbeddings, convert_to_tensor=True)

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


def extractForecastDays(text, lang="en"):
    number_match = re.search(r"\b(\d+)\s*(day|days|dni)?", text)
    if number_match:
        return min(int(number_match.group(1)), 10) 

    today = datetime.now()
    lower = text.lower()

    if lang == "en":
        if "today" in lower:
            return 1
        elif "tomorrow" in lower:
            return 2
        elif "weekend" in lower:
            weekday = today.weekday()
            days_until_saturday = (5 - weekday) % 7
            return days_until_saturday + 2
        elif "next week" in lower:
            return 7
    elif lang == "sk":
        if "dnes" in lower:
            return 1
        elif "zajtra" in lower:
            return 2
        elif "víkend" in lower:
            weekday = today.weekday()
            days_until_saturday = (5 - weekday) % 7
            return days_until_saturday + 2
        elif "budúci týždeň" in lower or "buduci tyzden" in lower:
            return 7

    return 3

def awakening(userInput, embedding, langs):
    if not userInput:
        print("No input. Waiting.")
        return False, None
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

        if not userInput:
            print("Continuing listening.")
            continue
        awakened, lang = awakening(userInput, wakingEmbeddings, langWakeWords)

        if awakened:
            return lang 

import time

async def listener():
    while True:
        awakenedLang = waitForWaking()
        
        if awakenedLang == "en":
            speak("What's up?", "en")
        elif awakenedLang == "sk":
            speak("Počúvam", "sk")

        lastCommandTime = time.time()
        timeoutDuration = 30

        while True:
            if time.time() - lastCommandTime > timeoutDuration:
                speak("Going to sleep due to inactivity." if awakenedLang == "en" else "Prechádzam do režimu spánku pre nečinnosť.", awakenedLang)
                break

            userText = speechRecognition()
            if not userText:
                continue

            lastCommandTime = time.time()

            if awakenedLang == "en" and "go to sleep" in userText.lower() or "goodbye" in userText.lower():
                speak("Going to sleep.", "en")
                break
            elif awakenedLang == "sk" and ("choď spať" in userText.lower() or "dovidenia" in userText.lower()):
                speak("Idem spať.", "sk")
                break

            timeCommand, intent, lang = detectIntent(userText, timeEmbeddings, timePhrase_languages)
            if timeCommand:
                speak(an.whatsTheTime(lang), lang)
                continue

            weatherCommand, intent, lang = detectIntent(userText, weatherEmbeddings, wphraseLanguages, labels=wphraseLabels)
            if weatherCommand:
                if intent == "current_weather":
                    speak(await an.whatsTheWeather(lang), lang)
                elif intent == "hourly_forecast":
                    speak(await an.whatsHourlyForecast(lang), lang)
                elif intent == "daily_forecast":
                    days = extractForecastDays(userText, lang)
                    speak(await an.whatsDailyForecast(lang, days), lang)
                continue

            musicCommand, intent, lang = detectIntent(userText, musicEmbeddings_, musicLanguages, labels=musicLabels)
            if musicCommand:
                if intent == "play_song":
                    song = userText.replace("play", "").strip()
                    speak(an.nowPlaying(song, lang), lang)
                    spot.playSong(song)


                
