from openai import OpenAI
import requests #http request library to make api calls to the watson speech-to-text api

openai_client = OpenAI()


def speech_to_text(audio_binary):
    #set up watson speech-to-text http api url
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = 'https://sn-watson-stt.labs.skills.network/speech-to-text/api/v1/recognize'
    #parameters
    params = {
        'model': 'en-US_Multimedia', #telling watson want to use US english model for processing speech
    }
    #body of the http request
    body = audio_binary #parameter, sending audio data inside post request
    #http post request
    response = requests.post(api_url, params=params, data=audio_binary).json() #converted to json to make it easier for python to parse, pass url, params, and data (body)
    #parse the respnose for transcribed text
    text = 'null'
    while bool(response.get('results')):
        print('speech to text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)
        return text
    return None


def text_to_speech(text, voice=""):
    #set up watson text to speech http api url
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = 'https://sn-watson-tts.labs.skills.network/text-to-speech/api/v1/synthesize?output=output_text.wav'
# Adding voice parameter in api_url if the user has selected a preferred voice
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
    # Set the headers for our HTTP request
    headers = {
        'Accept': 'audio/wav', #we are sending audio wav
        'Content-Type': 'application/json', #format of body json
    }
    # Set the body of our HTTP request
    json_data = {
        'text': text,
    }
    # Send a HTTP Post request to Watson Text-to-Speech Service
    response = requests.post(api_url, headers=headers, json=json_data)
    print('text to speech response:', response)
    return response.content    


def openai_process_message(user_message):
    #will take a prompt and pass it to OpenAI's gpt-3 api to receive a response
    # Set the prompt for OpenAI Api
    prompt = "Act like a personal assistant. You can respond to questions, translate sentences, summarize news, and give recommendations."
    # Call the OpenAI Api to process our prompt
    openai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=4000 #max of response
    )
    print("openai response:", openai_response)
    # Parse the response to get the response message for our prompt
    response_text = openai_response.choices[0].message.content
    return response_text
