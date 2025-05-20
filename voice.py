import azure.cognitiveservices.speech as speechsdk

def speak(text, lang):
    speechKey = "1kYtz6KJkc1hZeTSYVf2SgS1S7E6dH12EMu2AdcEJsxqAu1VscdvJQQJ99BEAC5RqLJXJ3w3AAAYACOG5KTU"
    serviceRegion = "westeurope"

    speechConfig = speechsdk.SpeechConfig(subscription = speechKey, region = serviceRegion)
    speechConfig.speech_synthesis_voice_name = "sk-SK-ViktoriaNeural" if lang == "sk" else "en-US-AvaNeural"

    audioConfig = speechsdk.audio.AudioOutputConfig(use_default_speaker = True)

    synthesizer = speechsdk.SpeechSynthesizer(speech_config = speechConfig, audio_config = audioConfig)
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Successfully synthesized")
    else:
        cancellation = result.cancellation_details
        print(f"Error: {result.reason}")
        print(f"Details: {cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation.error_details}")

