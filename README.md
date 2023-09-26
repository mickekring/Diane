# Diane
This is a basic, simple prototype of the app Diane, which is a voice recorder using Whisper to transcribe and GPT to process text based on a template. Finally it saves the result to your Obsidian directory.

<img width="752" alt="v08" src="https://github.com/mickekring/Diane/assets/10948066/e9350cbf-1ca1-462a-b4c9-810e8ca3fa94">

## Disclaimer
* Written in Python by a non-coder
* Only tested on MacOS

## Flow
* Press "Spela in" to start recording your voice
* Press "Stoppa inspelning" - stops recording and saves the audio file to the audio directory and converts the wav file to mp3
* Choose a template (or create one) from the dropdown menu which transcribes the audio file with Whisper and after that the transcribed text in sent to either GPT-3 or GPT-4 with a prompt from the config.py or templates.json file
* Press "Spara" (save) to save the result to your Obsidian https://obsidian.md/ directory or if you're not using Obsidian, a text file will be saved in the docs folder.

## How to?
* You need an API key from OpenAI https://openai.com/
* Download files and directories to your computer
* Install FFMPEG on your computer
* Install python modules using pip : __customtkinter__, __pyaudio__, __pydub__, __pillow__, __tiktoken__ __ and __openai__.
* Open __config.py__ and insert you OpenAI API key in __OPEN_AI_API_KEY = ''__ and change the file path to your Obsidian directory, where you want to store your notes in __OBSIDIAN_FILE_PATH = ''__. If you don't want to use Obsidian, change __NOTES_APP__ to 'none' and a text file will be saved in the docs folder. 
* Run __main.py__ and have fun
* Promtps for the default templates are stored in config.py as well

## Updates
* v 0.9 | 2023-09-26 | When using both OpenAI or Azure as LLM, it calculates the amount of tokens needed and chooses the "right" model for you. GPT-4 8K is standard, and when > 8K it sends OpenAI to GPT3.5-16K and Azure to GPT-4-32K. There's a requirements.txt file as well for easy install of modules.
* v 0.8 | 2023-09-24 | You can now create your own templates. You can also use Azure and Hugging Face for LLM and/or Whisper. You can also choose a pre-recorded audio file instead of only record.
* v 0.4 | 2023-09-09 | Now text is streamed from GPT instead of wating for the whole response to be generated.
* v 0.3 | 2023-09-08 | Added a delay when you press 'stop recording' so you don't accidentally double press it and start a new recording. I also changed the conversion to mp3, so that the audio file always should stay below 25 MB, since that it the max input when sending the file to Whisper.
* v 0.2 | Changed GUI fron tkinter to customtkinter. Audio file is converted to mp3 for file size which can be sent to Whisper (25 MB limit). Dropdown menu instead of buttons for templates.
* v 0.1 | Initial Upload

## Problems?
* If you run into empty recordings, you want to change the privacy settings of MacOS that prohibits the use the microphone via a python script that runs in IDLE. You'll also get a popup to grant microphone access for Terminal.

