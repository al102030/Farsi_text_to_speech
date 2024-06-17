from pathlib import Path
# OpenAI Library. install it using your virtual environment system (pipenv or venv) before running the code
from openai import OpenAI
import os
import warnings

# this is the definition of OpneAI client using OPENAI_API_KEY
# you can put your Key in Bashrc file in linux (check it in terminal using "echo $OPENAI_API_KEY ")
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"))

# You can put your Farsi text in this file
with open("text.txt", "r", encoding="utf-8") as my_file:
    txt = my_file.read()

if txt:
    completion = client.chat.completions.create(
        # Here you can choose your desire model
        model="gpt-3.5-turbo-0125",
        messages=[
            # This is the message that define the kind of abstraction
            {"role": "system", "content": """It is a long Farsi text, and I want you to give me
            a meaningful abstract(gist) paragraph () about the whole context (Don't add anything).
            I would appreciate it if you could answer it in Farsi"""},
            {"role": "user", "content": txt}
        ]
    )
    # this is the abstracted text which ChatGPT returned
    abstracted_txt = completion.choices[0].message.content

    # Ignore Deprecation Warning *
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # here you can define a path to save your Audio file
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        # This is the Text-to-speech API model
        model="tts-1",
        # this is the kind of Artificial voice
        voice="shimmer",
        input=abstracted_txt
    )

    # * Despite the deprecation of this method, it remains the only one suggested by OpenAI.
    response.stream_to_file(speech_file_path)
    print("Done!")
else:
    print("Text file is empty!")
