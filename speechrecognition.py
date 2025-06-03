import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util
import answers as an
from voice import speak
import re
from datetime import datetime, timedelta
import spotify as spot
import traceback

recognizer = sr.Recognizer()

def speechRecognition():
    with sr.Microphone() as source:
        recognizer.energy_threshold=1500
        recognizer.adjust_for_ambient_noise(source)  
        try: 
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("niktoo nic nehovori lol")
    try:
        if audio:
            text = recognizer.recognize_google(audio, language="sk-SK")
            text = text.strip()
            print(f"text: {text}")
            return text
        else: 
            print("No audio detected.")
            return "Nerozumiem"
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
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
            "aké bude počasie zajtra",
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
            "play", "play song", "play music", "start playing", "play track", "put on", "listen to"
        ],
        "sk": [
            "pusti", "prehraj", "zapni hudbu", "pusti pesničku", "zahraj", "spusti hudbu", "počúvaj"
        ]
    },
    "pause": {
        "en": [
            "pause", "pause the music", "stop the music", "hold on", "pause playback"
        ],
        "sk": [
            "zastav hudbu", "pauzni hudbu", "pozastav", "pauza", "zastav prehrávanie"
        ]
    },
    "start": {
        "en": [
            "resume", "continue the music", "play again", "start playback", "unpause", "keep playing"
        ],
        "sk": [
            "pokračuj", "pusti hudbu", "spusti prehrávanie", "znovu pusti", "pokračuj v prehrávaní"
        ]
    },
    "toggle_play_pause": {
        "en": [
            "toggle play pause", "play or pause", "play/pause", "toggle music", "pause or play"
        ],
        "sk": [
            "zapni alebo zastav hudbu", "prehraj alebo pauzni", "zapni/pauzni", "prepnúť prehrávanie"
        ]
    },
    "stop": {
        "en": [
            "stop", "stop music", "stop playback", "end music", "turn off music"
        ],
        "sk": [
            "zastav", "zastav hudbu", "ukonči prehrávanie", "vypni hudbu", "stopni hudbu"
        ]
    },
    "next_track": {
        "en": [
            "next", "next song", "skip", "skip track", "next track", "skip to next"
        ],
        "sk": [
            "ďalšia", "ďalšia pesnička", "preskoč", "preskoč skladbu", "ďalší track"
        ]
    },
    "previous_track": {
        "en": [
            "previous", "previous song", "go back", "last track", "previous track", "go back song"
        ],
        "sk": [
            "predchádzajúca", "predchádzajúca pesnička", "choď späť", "posledný track", "predchádzajúci song"
        ]
    },
    "get_current_song": {
        "en": [
            "what is playing", "what song is this", "current song", "what's playing now", "tell me the song"
        ],
        "sk": [
            "čo hrá", "aká je táto pesnička", "aktuálna pesnička", "čo sa hrá teraz", "povedz mi pesničku"
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

import spacy

nlp = spacy.load("en_core_web_sm")

def extract_location_en(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":  
            return ent.text
    return None

import stanza

stanza.download("sk")
nlp = stanza.Pipeline("sk", processors="tokenize,mwt,pos,lemma", use_gpu=False)

places_sk = [
    "Bratislava", "Kosice", "Presov", "Zilina", "Nitra", "BanskaBystrica", "Trnava", "Trencin",
    "Martin", "Poprad", "Prievidza", "Zvolen", "PovazskaBystrica", "NoveZamky", "Michalovce",
    "SpisskaNovaVes", "Komarno", "Levice", "Bardejov", "LiptovskyMikulas", "Lucenec", "Pezinok",
    "Humenne", "Ruzomberok", "Topolcany", "DolnyKubin", "Skalica", "Trebisov", "Senica", "Cadca",
    "VranovnadToplou", "Hlohovec", "DunajskaStreda", "Partizanske", "Malacky", "Handlova",
    "Roznava", "VelkyKrtis", "StaraLubovna", "Puchov", "Revuca", "Senec", "Galanta", "KysuckeNoveMesto",
    "Levoca", "Tvrdosin", "Sala", "Snina", "ZiarnadHronom", "Brezno", "Svidnik", "Myjava", "Krupina",
    "Gelnica", "Medzilaborce", "Sabinov", "Ilava", "Detva", "TurcianskeTeplice", "Bytca", "Kezmarok",
    "Stropkov", "Sered", "NovaDubnica", "VelkeKapusany", "Kolarovo", "Samorin", "Modra", "NoveMestonadVahom",
    "VelkyMeder", "Sladkovicovo", "Rajec", "Sturovo", "Namestovo", "Filakovo", "Krompachy", "Secovce",
    "VelkeUlany", "Holic", "Gbely", "Zarnovica", "Hrinova", "Vrable", "Stupava",

    "Londyn",         # London
    "Pariz",          # Paris
    "Berlín",         # Berlin
    "Madrid",         # Madrid
    "Rim",            # Rome
    "Vieden",         # Vienna
    "Amsterdam",      # Amsterdam (same)
    "Brusel",         # Brussels
    "Varšava",        # Warsaw
    "Budapesť",       # Budapest
    "Praha",          # Prague
    "Dublin",         # Dublin (same)
    "Helsinky",       # Helsinki
    "Oslo",           # Oslo (same)
    "Stockholm",      # Stockholm (same)
    "Kodaň",          # Copenhagen
    "Lisabon",        # Lisbon
    "Atény",          # Athens
    "Rejkjavik",      # Reykjavik
    "Moskva",         # Moscow
    "Kyjev",          # Kiev
    "Belehrad",       # Belgrade
    "Záhreb",         # Zagreb
    "Sarajevo",       # Sarajevo (same)
    "Skopje",         # Skopje (same)
    "Tirana",         # Tirana (same)
    "Riga",           # Riga (same)
    "Vilnius",        # Vilnius (same)
    "Tallinn",        # Tallinn (same)

    "NewYork",        # New York
    "LosAngeles",     # Los Angeles
    "Chicago",        # Chicago
    "Houston",        # Houston
    "Phoenix",        # Phoenix
    "Philadelphia",   # Philadelphia
    "SanAntonio",     # San Antonio
    "SanDiego",       # San Diego
    "Dallas",         # Dallas
    "SanJose",        # San Jose
    "Toronto",        # Toronto
    "Vancouver",      # Vancouver
    "Montreal",       # Montreal
    "MexicoCity",     # Mexico City
    "Guadalajara",    # Guadalajara
    "Monterrey",      # Monterrey

    "SaoPaulo",       # São Paulo
    "RioDeJaneiro",   # Rio de Janeiro
    "BuenosAires",    # Buenos Aires
    "Lima",           # Lima
    "Bogota",         # Bogotá
    "Santiago",       # Santiago
    "Caracas",        # Caracas
    "Quito",          # Quito
    "LaPaz",          # La Paz

    "Tokio",          # Tokyo
    "Soul",           # Seoul
    "Shanghai",       # Shanghai (same)
    "Peking",         # Beijing
    "Bangkok",        # Bangkok (same)
    "Singapur",       # Singapore
    "Jakarta",        # Jakarta (same)
    "Bombaj",         # Mumbai
    "Delhi",          # Delhi (same)
    "Kalkata",        # Kolkata
    "Manila",         # Manila (same)
    "HoChiMinh",      # Ho Chi Minh City (usually Vietnamese name)
    "Teheran",        # Tehran
    "Dubaj",          # Dubai
    "TelAviv",        # Tel Aviv (same)
    "Istanbul",       # Istanbul (same)
    "HongKong",       # Hong Kong (same)

    "Kairo",          # Cairo
    "Lagos",          # Lagos (same)
    "Johannesburg",   # Johannesburg (same)
    "Nairobi",        # Nairobi (same)
    "AddisAbeba",     # Addis Ababa
    "Casablanca",     # Casablanca (same)
    "Accra",          # Accra (same)
    "Kampala",        # Kampala (same)
    "DarEsSalaam",    # Dar es Salaam (same)
    "Tunis",          # Tunis (same)

    "Sydney",         # Sydney (same)
    "Melbourne",      # Melbourne (same)
    "Auckland",       # Auckland (same)
    "Brisbane",       # Brisbane (same)
    "Perth",          # Perth (same)
    "Wellington"      # Wellington (same)
]
import unicodedata

def remove_diacritics(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

from rapidfuzz import process

def find_closest_city(word, places, threshold=80):
    word_norm = remove_diacritics(word.lower())
    normalized_places = [remove_diacritics(p.lower()) for p in places]

    results = process.extract(word_norm, normalized_places, limit=1, score_cutoff=threshold)
    if results:
        best_match = results[0][0]
        idx = normalized_places.index(best_match)
        return places[idx]
    return None

def extract_location_sk(text):
    doc = nlp(text)
    normalized_places = [remove_diacritics(p.lower()) for p in places_sk]

    for sent in doc.sentences:
        for word in sent.words:
            lemma_norm = remove_diacritics(word.lemma.lower())
            print(f"Checking lemma: {word.lemma} -> normalized: {lemma_norm}")
            if lemma_norm in normalized_places:
                idx = normalized_places.index(lemma_norm)
                print(f"Found exact match: {places_sk[idx]}")
                return places_sk[idx]

    for sent in doc.sentences:
        for word in sent.words:
            city = find_closest_city(word.lemma, places_sk)
            if city:
                print(f"Found fuzzy match: {city}")
                return city

    print("No location found")
    return None

from googletrans import Translator

translator = Translator()
from googletrans import Translator

translator = Translator()

def extract_location(text, lang):
    if lang == "en":
        location = extract_location_en(text)  
        if location:
            return translator.translate(location, dest='en').text
        return None

    elif lang == "sk":
        location = extract_location_sk(text)  
        if location:
            return translator.translate(location, dest='en').text
        return None

    return None



import time
from langdetect import detect

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

            lang = detect(userText)
            if awakenedLang == "en" and "go to sleep" in userText.lower() or "goodbye" in userText.lower():
                speak("Going to sleep.", "en")
                break
            elif awakenedLang == "sk" and ("choď spať" in userText.lower() or "dovidenia" in userText.lower()):
                speak("Idem spať.", "sk")
                break

            timeCommand, intent, lang = detectIntent(userText, timeEmbeddings, timePhrase_languages)
            if timeCommand:
                if "v " in userText.lower() or "in " in userText.lower() or "vo " in userText.lower():
                    location = extract_location(userText, lang)
                    speak(an.whatsTheTime(lang, location = location), lang)
                else:
                    speak(an.whatsTheTime(lang), lang)
                continue

            weatherCommand, intent, lang = detectIntent(userText, weatherEmbeddings, wphraseLanguages, labels=wphraseLabels)
            if weatherCommand:
                location = extract_location(userText, lang)
                if intent == "current_weather":
                    speak(await an.whatsTheWeather(lang, location), lang)
                elif intent == "hourly_forecast":
                    speak(await an.whatsHourlyForecast(lang, location), lang)
                elif intent == "daily_forecast":
                    days = extractForecastDays(userText, lang)
                    speak(await an.whatsDailyForecast(lang, days, location), lang)
                continue

            musicCommand, intent, lang = detectIntent(userText, musicEmbeddings_, musicLanguages, labels=musicLabels)
            if musicCommand:
                if intent == "play_song":
                    triggers = musicPhrases["play_song"].get(lang, [])
                    song = userText.lower()
                    for phrase in triggers:
                        if phrase in song:
                            song = song.replace(phrase, "").strip()
                            break
                    if song:
                        speak(an.nowPlaying(song, lang), lang)
                        spot.play_song(song)
                    else:
                        speak("Please specify a song name.", lang)
            
                elif intent == "pause":
                    speak("Pausing music.", lang)
                    spot.pause()
            
                elif intent == "start":
                    speak("Resuming music.", lang)
                    spot.resume()
            
                elif intent == "toggle_play_pause":
                    speak("Toggling play/pause.", lang)
                    spot.toggle_play_pause()
            
                elif intent == "stop":
                    speak("Stopping playback.", lang)
                    spot.stop()
            
                elif intent == "next_track":
                    speak("Skipping to next track.", lang)
                    spot.next_track()
            
                elif intent == "previous_track":
                    speak("Going back to previous track.", lang)
                    spot.previous_track()
            
                elif intent == "get_current_song":
                    current = spot.get_current_song()
                    speak(current, lang)
            if not (timeCommand or weatherCommand or musicCommand):
                try:
                    lang = detect(userText)
                    response = an.geminiAnswer(userText)
                    if response:
                        speak(response, lang)
                    else:
                        speak("I didn't understand that." if lang=="en" else "Prepáč, nerozumiem.")
                except Exception as e:
                    print("Gemini error:", e)
                    speak("Sorry, something went wrong while answering." if lang=="en" else "Prepáč, niečo sa pri odpovedaní pokazilo.", lang)