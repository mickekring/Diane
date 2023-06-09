### Diane
### Version: 0.2
### Author: Micke Kring
### Contact: jag@mickekring.se

import customtkinter as ctk
from PIL import Image
import pyaudio
import wave
import threading
import os
import sys
import datetime
import openai
import config as c
import time
from pydub import AudioSegment

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

global transcribed_audio_exists
transcribed_audio_exists = False


# Set Appearance

#customtkinter.set_appearance_mode("system")  # default value
ctk.set_appearance_mode("dark")
#customtkinter.set_appearance_mode("light")
ctk.set_default_color_theme("my-theme.json")



# Converting wave file to mp3

def convert_to_mp3(input_file, output_file):
	audio = AudioSegment.from_wav(input_file)
	audio.export(output_file, format="mp3")



# Define the function to be called when the button is clicked

def record(app_instance, icon_rec, icon_stop_rec):
	global recording, frames, wf, t, p, RATE, FORMAT, CHANNELS, filename, mp3_filename, now, transcribed_audio_exists
	
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
		
		app_instance.button_record.configure(text="Stoppa inspelning", image=icon_stop_rec)
		transcribed_audio_exists = False

		app_instance.textbox.delete(1.0, 'end')
		app_instance.textbox.insert('end', "1. Spelar in...\n")
        
		print()
		print("--- --- ---\n")
		print("Recording...")
       
		t = threading.Thread(target=read_audio_frames, args=(stream, CHUNK, frames))
		t.start()

	else:

		recording = False
		t.join()
		now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
		filename = f"audio/audio_{now}.wav"
		wf = wave.open(filename, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()

		# Convert WAV to MP3
		print("Converting to mp3")
		mp3_filename = f"audio/audio_{now}.mp3"
		convert_to_mp3(filename, mp3_filename)

		app_instance.button_record.configure(text="Spela in igen", image=icon_rec)

		#app_instance.textbox.delete(1.0, 'end')
		app_instance.textbox.insert('end', "\n2. Inspelning stoppad.\nLjudfilen " + str(now) 
			+ ".wav\när sparad.\n")

		recorded_audio_exists = True
		
		if recorded_audio_exists:
			app_instance.button_send.configure(state="normal")
			app_instance.button_save.configure(state="normal")

		print("Recording stopped.\n")

		print(filename + "\n")
		print(mp3_filename + "\n")



def read_audio_frames(stream, chunk, frames):
	global recording
	while recording:
		data = stream.read(chunk)
		frames.append(data)
	stream.stop_stream()
	stream.close()



# Sending audio to Whisper

def send_to_whisper(app_instance, user_choice):

	global transcribed_audio_exists
	global user_made_choice
	global chat_response

	user_made_choice = user_choice
	
	print("Sending to Whisper...")
	print(user_choice)

	app_instance.textbox.insert('end', "\n4. Skickar inspelning till transkribering...\n")
	
	audio_file= open(mp3_filename, "rb")
	transcript = openai.Audio.transcribe("whisper-1", audio_file)

	global transcribed
	transcribed = transcript["text"]

	print()
	print(transcribed)

	chat_response = transcribed

	app_instance.textbox.insert('end', "\n___ Transkribering ___ \n\n" + transcribed + "\n")

	transcribed_audio_exists = True



# Sending transcription to GPT based on choice of template

def send_to_gpt(prompt_primer, gpt_model, app_instance, choice):
	print()
	print("Sending to " + gpt_model + "...")

	global chat_response
	global user_made_choice

	user_made_choice = choice

	messages = []

	messages.append({"role": "user", "content": prompt_primer + "\n" + transcribed})

	completion = openai.ChatCompletion.create(model=gpt_model, messages=messages)

	chat_response = completion.choices[0].message.content
	print(f'ChatGPT: {chat_response}')

	app_instance.textbox.insert('end', "\n___ " + choice + ": " + gpt_model + " ___\n\n" + chat_response + "\n")



# Create markdown file for Obsidian

def write_to_file():
	print()
	print("Writing to file...")

	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

	f = open("docs/" + user_made_choice + now + ".txt", "w")
	f.write(chat_response)
	f.close()

	if c.NOTES_APP == "obsidian":
		f = open(c.OBSIDIAN_FILE_PATH + user_made_choice.capitalize() + " " + now + ".md", "w")
		
		if user_made_choice == "linkedin":

			f.write('<img src="' + dall_e_img_url + '">\n' + chat_response)

		else:

			f.write(chat_response)

		f.close()



class App(ctk.CTk):
	def __init__(self):
		super().__init__()

		self.geometry("400x660")
		self.title("Diane - version 0.2")
		self.minsize(400, 660)

		icon_rec = ctk.CTkImage(light_image=Image.open("images/rec.png"), 
			dark_image=Image.open("images/rec.png"), size=(46, 50))

		icon_stop_rec = ctk.CTkImage(light_image=Image.open("images/stop_rec.png"), 
			dark_image=Image.open("images/stop_rec.png"), size=(46, 50))

		image_logo = ctk.CTkImage(light_image=Image.open("images/logo.png"), 
			dark_image=Image.open("images/logo.png"), size=(135, 40))


		# create 2x2 grid system
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure((0, 1, 2), weight=1)


		# Create logo label
		self.logo_label = ctk.CTkLabel(master=self, image=image_logo, text="")
		self.logo_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 0), sticky="nw")

		self.textbox = ctk.CTkTextbox(master=self, wrap="word", height=340)
		self.textbox.grid(row=1, column=0, columnspan=3, padx=20, pady=(20, 0), sticky="nsew")

		self.button_record = ctk.CTkButton(master=self, image=icon_rec, height=70, 
			command=lambda: record(self, icon_rec, icon_stop_rec), text="Spela in")
		self.button_record.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
		self.button_record.configure(fg_color="#eb4e3d", hover_color="#a3392e")


		self.combobox = ctk.CTkComboBox(master=self, height=46, 
			values=["--- Välj mall ---", "Endast transkribering", "Generellt möte (GPT-3)", "Tankar och idéer (GPT-3)", 
			"Projektbeskrivning (GPT-4)", "LinkedIn (GPT-3)", "Twitter (GPT-3)", "Tala in din egna prompt (GPT-4)"])
		self.combobox.grid(row=3, column=0, columnspan=2, padx=(20, 10), pady=0, sticky="ew")

		self.button_send = ctk.CTkButton(master=self, height=46, command=self.button_callback, text="Bearbeta text")
		self.button_send.grid(row=3, column=2, columnspan=1, padx=(10, 20), pady=0, sticky="ew")
		self.button_send.configure(fg_color="gray20", hover_color="gray15", state="disabled")

		self.button_save = ctk.CTkButton(master=self, height=46, command=write_to_file, text="Spara")
		self.button_save.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky="ew")
		self.button_save.configure(fg_color="#65c366", hover_color="#478d48", state="disabled")


	def button_callback(self):
		self.textbox.insert("insert", "\n3. Val: " + self.combobox.get() + "\n")
		self.choice_made = self.combobox.get()
		print("\n3. " + self.choice_made)

		if self.choice_made == "--- Välj mall ---":
			self.textbox.insert("insert", "\nDu måste välja en mall i rullgardinsmenyn.")


		elif self.choice_made == "Endast transkribering":

			whisper_thread = threading.Thread(target=send_to_whisper, args=(self, self.choice_made,))
			whisper_thread.start()


		elif self.choice_made == "LinkedIn (GPT-3)":

			def process_choice(app_instance):
				global transcribed_audio_exists
				
				if transcribed_audio_exists == False:
					send_to_whisper(app_instance, self.choice_made)
				while not transcribed_audio_exists:
					time.sleep(0.1)

				send_to_gpt(c.LINKED_IN_PROMPT_PRIMER, c.GPT3, app_instance, self.choice_made)


			process_thread = threading.Thread(target=process_choice, args=(self,))
			process_thread.start()


		elif self.choice_made == "Twitter (GPT-3)":

			def process_choice(app_instance):
				global transcribed_audio_exists
				
				if transcribed_audio_exists == False:
					send_to_whisper(app_instance, self.choice_made)
				while not transcribed_audio_exists:
					time.sleep(0.1)

				send_to_gpt(c.TWITTER_PROMPT_PRIMER, c.GPT3, app_instance, self.choice_made)


			process_thread = threading.Thread(target=process_choice, args=(self,))
			process_thread.start()


		elif self.choice_made == "Generellt möte (GPT-3)":

			def process_choice(app_instance):
				global transcribed_audio_exists
				
				if transcribed_audio_exists == False:
					send_to_whisper(app_instance, self.choice_made)
				while not transcribed_audio_exists:
					time.sleep(0.1)

				send_to_gpt(c.GENERAL_MEET_PROMPT_PRIMER, c.GPT3, app_instance, self.choice_made)


			process_thread = threading.Thread(target=process_choice, args=(self,))
			process_thread.start()


		elif self.choice_made == "Tankar och idéer (GPT-3)":

			def process_choice(app_instance):
				global transcribed_audio_exists
				
				if transcribed_audio_exists == False:
					send_to_whisper(app_instance, self.choice_made)
				while not transcribed_audio_exists:
					time.sleep(0.1)

				send_to_gpt(c.IDEAS_PROMPT_PRIMER, c.GPT3, app_instance, self.choice_made)


			process_thread = threading.Thread(target=process_choice, args=(self,))
			process_thread.start()


		elif self.choice_made == "Projektbeskrivning (GPT-4)":

			def process_choice(app_instance):
				global transcribed_audio_exists
				
				if transcribed_audio_exists == False:
					send_to_whisper(app_instance, self.choice_made)
				while not transcribed_audio_exists:
					time.sleep(0.1)

				send_to_gpt(c.PROJECT_PROMPT_PRIMER, c.GPT4, app_instance, self.choice_made)


			process_thread = threading.Thread(target=process_choice, args=(self,))
			process_thread.start()


		elif self.choice_made == "Tala in din egna prompt (GPT-4)":

			def process_choice(app_instance):
				global transcribed_audio_exists
				
				if transcribed_audio_exists == False:
					send_to_whisper(app_instance, self.choice_made)
				while not transcribed_audio_exists:
					time.sleep(0.1)

				send_to_gpt(c.YOUR_OWN_PROMTP_PRIMER, c.GPT4, app_instance, self.choice_made)


			process_thread = threading.Thread(target=process_choice, args=(self,))
			process_thread.start()

			
		else:
			self.textbox.insert("insert", "\nDin text transkriberas nu och skickas\ndärefter till GPT.")



if __name__ == "__main__":
	app = App()
	app.mainloop()


