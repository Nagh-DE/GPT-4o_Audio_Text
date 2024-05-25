from record_voice import record_voice
from audio_to_text import transcribe_to_text
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import openai
import os
from dotenv import load_dotenv
load_dotenv()

audio_file = record_voice() #record user voice and save in a file
# audio_file = "audio.wav" #TO TEST
text = transcribe_to_text(file_name=audio_file) # convert audio to text
if text != 1:
    
    print(text)

    openai.api_key = os.getenv("AZURE_OPENAI_KEY")
    token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

    chatgpt_model = os.getenv("AZURE_GPT_DEPLOYMENT")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version="2024-02-01",
    )

    completion = client.chat.completions.create(
        model=chatgpt_model,
        messages=[
            {
                "role": "system", 
                "content": "You are an expert in converting text to SQL queries, this text is converted from audio so try to identify\
                    if there are any spelling mistakes in it. don't try to add explanation to it, just return the sql query.\
                        do not include ``` at the start and end of query"},
            {
                "role": "user",
                "content": text
            }
        ]
    )
    print(completion.choices[0].message.content)
