# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

# <code>
import azure.cognitiveservices.speech as speechsdk
import time

import text_to_cmd
import text_to_speech
import SQLTest

def process_cmds():
    
    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    
    player = text_to_speech.TextToSpeech()
    player.get_token()
    
    speech_key, service_region = "ae06249641924ee8bfebd863b121f33c", "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    
    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    
    flag = 1
    
    auth = False
    invalidUID = True
    invalidPW = True
    counter = 0
    while (auth):
        while (invalidUID):
            # ask UID
            player.save_audio("Hello. Please state your member number.")

            result = speech_recognizer.recognize_once()
            
            # Checks result.
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print("Recognized: {}".format(result.text))
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(result.no_match_details))
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
            time.sleep(10)
            userID = result.text.replace(".", "").replace(",", "")
            print(userID)
            if (len(userID) > 0):
                invalidUID = False
        while (invalidPW):
            # ask password
            player.save_audio("Hello. Please state your password.")

            result = speech_recognizer.recognize_once()
            
            # Checks result.
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print("Recognized: {}".format(result.text))
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(result.no_match_details))
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
            time.sleep(10)
            password = result.text.lower().replace(" ", "").replace(".", "")
            print(password)
            if (len(password) > 0):
                invalidPW = False
                
        try:
            val = SQLTest.get_auth(userID, password)
            if (val is not None):
                auth = False
        except:
            player.save_audio("Invalid login")
            
        invalidUID = True
        invalidPW = True
        counter += 1
        if (counter > 5):
            break  


    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed.  The task returns the recognition text as result. 
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query. 
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    while flag:
        player.save_audio('What would you like to do')
    
        result = speech_recognizer.recognize_once()
        
        # Checks result.
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                
        if 'quit' in result.text.lower():
          flag = 0
          player.save_audio('Thank you for your business') 
          break
        player.save_audio(result.text)
        
        c = text_to_cmd.return_command_type(result.text)
        player.save_audio(c)
        
        cmd_type = 'not a command'
        
        if (c=="cmd_type"):
        #if result.text
            break
        else:
            #SQLTest.deal_with_switch('balance', result.text)
            SQLTest.deal_with_switch(c,result.text)
            player.save_audio("Action completed! Say quit to end.")
                
            # TODO Add quit to commands        
       
# </code>