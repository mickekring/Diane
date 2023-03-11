
# version = 0.2

import tkinter as tk
from tkinter import ttk
import pyaudio
import wave
import threading
import os
import sys
import datetime
from tkinter import *
import openai
import config as c
import time

if sys.platform == "win32":
	import ctypes

# Variables

openai.api_key = c.OPEN_AI_API_KEY


# Initialize the recording state

recording = False
frames = None
wf = None
t = None
CHANNELS = None

recorded_audio_exists = False
ai_text_exists = False


# Create the function that will be called when the variable changes

def update_button1_state(*args):
	if recorded_audio_exists:
		button1.config(state="tk.NORMAL")
	else:
		button1.config(state="tk.DISABLED")

def update_button2_state(*args):
	if recorded_audio_exists:
		button2.config(state="tk.NORMAL")
	else:
		button2.config(state="tk.DISABLED")

def update_button3_state(*args):
	if recorded_audio_exists:
		button3.config(state="tk.NORMAL")
	else:
		button3.config(state="tk.DISABLED")

def update_button_save_state(*args):
	if ai_text_exists:
		button_save.config(state="tk.NORMAL")
	else:
		button_save.config(state="tk.DISABLED")


# Define the function to be called when the button is clicked

def record():
	global recording, frames, wf, t, p, RATE, FORMAT, CHANNELS, filename, now
	
	if not recording:
		
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 22050
		frames = []
		p = pyaudio.PyAudio()
		stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
		recording = True
		
		button_rec.config(text="Stoppa inspelning")

		text_widget.delete(1.0, tk.END)
		text_widget.insert(tk.END, "Spelar in... prata på...\n\nKlicka på stopp när du är klar.")
        
		print()
		print("--- --- ---\n")
		print("Recording...")
       
		t = threading.Thread(target=read_audio_frames, args=(stream, CHUNK, frames))
		t.start()

	else:

		recording = False
		t.join()
		now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
		filename = f"audio/anteckning_{now}.wav"
		wf = wave.open(filename, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
		button_rec.config(text="Spela in igen")

		print("Recording stopped.\nSending to Whisper.")

		print(filename)

		send_to_whisper(filename)


def read_audio_frames(stream, chunk, frames):
	global recording
	while recording:
		data = stream.read(chunk)
		frames.append(data)
	stream.stop_stream()
	stream.close()


# Sending audio to Whisper

def send_to_whisper(filename):

	text_widget.delete(1.0, tk.END)
	text_widget.insert(tk.END, "Din text transkriberas...")
	
	print("Sending to Whisper...")
	
	audio_file= open(filename, "rb")
	transcript = openai.Audio.transcribe("whisper-1", audio_file)

	global transcribed
	transcribed = transcript["text"]

	print()
	print(transcribed)

	update_button1_state(True)
	update_button2_state(True)
	update_button3_state(True)
	update_button_save_state(True)

	text_widget.delete(1.0, tk.END)
	text_widget.insert(tk.END, "Transkribering:\n\n" + transcribed)


# Sending transcription to GPT based on choice of template

def send_to_gpt(choice):
	print()
	print("Sending to GPT-3...")

	global chat_response

	messages = []
	#messages = c.LINKED_IN_SYSTEM

	if choice == "linkedin":
		
		prompt_primer = c.LINKED_IN_PROMPT_PRIMER
		messages.append({"role": "user", "content": prompt_primer + "\n" + transcribed})

	elif choice == "ideas":

		prompt_primer = c.IDEAS_PROMPT_PRIMER
		messages.append({"role": "user", "content": prompt_primer + "\n" + transcribed})

	elif choice == "project":

		prompt_primer = c.PROJECT_PROMPT_PRIMER
		messages.append({"role": "user", "content": prompt_primer + "\n" + transcribed})

	completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

	chat_response = completion.choices[0].message.content
	print(f'ChatGPT: {chat_response}')

	text_widget.delete(1.0, tk.END)
	text_widget.insert(tk.END, "GPT 3.5-turbo: \n" + chat_response)

	if choice == "linkedin":

		write_promtp_dall_e(chat_response)


# Writes prompt for DALL-E when LinkedIn choice is made

def write_promtp_dall_e(chat_response):

	global dall_e_response

	messages = []

	prompt_primer = c.DALL_E_PROMT_PRIMER

	messages.append({"role": "user", "content": prompt_primer + "\n" + chat_response})

	completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

	dall_e_response = completion.choices[0].message.content
	print(f'ChatGPT DALL-E: {dall_e_response}')

	send_to_dall_e(dall_e_response)


# Created markdown file for Obsidian

def write_to_file():
	print()
	print("Writing to file...")

	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

	f = open("docs/" + choice + " " + now + ".txt", "w")
	f.write(chat_response)
	f.close()

	if c.NOTES_APP == "obsidian":
		f = open(c.OBSIDIAN_FILE_PATH + choice.capitalize() + " " + now + ".md", "w")
		
		if choice == "linkedin":

			f.write('<img src="' + dall_e_img_url + '">\n' + chat_response)

		else:

			f.write(chat_response)

		f.close()


# Sending prompt to DALL-E

def send_to_dall_e(dall_e_response):
	
	global dall_e_img_url

	PROMPT = dall_e_response
	
	response = openai.Image.create(
    prompt=PROMPT,
    n=1,
    size="512x512",
	)
	
	print()
	dall_e_img_url = response["data"][0]["url"]
	print(response["data"][0]["url"])


def choice_linkedin():

	global choice

	choice = "linkedin"
	send_to_gpt(choice)


def choice_ideas():

	global choice

	choice = "ideas"
	send_to_gpt(choice)


def choice_project():

	global choice

	choice = "project"
	send_to_gpt(choice)


# Create a new window
root = tk.Tk()

# Set the window size and position
root.geometry("380x638+300+300")
root.configure(background='#000000')

# Set the window title
root.title("Diane")

# Set the theme to 'clam'
ttk.Style().theme_use('clam')

# Create a style object
style = ttk.Style()

# Set the background color, text color, and hover text color of the button using the style object
style.configure('Red.TButton', padding=20, width=34, background='#ec5545', foreground='white', font=('Arial', 16, 'bold'), bordercolor='black', borderwidth=0)
style.map('Red.TButton', foreground=[('active', '#ec5545'), ('disabled', 'grey')])

style.configure('Green.TButton', padding=20, width=34, background='#68cd67', foreground='white', font=('Arial', 16, 'bold'), bordercolor='black', borderwidth=0)
style.map('Green.TButton', foreground=[('active', '#68cd67'), ('disabled', '#8e8e93')])

style.configure('Third.TButton', padding=(2, 20), width=11, background='#68cd67', foreground='white', font=('Arial', 16, 'bold'), bordercolor='black', borderwidth=0)
style.map('Third.TButton', foreground=[('active', '#68cd67'), ('disabled', '#8e8e93')])

# Create a text widget
# Create a font object with the desired font and size
text_font = ("Arial", 18)
text_widget = tk.Text(root, width=30, height=18, bg='#222222', pady=10, padx=10, fg='white', font=text_font, wrap="word")
text_widget.configure(highlightbackground='#000000')

# Add the text widget to the window using the grid geometry manager
text_widget.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

# Insert some text into the widget
text_widget.insert(tk.END, "Välkommen!\n\nJag är Diane. Spela in när du är redo.\n\nNär du trycker på stopp skickas din\ninspelning för transkribering.\nDet kan ta upp till ett par minuter.")

# Create a button
button_rec = ttk.Button(root, text="Spela in", command=record, style='Red.TButton')

button1 = ttk.Button(root, text="Idéer", style='Third.TButton', state="disabled", command=choice_ideas)
button2 = ttk.Button(root, text="LinkedIn", style='Third.TButton', state="disabled", command=choice_linkedin)
button3 = ttk.Button(root, text="Projekt", style='Third.TButton', state="disabled", command=choice_project)

button_save = ttk.Button(root, state="disabled", text="Spara", style='Green.TButton', command=write_to_file)

# Add the buttons to the window using the grid geometry manager
button_rec.grid(row=1, column=0, padx=10, pady=0, columnspan=3)

button1.grid(row=2, column=0, padx=10, pady=10, columnspan=1)
button2.grid(row=2, column=1, padx=0, pady=10, columnspan=1)
button3.grid(row=2, column=2, padx=10, pady=10, columnspan=1)

button_save.grid(row=3, column=0, padx=10, pady=0, columnspan=3)


### MAIN ###

# Run the main event loop
root.mainloop()
