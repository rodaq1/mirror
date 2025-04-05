import getters as g
def whatsTheTime(lang, timeZone ="Europe/Bratislava"):
    dateTime = g.getTimeDate(timeZone)
    if lang == "en":
        answer = f"It's {dateTime['hour']}:{dateTime['minute']}"
        return answer
    elif lang == "sk":
        answer = f"Je {dateTime['hour']}:{dateTime['minute']}"
        return answer
