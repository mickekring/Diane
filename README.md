# Diane
This is a basic, simple prototype of the app Diane, which is a voice recorder using Whisper to transcribe and GPT to process text based on a template. Finally it saves the result to your Obsidian directory.

![diane](https://user-images.githubusercontent.com/10948066/224471311-6a09757d-34fa-4bc0-8cd5-c6eb770dd243.jpg)

## Disclaimer
* Written in Python by a non-coder
* Only tested on MacOS

## Flow
* Press "Spela in" to start recording your voice
* Press "Stoppa inspelning" - stops recording and saves the audio file to the audio directory, then sends the audio file to Whisper for transcription
* Choose a template; Idéer (ideas), LinkedIn or Projekt - sends the transcribed text to GPT3.5-turbo with a promt from the config.py file
* Press "Spara" (save) to save the result from GPT3.5-turbo to your Obsidian https://obsidian.md/ directory

## How to?
* You need an API key from OpenAI https://openai.com/
* Download files and directories to your computer
* Install python modules using pip : __Tkinter__, __pyaudio__ and __openai__
* Open __config.py__ and insert you OpenAI API key in __OPEN_AI_API_KEY = ''__ and change the file path to your Obsidian directory, where you want to store your notes in __OBSIDIAN_FILE_PATH = ''__ 
* Run __main.py__ and have fun
* Promtps for the templates are stored in config.py as well

## Problems?
* If you run into empty recordings, you want to change the privacy settings of macOS that prohibits the use the microton via a python script that runs in IDLE. You'll also get a popup to grant microton access for Terminal.
