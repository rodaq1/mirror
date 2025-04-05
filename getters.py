# tento subor bude mat v sebe gettery pre informacie ktore voice assistant nedokaze vykonat cez gemini - 
# cize real time veci a personal veci, 
# pravdepodobne to budeme spajat s google apis na vsekto mozne
import datetime
import requests
import json
import certifi
import urllib3

weatherApiKey = "0c828664a0284e0ab89190507250404"
googleMapsKey = "AIzaSyD3hH7ACLlPHHgbwk9d9ARjpbRDBAsKTYw"

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

def getLatLng(address):
    try:
        result = http.request('GET', f'https://maps.googleapis.com/maps/api/geocode/json?key={googleMapsKey}&address={address}')
    except requests.exceptions.RequestException as e: 
        print(f"Error fetching data: {e}")
        return None
    parsedResult = result.json()
    lat = parsedResult["results"][0]["geometry"]["location"]["lat"]
    lng = parsedResult["results"][0]["geometry"]["location"]["lng"]
    location = f"{lat},{lng}"

    return location

def getTimeZone(address):
    location = getLatLng(address)
    try:
        result = http.request('GET', f'https://maps.googleapis.com/maps/api/timezone/json?location={location}&timestamp=1733428634&key={googleMapsKey}')      
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    parsedResult = result.json()
    timeZone = parsedResult["timeZoneId"]

    return timeZone

def getTimeDate(address):
    timeZone = getTimeZone(address)
    try:
        result = http.request('GET', f'https://timeapi.io/api/time/current/zone?timeZone={timeZone}')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    parsedResult = result.json()
    datetimeInfo = {
        "year": parsedResult["year"],
        "month": parsedResult["month"],
        "day": parsedResult["day"],
        "hour": parsedResult["hour"],
        "minute": parsedResult["minute"],
        "seconds": parsedResult["seconds"],
        "dayOfWeek": parsedResult["dayOfWeek"]
    }

    return datetimeInfo

def getCurrentWeather(address):
    location = getLatLng(address)
    try:
        result = http.request('GET', f'http://api.weatherapi.com/v1/current.json?key={weatherApiKey}&q={location}')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    parsedResult = result.json()

    try:
        current = parsedResult["current"]
        weatherInfo = {
            "temp": current["temp_c"],
            "feelsliketemp": current["feelslike_c"],
            "condition": current["condition"]["text"],
            "wind": current["wind_kph"],
            "humidity": current["humidity"],
        }
        return weatherInfo
    except KeyError as e:
        print(f"Missing key in weather data: {e}")
        return None

def getForecast(address, days):
    location = getLatLng(address)
    try:
        result = http.request('GET', f'http://api.weatherapi.com/v1/forecast.json?key={weatherApiKey}&q={location}&days={days}')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    parsedResult = result.json()
    return parsedResult

def getHourlyForecast(forecast):
    hourlyForecast = []

    for day in forecast['forecast']['forecastday']:
        date = day['date']
        for hour in day['hour']:
            hourInfo = {
                'date': date,
                'time': hour['time'].split(' ')[1],
                'temp_c': hour['temp_c'],
                'feelslike_c': hour['feelslike_c'],
                'humidity': hour['humidity'],
                'condition': hour['condition']['text'],
                'chance_of_rain': hour.get('chance_of_rain', 0),
                'chance_of_snow': hour.get('chance_of_snow', 0),
            }
            hourlyForecast.append(hourInfo)

    return hourlyForecast

def getDailyForecast(forecast):
    dailyForecast = []

    for day in forecast['forecast']['forecastday']:
        dayInfo = {
            "date": day['date'], 
            "max_temp": day['day']['maxtemp_c'],
            "min_temp": day['day']['mintemp_c'],
            "condition": day['day']['condition']['text'],
            "sunrise": day['astro']['sunrise'],
            "sunset": day['astro']['sunset']
        }
        dailyForecast.append(dayInfo)
    
    return dailyForecast

    



