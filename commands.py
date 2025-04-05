# tento subor bude mat v sebe commandy ktore voice assistant nedokaze vykonat cez gemini - 
# cize real time veci a personal veci, 
# pravdepodobne to budeme spajat s google apis na vsekto mozne
import datetime
import requests
import json

weatherApiKey = "0c828664a0284e0ab89190507250404"
googleMapsKey = "AIzaSyD3hH7ACLlPHHgbwk9d9ARjpbRDBAsKTYw"

def getLatLng(address):
    result = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?key={googleMapsKey}&address={address}')
    parsedResult = json.loads(result)
    lat = parsedResult["results"][0]["geometry"]["location"]["lat"]
    lng = parsedResult["results"][0]["geometry"]["location"]["lng"]
    location = f"{lat},{lng}"
    return location

def getTimeZone(address):
    location = getLatLng(address)
    result = requests.get(f'https://maps.googleapis.com/maps/api/timezone/json?location={location}&timestamp=1733428634&key={googleMapsKey}')       
    parsedResult = json.loads(result)
    timeZone = parsedResult["timeZoneId"]
    return timeZone

def getTimeDate(address):
    timeZone = getTimeZone(address)
    result = requests.get(f'https://timeapi.io/api/time/current/zone?timeZone={timeZone}')

    parsedResult = json.loads(result)
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
    result = requests.get(f'http://api.weatherapi.com/v1/current.json?key={weatherApiKey}&q={location}')
    parsedResult = json.loads(result)

    



