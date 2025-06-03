#!/bin/bash
cd "$(dirname "$0")"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install SpeechRecognition
pip install googletrans
pip install google-generativeai
pip install azure-cognitiveservices-speech
pip install certifi
pip install sentence-transformers
pip install spotipy
pip install urllib3
pip install requests
pip install protobuf
python3 main.py
192.168.0.201
