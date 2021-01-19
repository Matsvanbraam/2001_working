# Project by Mats van Braam and Laura Schep

import speech_recognition as sr
import pyaudio

class VoiceControls:
    def __init__(self):
        self.r = sr.Recognizer()

    #This function will start listening with your microphone when called
    def listening(self):
        with sr.Microphone() as source:
            #A denioser
            self.r.adjust_for_ambient_noise(source)
            print('Say a number between 0 and 6: ')
            audio = self.r.listen(source)
        try:
            text = self.r.recognize_google(audio, language='en-in')
            print('You said :  {}'.format(text))
            #If the words said are a valid input, convert it to an int and pass this input
            if text == "0" or text == "1" or text == "2" or text == "3" or text == "4" or text == "5" or text == "6":
                text = int(text)
                return text
            else:
                #If the input isn't valid, return the function so it starts to listen again
                print("What you said doesn't correspond to a column")
                return self.listening()
        #This happens when the input is not clear
        except Exception:
            print('Please raise your voice or speak more clearly')
            return self.listening()