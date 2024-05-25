import speech_recognition as sr

def transcribe_to_text(file_name):

    r = sr.Recognizer()
   
    with sr.AudioFile(file_name) as source:
        audio_text = r.listen(source)

        try:
            text = r.recognize_google(audio_text)
            return text
        except:
            return 1