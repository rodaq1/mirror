import getters as g
from googletrans import Translator
import asyncio
def whatsTheTime(lang, timeZone ="Europe/Bratislava"):
    dateTime = g.getTimeDate(timeZone)
    if lang == "en":
        answer = f"It's {dateTime['hour']}:{dateTime['minute']}"
        return answer
    elif lang == "sk":
        answer = f"Je {dateTime['hour']}:{dateTime['minute']}"
        return answer

async def whatsTheWeather(lang, location = "KysuckeNoveMesto"):
    weather = g.getCurrentWeather(location)
    if lang == "en":
        answer = f"Today, it's {weather['condition'].lower()} outside. The temperature is {weather['temp']} degrees Celsius, but it feels like {weather['feelsliketemp']} degrees. Wind is blowing at {weather['wind']} kilometers per hour, and the humidity is {weather['humidity']} percent."
        return answer
    elif lang == "sk":
        translator = Translator()
        condition = translator.translate(weather['condition'], dest='sk').text

        if condition.endswith("ý"):
            condition = condition[:-1] + "é"

        temp_noun = "stupňov Celzia" if weather['temp'] != 1 else "stupňa Celzia"  
        feelslike_noun = "stupňov" if weather['feelsliketemp'] != 1 else "stupňa"  
        wind_noun = "kilometrov za hodinu" if weather['wind'] != 1 else "kilometer za hodinu"
        
        answer = f"Dnes je vonku {condition.lower()}. Teplota je {weather['temp']} {temp_noun}, ale pocitová teplota je {weather['feelsliketemp']} {feelslike_noun}. Vietor fúka rýchlosťou {weather['wind']} {wind_noun} a vlhkosť vzduchu je {weather['humidity']} percent."
        return answer