import speech_recognition as sr

recognizer = sr.Recognizer()

def speechRecognition():
    with sr.Microphone() as source:
        print(" ovor...")
        recognizer.energy_threshold=1500
        recognizer.adjust_for_ambient_noise(source)  
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="sk-SK")
        return text
    except Exception as e:
        print(f"chybicka {e}")