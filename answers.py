import getters as g
from googletrans import Translator
import asyncio

translator = Translator()


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
        answer = f"Currently, it's {weather['condition'].lower()} outside. The temperature is {weather['temp']} degrees Celsius, but it feels like {weather['feelsliketemp']} degrees. Wind is blowing at {weather['wind']} kilometers per hour, and the humidity is {weather['humidity']} percent."
        return answer
    elif lang == "sk":
        condition = translator.translate(weather['condition'], dest='sk').text

        if condition.endswith("ý"):
            condition = condition[:-1] + "é"

        temp_noun = "stupňov Celzia" if weather['temp'] != 1 else "stupňa Celzia"  
        feelslike_noun = "stupňov" if weather['feelsliketemp'] != 1 else "stupňa"  
        wind_noun = "kilometrov za hodinu" if weather['wind'] != 1 else "kilometer za hodinu"
        
        answer = f"Momentálne je vonku {condition.lower()}. Teplota je {weather['temp']} {temp_noun}, ale pocitová teplota je {weather['feelsliketemp']} {feelslike_noun}. Vietor fúka rýchlosťou {weather['wind']} {wind_noun} a vlhkosť vzduchu je {weather['humidity']} percent."
        return answer
    
async def whatsHourlyForecast(lang, location = "KysuckeNoveMesto", desiredHour=12):
    forecast = g.getForecast(location, 1)
    hourlyForecast = g.getHourlyForecast(forecast)

    firstHour = desiredHour - 4
    lastHour = desiredHour + 4

    answer = ""

    if lang == "en":
        answer = f"Here's an overview of today's weather, hourly: "
        for hour in hourlyForecast[firstHour:lastHour]:
            hour_info = f"{hour['time']} - {hour['temp_c']}°C, {hour['condition']}"
            if hour['chance_of_rain'] > 0:
                hour_info += f", {hour['chance_of_rain']}% chance of rain"
            elif hour['chance_of_snow'] > 0:
                hour_info += f", {hour['chance_of_snow']}% chance of snow"
            answer += f"{hour_info}; "

        answer = answer.rstrip("; ") 
    elif lang == "sk":
        answer = f"Tu je prehľad dnešného počasia po hodinách: "
        for hour in hourlyForecast[firstHour:lastHour]:
            condition = translator.translate(hour['condition'], dest='sk').text

            if condition.endswith("ý"):
                condition = condition[:-1] + "é"

            hour_info = f"{hour['time']} - {hour['temp_c']}°C, {condition}"
            if hour['chance_of_rain'] > 0:
                hour_info += f", {hour['chance_of_rain']}% pravdepodobnosť dažďa"
            elif hour['chance_of_snow'] > 0:
                hour_info += f", {hour['chance_of_snow']}% pravdepodobnosť snehu"
            answer += f"{hour_info}; "

        answer = answer.rstrip("; ")

    return answer

async def whatsDailyForecast(lang, days, location = "KysuckeNoveMesto"):
    forecast = g.getForecast(location, days)
    dailyForecast = g.getDailyForecast(forecast)

    answer = ""

    if lang == "en":
        answer = "Here's the daily weather forecast:\n"
        for day in dailyForecast:
            answer += (
                f"{day['date']}: {day['condition']}, "
                f"{day['min_temp']}°C to {day['max_temp']}°C, "
                f"sunrise at {day['sunrise']}, sunset at {day['sunset']}.\n"
            )

    elif lang == "sk":
        answer = "Tu je denná predpoveď počasia:\n"
        for day in dailyForecast:
            condition = translator.translate(day['condition'], dest='sk').text

            if condition.endswith("ý"):
                condition = condition[:-1] + "é"

            answer += (
                f"{day['date']}: {condition}, "
                f"od {day['min_temp']}°C do {day['max_temp']}°C, "
                f"východ slnka o {day['sunrise']}, západ slnka o {day['sunset']}.\n"
            )

    return answer

def nowPlaying(song, lang):
    if lang == "en":
        answer = f"Now playing {song} on spotify"
    elif lang == "sk":
        answer = f"Púšťam {song} cez spotify"
    return answer