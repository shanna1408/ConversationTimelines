import os
import time
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(subscription="", region="westus")
speech_config.speech_recognition_language="en-US"
audio_config = ""
speech_recognizer = ""
done = False

def stop_cb(evt):
    print('CLOSING on {}'.format(evt))
    speech_recognizer.stop_continuous_recognition()
    global done 
    done = True

def recognize_from_file(input, output):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    # print(os.environ.get('SPEECH_KEY'), os.environ.get('SPEECH_REGION'))
    global audio_config, speech_recognizer
    audio_config = speechsdk.AudioConfig(filename=input)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt.result.text)))
    speech_recognizer.recognized.connect(lambda evt: output.write('{}\n'.format(evt.result.text)))
    # speech_recognizer.recognized.connect(lambda evt: print('{}\n'.format(evt.result.text)))
    
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)
    
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    
    return

def m4a_wav(m4a_file):
    wav_filename = 'SV_Transcript.wav'
    sound = AudioSegment.from_file(m4a_file, format='m4a')
    file_handle = sound.export(wav_filename, format='wav')

def main():
    # m4a_wav("Transcript 2.m4a")
    filename = "SV_Transcript.wav"
    transcript = open("SV_Transcript.txt", "w")
    recognize_from_file(filename, transcript)
    
if __name__ == "__main__":
    main()
    
