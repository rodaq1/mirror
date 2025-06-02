import getters as g
from googletrans import Translator
import asyncio
import aiSetup as genai
import google.generativeai as gen

translator = Translator()

    
def format_temp_slovak(value, noun):
    if isinstance(value, float) and not value.is_integer():
        int_part = int(value)
        dec_part = str(value).split('.')[1][:2].rstrip('0')  
        return f"{int_part} celých {dec_part} {noun}"
    return f"{int(value)} {noun}"

locative_map = {
    "Bratislava": "Bratislave",
    "Kosice": "Košiciach",
    "Presov": "Prešove",
    "Zilina": "Žiline",
    "Nitra": "Nitre",
    "BanskaBystrica": "Banskej Bystrici",
    "Trnava": "Trnave",
    "Trencin": "Trenčíne",
    "Martin": "Martine",
    "Poprad": "Poprade",
    "Prievidza": "Prievidzi",
    "Zvolen": "Zvolene",
    "PovazskaBystrica": "Považskej Bystrici",
    "Michalovce": "Michalovciach",
    "SpisskaNovaVes": "Spišskej Novej Vsi",
    "Komarno": "Komárne",
    "Levice": "Leviciach",
    "Bardejov": "Bardejove",
    "LiptovskyMikulas": "Liptovskom Mikuláši",
    "Lucenec": "Lučeneci",
    "Pezinok": "Pezinku",
    "Humenne": "Humennom",
    "Ruzomberok": "Ružomberku",
    "Topolcany": "Topoľčanoch",
    "DolnyKubin": "Dolnom Kubíne",
    "Skalica": "Skalici",
    "Trebisov": "Trebišove",
    "Senica": "Senici",
    "Cadca": "Čadci",
    "VranovnadToplou": "Vranove nad Topľou",
    "Hlohovec": "Hlohovci",
    "DunajskaStreda": "Dunajskej Strede",
    "Partizanske": "Partizánskom",
    "Malacky": "Malackách",
    "Handlova": "Handlove",
    "Roznava": "Rožňave",
    "VelkyKrtis": "Veľkom Krtíši",
    "StaraLubovna": "Starej Ľubovni",
    "Puchov": "Púchove",
    "Revuca": "Revúcej",
    "Senec": "Seneci",
    "Galanta": "Galante",
    "KysuckeNoveMesto": "Kysuckom Novom Meste",
    "Kysucke Nove Mesto": "Kysuckom Novom Meste",
    "Levoca": "Levoči",
    "Tvrdosin": "Tvrdosíne",
    "Sala": "Šali",
    "Snina": "Snine",
    "ZiarnadHronom": "Žiaru nad Hronom",
    "Brezno": "Brezne",
    "Svidnik": "Svidníku",
    "Myjava": "Myjave",
    "Krupina": "Krupine",
    "Gelnica": "Gelnici",
    "Medzilaborce": "Medzilaborciach",
    "Sabinov": "Sabinove",
    "Ilava": "Ilave",
    "Detva": "Detve",
    "TurcianskeTeplice": "Turčianskych Tepliciach",
    "Bytca": "Bytči",
    "Kezmarok": "Kežmarku",
    "Stropkov": "Stropkove",
    "Sered": "Seredi",
    "NovaDubnica": "Novej Dubnici",
    "VelkeKapusany": "Veľkých Kapušanoch",
    "Kolarovo": "Kolárove",
    "Samorin": "Šamoríne",
    "Modra": "Modre",
    "NoveMestonadVahom": "Novom Meste nad Váhom",
    "VelkyMeder": "Veľkom Mederi",
    "Sladkovicovo": "Sládkovičove",
    "Rajec": "Rajci",
    "Sturovo": "Štúrove",
    "Namestovo": "Námestove",
    "Filakovo": "Fiľakove",
    "Krompachy": "Krompachoch",
    "Secovce": "Sečovciach",
    "VelkeUlany": "Veľkých Úľanoch",
    "Holic": "Holíči",
    "Gbely": "Gbeľoch",
    "Zarnovica": "Žarnovici",
    "Hrinova": "Hriňovej",
    "Vrable": "Vrábľoch",
    "Stupava": "Stupave",

    "London": "Londýne",
    "Paris": "Paríži",
    "Berlin": "Berlíne",
    "Madrid": "Madride",
    "Rome": "Ríme",
    "Vienna": "Viedni",
    "Amsterdam": "Amsterdame",
    "Brussels": "Bruseli",
    "Warsaw": "Varšave",
    "Budapest": "Budapešti",
    "Prague": "Prahe",
    "Dublin": "Dublině",
    "Helsinki": "Helsinkách",
    "Oslo": "Osle",
    "Stockholm": "Štokholme",
    "Copenhagen": "Kodani",
    "Lisbon": "Lisabone",
    "Athens": "Aténach",
    "Reykjavik": "Rejkjaviku",
    "Moscow": "Moskve",
    "Kyiv": "Kyjeve",
    "Belgrade": "Belehrade",
    "Zagreb": "Záhrebe",
    "Sarajevo": "Sarajeve",
    "Skopje": "Skopje",
    "Tirana": "Tirane",
    "Riga": "Rige",
    "Vilnius": "Vilniuse",
    "Tallinn": "Tallinne",

    "New York": "New Yorku",
    "Los Angeles": "Los Angelesi",
    "Chicago": "Chicagu",
    "Houston": "Houstone",
    "Phoenix": "Phoenixe",
    "Philadelphia": "Philadelphii",
    "San Antonio": "San Antoniu",
    "San Diego": "San Diegu",
    "Dallas": "Dallase",
    "San Jose": "San Jose",
    "Toronto": "Toronte",
    "Vancouver": "Vancouveri",
    "Montreal": "Montreale",
    "Mexico City": "Mexiku",
    "Guadalajara": "Guadalajare",
    "Monterrey": "Monterreyi",

    "São Paulo": "São Paule",
    "Rio de Janeiro": "Riu de Janeiro",
    "Buenos Aires": "Buenos Aires",
    "Lima": "Lime",
    "Bogotá": "Bogote",
    "Santiago": "Santiagu",
    "Caracas": "Caracase",
    "Quito": "Quite",
    "La Paz": "La Pazi",

    "Tokyo": "Tokiu",
    "Seoul": "Soule",
    "Shanghai": "Šanghaji",
    "Beijing": "Pekingu",
    "Bangkok": "Bangkoku",
    "Singapore": "Singapure",
    "Jakarta": "Jakarte",
    "Mumbai": "Bombaji",
    "Delhi": "Delhí",
    "Kolkata": "Kalkate",
    "Manila": "Manile",
    "Ho Chi Minh City": "Ho Chi Minhovi",
    "Tehran": "Teheráne",
    "Dubai": "Dubaji",
    "Tel Aviv": "Tel Avive",
    "Istanbul": "Istanbule",
    "Hong Kong": "Hongkongu",

    "Cairo": "Káire",
    "Lagos": "Lagosu",
    "Johannesburg": "Johannesburgu",
    "Nairobi": "Nairobi",
    "Addis Ababa": "Addis Abebe",
    "Casablanca": "Casablance",
    "Accra": "Accre",
    "Kampala": "Kampale",
    "Algiers": "Alžíri",
}

def get_locative_form(city, city_dict):
   
    return city_dict.get(city, city)  

def whatsTheTime(lang, location ="Kysucke Nove Mesto"):
    if location == None:
        location = "Kysucke nove mesto"
    print(f"WhastTheTime called with location: {location}")

    dateTime = g.getTimeDate(location)
    print(f"getTimeInfo returned: {dateTime}")

    if lang == "en":
        answer = f"It's {dateTime['hour']}:{dateTime['minute']} in {location}"
        return answer
    elif lang == "sk":
        location = get_locative_form(location, locative_map)
        answer = f"Je {dateTime['hour']}:{dateTime['minute']} v {location}"
        return answer

from datetime import datetime
def convert_am_pm_to_slovak(time_str):
    try:
        dt = datetime.strptime(time_str.strip(), "%I:%M %p")
        return dt.strftime("%H:%M")
    except ValueError:
        return None

async def whatsTheWeather(lang, location):
    if not location:
        print("[INFO] No location detected. Using default 'KysuckeNoveMesto'.")
        location = "KysuckeNoveMesto"
    
    weather = g.getCurrentWeather(location)
    if not weather:
        return "Prepáč, neviem získať počasie pre túto lokalitu." if lang == "sk" else "Sorry, I couldn't get the weather for this location."
    if lang == "en":
        answer = f"Currently, it's {weather['condition'].lower()} in {location} outside. The temperature is {weather['temp']} degrees Celsius and it feels like {weather['feelsliketemp']} degrees. Wind is blowing at {weather['wind']} kilometers per hour, and the humidity is {weather['humidity']} percent."
        return answer
    elif lang == "sk":
        condition = translator.translate(weather['condition'], dest='sk').text

        if condition.endswith("ý"):
            condition = condition[:-1] + "é"

        temp_noun = "stupňov Celzia" if weather['temp'] != 1 else "stupňa Celzia"  
        feelslike_noun = "stupňov" if weather['feelsliketemp'] != 1 else "stupňa"  
        wind_noun = "kilometrov za hodinu" if weather['wind'] != 1 else "kilometer za hodinu"
        temp_formatted = format_temp_slovak(weather['temp'], temp_noun)
        feelslike_formatted = format_temp_slovak(weather['feelsliketemp'], feelslike_noun)
        wind_formatted = format_temp_slovak(weather['wind'], wind_noun)
        if location:
            location_in_locative = get_locative_form(location, locative_map)
        answer = f"Momentálne je v {location_in_locative} {condition.lower()}. Teplota je {temp_formatted}, pocitová teplota je {feelslike_formatted}. Vietor fúka rýchlosťou {wind_formatted} a vlhkosť vzduchu je {weather['humidity']} percent."
        return answer
    
async def whatsHourlyForecast(lang, location="KysuckeNoveMesto", desiredHour=12):
    if not location:
        print("[INFO] No location detected. Using default 'KysuckeNoveMesto'.")
        location = "KysuckeNoveMesto"
    forecast = g.getForecast(location, 1)
    hourlyForecast = g.getHourlyForecast(forecast)

    firstHour = max(0, desiredHour - 4)
    lastHour = min(len(hourlyForecast), desiredHour + 5)

    if lang == "en":
        answer = f"Here's an overview of today's weather by hour in {location}:\n"
        for hour in hourlyForecast[firstHour:lastHour]:
            hour_info = f"{hour['time']}: {hour['temp_c']}°C, {hour['condition']}"
            if hour.get('chance_of_rain', 0) > 0:
                hour_info += f", {hour['chance_of_rain']}% chance of rain"
            elif hour.get('chance_of_snow', 0) > 0:
                hour_info += f", {hour['chance_of_snow']}% chance of snow"
            answer += hour_info + "\n"
        return answer.strip()

    elif lang == "sk":
        location_in_locative = get_locative_form(location, locative_map)
        answer = f"Tu je prehľad dnešného počasia po hodinách v {location_in_locative}:\n"
        for hour in hourlyForecast[firstHour:lastHour]:
            condition = translator.translate(hour['condition'], dest='sk').text
            if condition.endswith("ý"):
                condition = condition[:-1] + "é"
            temp_formatted = format_temp_slovak(hour['temp_c'], "stupňov Celzia")
            time = convert_am_pm_to_slovak(hour['time'])
            hour_info = f"{time}: {temp_formatted}, {condition.lower()}"
            if hour.get('chance_of_rain', 0) > 0:
                hour_info += f", {hour['chance_of_rain']}% pravdepodobnosť dažďa"
            elif hour.get('chance_of_snow', 0) > 0:
                hour_info += f", {hour['chance_of_snow']}% pravdepodobnosť snehu"
            answer += hour_info + "\n"
        return answer.strip()


async def whatsDailyForecast(lang, days, location="KysuckeNoveMesto"):
    if not location:
        print("[INFO] No location detected. Using default 'KysuckeNoveMesto'.")
        location = "KysuckeNoveMesto"
    forecast = g.getForecast(location, days)
    dailyForecast = g.getDailyForecast(forecast)
    
    if lang == "en":
        answer = f"Here's the daily weather forecast for {location}:\n"
        for day in dailyForecast:
            answer += (
                f"{day['date']}: {day['condition']}, "
                f"low of {day['min_temp']}°C, high of {day['max_temp']}°C, "
                f"sunrise at {day['sunrise']}, sunset at {day['sunset']}.\n"
            )
        return answer.strip()

    elif lang == "sk":
        location_in_locative = get_locative_form(location, locative_map)
        answer = f"Tu je denná predpoveď počasia pre {location_in_locative}:\n"
        for day in dailyForecast:
            condition = translator.translate(day['condition'], dest='sk').text
            if condition.endswith("ý"):
                condition = condition[:-1] + "é"
            min_temp_formatted = format_temp_slovak(day['min_temp'], "stupňov Celzia")
            max_temp_formatted = format_temp_slovak(day['max_temp'], "stupňov Celzia")
            sunrise = convert_am_pm_to_slovak(day['sunrise'])
            sunset = convert_am_pm_to_slovak(day['sunset'])
            answer += (
                f"{day['date']}: {condition.lower()}, "
                f"od {min_temp_formatted} do {max_temp_formatted}, "
                f"východ slnka o {sunrise}, západ slnka o {sunset}.\n"
            )
        return answer.strip()

def nowPlaying(song, lang):
    if lang == "en":
        answer = f"Now playing {song} on spotify"
    elif lang == "sk":
        answer = f"Púšťam {song} cez spotify"
    return answer

from langdetect import detect

def geminiAnswer(question):
    gen.configure(api_key="AIzaSyDeZyH_yeLW8iDVHYVUHUkO2uvp4qWjeRA")
    model = gen.GenerativeModel('gemini-1.5-flash')

    try:
        lang = detect(question)
        if lang.startswith("sk"):
            prompt = (
                question + 
                "\n\nOdpovedz ako hlasový asistent. Odpoveď má byť hovorená, prirodzená, nie dlhšia ako 5–6 viet. Nerozprávaj sa o tomto texte ani o hlasovom asistentovi, len odpovedz na otázku."
            )
        else:
            lang = "en"
            prompt = (
                question + 
                "\n\nAnswer like a voice assistant. The answer should be spoken, natural, no longer than 5–6 sentences. Do not talk about this prompt, just answer the question."

            )

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"Gemini error: {e}")
        return "Sorry, I couldn't find the answer."
        
