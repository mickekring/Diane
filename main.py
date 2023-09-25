### Diane
app_version = "0.8.3"
### Author: Micke Kring
### Contact: jag@mickekring.se

import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from PIL import Image
import pyaudio
import wave
import threading
import shutil
import os
import sys
import json
import requests
import datetime
import openai
import config as c
import time
from pydub import AudioSegment
#from elevenlabs import set_api_key

if sys.platform == "win32":
	import ctypes
	ctypes.windll.shcore.SetProcessDpiAwareness(1)

### VARIABLES

# Open AI
openai.api_key = c.OPEN_AI_API_KEY

# Eleven Labs
#set_api_key(c.ELEVENLABS_API_KEY)

# Misc

number = 1

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


default_templates = ["--- Välj mall ---", "Endast transkribering", "--- --- --- ---", "Översätt till engelska", 
		     "--- --- --- ---", "Learning Lab", "Projektbeskrivning",]


# Loading templates from json
# Load the templates

try:
	global templates

	with open('templates.json', 'r') as f:
		templates = json.load(f)
except FileNotFoundError:
	print("Heepåre")
	templates = {
		default_templates
	}

original_template_name = None


# Compressing the audio / video file

def convert_to_mono_and_compress_to_mp3(input_file, output_file, target_size_MB=8):

	# Load the audio file
	audio = AudioSegment.from_file(input_file)

	# Convert to mono
	audio = audio.set_channels(1)

	# Calculate target bitrate to achieve the desired file size (in bits per second)
	duration_seconds = len(audio) / 1000.0  # pydub works in milliseconds
	target_bitrate = int((target_size_MB * 1024 * 1024 * 8) / duration_seconds)

	print(f"Audio Path: {input_file}")
	print(f"Output Path: {output_file}")
	print(f"Target Bitrate: {target_bitrate}")

	# Compress the audio file
	try:
		audio.export(output_file, format="mp3", bitrate=f"{target_bitrate}")
	except Exception as e:
		print(f"Error during audio export: {e}")
		return None



# Define the function to be called when the button is clicked

def record(app_instance, icon_rec, icon_stop_rec):
	global recording, frames, wf, t, p, RATE, FORMAT, CHANNELS, filename, mp3_filename, now, transcribed_audio_exists

	if not recording:
		
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 11025
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
		app_instance.textbox.see('end')
        
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
		convert_to_mono_and_compress_to_mp3(filename, mp3_filename)

		app_instance.button_record.configure(text="Spela in igen", image=icon_rec)
		
		# Disable the record button for 2 seconds to prevent accidental double-click
		app_instance.button_record.configure(state="disabled")
		app_instance.after(3000, lambda: app_instance.button_record.configure(state="normal"))

		app_instance.textbox.insert('end', "\n2. Inspelning stoppad.\nLjudfilen " + str(now) 
			+ ".wav\när sparad.\n")
		app_instance.textbox.see('end')

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



# Choose audio file, instead of recordning

def choose_file(app_instance):

	global mp3_filename
	global transcribed_audio_exists

	app_instance.textbox.insert('end', "\n1. Välj fil.")
	app_instance.textbox.see('end')

	# Open the file dialog and get the path of the selected file
	file_path = filedialog.askopenfilename()

	# Define the destination path
	dest_path = os.path.join(os.getcwd(), "audio", os.path.basename(file_path))

	# Copy the file to the destination
	shutil.copy(file_path, dest_path)

	print(f"File copied to {dest_path}")

	# Generate a new filename for the converted file
	now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	mp3_filename = f"audio/audio_{now}.mp3"

	# Convert WAV to MP3
	print("Converting to mp3")
	mp3_filename = f"audio/audio_{now}.mp3"
	convert_to_mono_and_compress_to_mp3(dest_path, mp3_filename)

	app_instance.textbox.insert('end', "\n2. Din fil är klar.")
	app_instance.textbox.see('end')

	recorded_audio_exists = True
	transcribed_audio_exists = False
		
	if recorded_audio_exists:
		app_instance.button_send.configure(state="normal")
		app_instance.button_save.configure(state="normal")

	print(dest_path + "\n")
	print(mp3_filename + "\n")



# Sending audio to Whisper

def send_to_whisper(app_instance, user_choice):

	global transcribed_audio_exists
	global user_made_choice
	global gpt_response
	global transcribed

	user_made_choice = user_choice
	
	print("\nSKICKAR TILL WHISPER FÖR TRANSKRIBERING")
	print(user_choice)

	app_instance.textbox.insert('end', "\n4. Skickar inspelning till transkribering...\n")
	app_instance.textbox.see('end')
	
	if c.WHISPER_VERSION == "OpenAI":
	
		audio_file= open(mp3_filename, "rb")
		transcript = openai.Audio.transcribe("whisper-1", audio_file)		
		transcribed = transcript["text"]

	elif c.WHISPER_VERSION == "HF":
		def query(filename):
			with open(filename, "rb") as f:
				data = f.read()
			response = requests.post(c.WHISPER_API_URL, headers=c.headers, data=data)
			print()
			print(response.status_code)
			print(response.text)
			print()
			return response.json()

		output = query(mp3_filename)
		transcribed = output["text"]

	print()
	print(transcribed)
	print("\n--- --- --- ---")

	gpt_response = transcribed

	app_instance.textbox.insert('end', "\n___ Transkribering ___ \n\n" + transcribed + "\n")
	app_instance.textbox.see('end')

	transcribed_audio_exists = True

	#write_to_file()



# Translate with Whisper

def translate_with_whisper(app_instance, user_choice):

	#global user_made_choice
	global gpt_response
	#global transcribed

	user_made_choice = user_choice
    
	print("\nSKICKAR TILL WHISPER FÖR ÖVERSÄTTNING")
	print(user_choice)

	# Read the audio file
	audio_file= open(mp3_filename, "rb")

	print("Opened audio file")

	#openai.api_key = api_key
	translate = openai.Audio.translate("whisper-1", audio_file)

	print("Sent the text to Whisper")

	# Extract transcribed text from the response
	transcribed = translate["text"]

	print(transcribed)

	#return translated_text

	gpt_response = transcribed

	app_instance.textbox.insert('end', "\n___ Översättning ___ \n\n" + transcribed + "\n")
	app_instance.textbox.see('end')



# Sending transcription to GPT based on choice of template

def send_to_gpt(prompt_primer, gpt_model, app_instance, choice):
	
	print("\nSKICKAR TEXT TILL " + gpt_model + "")

	app_instance.textbox.insert('end', "\n5. Skickar transkribering till GPT...\n")
	app_instance.textbox.see('end')

	global chat_response
	global gpt_response
	global user_made_choice

	user_made_choice = choice

	messages = []
	gpt_response = []

	messages.append({"role": "user", "content": prompt_primer + "\n" + transcribed})
	message_llama = prompt_primer + "\n" + transcribed

	app_instance.textbox.insert('end', "\n___ Bearbetad text ___ \n\n")
	app_instance.textbox.see('end')

	if c.LLM == "Azure":
	
		for chunk in openai.ChatCompletion.create(
			api_key = c.AZURE_OPENAI_KEY,
			api_base = c.AZURE_OPENAI_ENDPOINT,
			api_type = 'azure',
			api_version = '2023-05-15',
			engine = 'gpt-4-uk-south',

			messages=messages, 
			stream=True,):
			chat_response = chunk["choices"][0].get("delta", {}).get("content")
			
			if chat_response is not None:
				print(chat_response, end='')
				app_instance.textbox.insert('end', chat_response)
				app_instance.textbox.see('end')
				gpt_response.append(chat_response)
		
		# Join the list of strings into a single string
		gpt_response = ''.join(gpt_response)

	elif c.LLM == "OpenAI":

		for chunk in openai.ChatCompletion.create(model=gpt_model, messages=messages, temperature=0.7, stream=True,):
			chat_response = chunk["choices"][0].get("delta", {}).get("content")
			if chat_response is not None:
				print(chat_response, end='')
				app_instance.textbox.insert('end', chat_response)
				app_instance.textbox.see('end')
				gpt_response.append(chat_response)
		
		# Join the list of strings into a single string
		gpt_response = ''.join(gpt_response)
	
	elif c.LLM == "HF":
		
		print(message_llama)
		print()
		print()
		print("From LLAMA")
		
		def query(payload):
			response = requests.post(c.LLAMA_API_URL, headers=c.headers, json=payload)
			json_response = response.json()
			dict_response = json_response[0]
			split_text = dict_response['generated_text'].split('\n\n')  # split on '\n\n'
			if len(split_text) > 1:
				desired_text = split_text[1]
			else:
				desired_text = split_text[0]
			return desired_text
	
		output = query({
			"inputs": message_llama,
			})

		print(output)

		app_instance.textbox.insert('end', output)
		app_instance.textbox.see('end')
	
	print("\n\nFinnished processing text with LLM\n")
	print("--- --- --- ---")



# Create markdown file for Obsidian

def write_to_file():

	global number

	print()
	print("\nSPARAT I OBSIDIAN")

	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

	f = open("docs/" + user_made_choice + now + str(number) + ".txt", "w")
	f.write(str(gpt_response))
	f.close()

	if c.NOTES_APP == "obsidian":
		f = open(c.OBSIDIAN_FILE_PATH + user_made_choice.capitalize() + " " + now + str(number) + ".md", "w")
		
		if user_made_choice == "Learning Lab":

			f.write('<img src="' + dall_e_img_url + '">\n\n' + str(gpt_response))

		else:

			f.write(str(gpt_response))

		f.close()

	number += 1



def write_promtp_dall_e(chat_response):

	print("\nSKRIVER EN PROMPT TILL DALL-E FÖR ATT SKAPA EN BILD")

	global dall_e_response

	messages = []

	prompt_primer = c.DALL_E_PROMT_PRIMER

	messages.append({"role": "user", "content": prompt_primer + "\n" + str(chat_response)})

	completion = openai.ChatCompletion.create(model=c.GPT4, messages=messages)

	dall_e_response = completion.choices[0].message.content
	
	print()
	print(f'ChatGPT DALL-E: {dall_e_response}')
	print("--- --- --- ---")

	send_to_dall_e(dall_e_response)



# Sending prompt to DALL-E

def send_to_dall_e(dall_e_response):

	print("\nSKAPAR EN BILD MED DALL-E")
	
	global dall_e_img_url

	PROMPT = dall_e_response
	
	response = openai.Image.create(
    prompt=PROMPT,
    n=1,
    size="1024x1024",
	)
	
	print()
	dall_e_img_url = response["data"][0]["url"]
	print(response["data"][0]["url"])
	print("--- --- --- ---")



class App(ctk.CTk):
	def __init__(self):
		super().__init__()

		self.geometry("640x660")
		self.title("Diane - version " + app_version)
		self.minsize(640, 660)

		icon_rec = ctk.CTkImage(light_image=Image.open("images/rec.png"), 
			dark_image=Image.open("images/rec.png"), size=(46, 50))

		icon_stop_rec = ctk.CTkImage(light_image=Image.open("images/stop_rec.png"), 
			dark_image=Image.open("images/stop_rec.png"), size=(46, 50))
		
		icon_upload = ctk.CTkImage(light_image=Image.open("images/upload.png"), 
			dark_image=Image.open("images/upload.png"), size=(46, 50))

		image_logo = ctk.CTkImage(light_image=Image.open("images/logo.png"), 
			dark_image=Image.open("images/logo.png"), size=(135, 40))
		
		icon_plus = ctk.CTkImage(light_image=Image.open("images/plus.png"), 
			dark_image=Image.open("images/plus.png"), size=(23, 25))


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
		self.button_record.grid(row=2, column=0, columnspan=2, padx=(20, 10), pady=20, sticky="ew")
		self.button_record.configure(fg_color="#eb4e3d", hover_color="#a3392e")

		self.button_upload = ctk.CTkButton(master=self, image=icon_upload, height=70, command=lambda: choose_file(self), text="Välj fil")
		self.button_upload.grid(row=2, column=2, columnspan=1, padx=(10, 20), pady=20, sticky="ew")
		self.button_upload.configure(fg_color="#2b6494", hover_color="#1e476a")

		self.combobox = ctk.CTkComboBox(master=self, height=46, 
			values= default_templates + list(templates.keys()))
		self.combobox.grid(row=3, column=0, columnspan=1, padx=(20, 10), pady=0, sticky="ew")

		self.button_new_template = ctk.CTkButton(master=self, image=icon_plus, height=46, command=lambda: self.create_new_template(self), text="Skapa mall")
		self.button_new_template.grid(row=3, column=1, columnspan=1, padx=(10, 10), pady=0, sticky="ew")
		self.button_new_template.configure(fg_color="gray20", hover_color="gray15")

		self.button_send = ctk.CTkButton(master=self, height=46, command=self.button_callback, text="Bearbeta text")
		self.button_send.grid(row=3, column=2, columnspan=1, padx=(10, 20), pady=0, sticky="ew")
		self.button_send.configure(fg_color="gray20", hover_color="gray15", state="disabled")

		self.button_save = ctk.CTkButton(master=self, height=46, command=write_to_file, text="Obsidian")
		self.button_save.grid(row=4, column=0, columnspan=1, padx=(20, 10), pady=20, sticky="ew")
		self.button_save.configure(fg_color="#65c366", hover_color="#478d48", state="disabled")

		self.button_docx = ctk.CTkButton(master=self, height=46, command=write_to_file, text="Word")
		self.button_docx.grid(row=4, column=1, columnspan=1, padx=(10, 10), pady=20, sticky="ew")
		self.button_docx.configure(fg_color="#65c366", hover_color="#478d48", state="disabled")

		self.button_text = ctk.CTkButton(master=self, height=46, command=write_to_file, text="Text")
		self.button_text.grid(row=4, column=2, columnspan=1, padx=(10, 20), pady=20, sticky="ew")
		self.button_text.configure(fg_color="#65c366", hover_color="#478d48", state="disabled")

	
	def update_combobox(self):

		global templates

		# Load the templates from the JSON file
		with open('templates.json', 'r') as f:
			templates = json.load(f)

		# Update the values of the combobox
		self.combobox.configure(values = default_templates + list(templates.keys()))

		# Force an update of the combobox
		self.combobox.update_idletasks()


	# Experimental function to allow users to create their own templates

	def create_new_template(self, app_instance):

		global templates

		# Load the templates from the JSON file
		with open('templates.json', 'r') as f:
			templates = json.load(f)

		# This function will be called when the user selects "Create new template"
		window = tk.Toplevel()
		
		if sys.platform == "win32":
			default_font = ('Arial', 10)
			window.geometry('800x900')  # Set the size of the window
		else:
			default_font = ('Arial', 16)
			window.geometry('640x660')  # Set the size of the window
		window.title('Skapa ny mall')  # Set the title of the window
		window.configure(bg="#333333")

		label = tk.Label(window, text="Välj en mall att redigera", bg="#333333", fg="#ffffff", font=default_font)
		label.pack(pady=(30, 10))

		# Create a custom style for the combobox
		style = ttk.Style()
		style.configure('Custom.TCombobox', font=default_font)
		style.configure('Custom.TCombobox.Listbox', font=default_font)

		# Dropdown menu for selecting a template
		template_combobox = ttk.Combobox(master=window, values=list(templates.keys()), style='Custom.TCombobox')
		template_combobox.pack(pady=(0, 20))

		tk.Label(window, text='Namn på mallen', bg="#333333", fg="#ffffff", font=default_font).pack(pady=(0, 10))  # Add a label for the name entry
		name_entry = tk.Entry(window, bg="#666666", fg="#ffffff", highlightthickness=0, relief="flat", font=default_font)
		name_entry.pack(pady=(0, 20))

		tk.Label(window, text='Prompt', bg="#333333", fg="#ffffff", font=default_font).pack(pady=(0, 10))  # Add a label for the primer entry
		primer_entry = tk.Text(window, height=10, bg="#666666", fg="#ffffff", highlightthickness=0, relief="flat", font=default_font)
		primer_entry.pack(pady=(0, 20), padx=(20, 20), ipadx=20, ipady=20)

		def load_template(event):
			global original_template_name

			print("Combobox option selected!")  # Debugging print statement
			# Load the selected template into the name and primer fields
			selected_template = template_combobox.get()
			if selected_template in templates:
				name_entry.delete(0, 'end')
				name_entry.insert(0, selected_template)
				primer_entry.delete('1.0', 'end')
				primer_entry.insert('1.0', templates[selected_template])
			
			original_template_name = template_combobox.get()

		template_combobox.bind('<<ComboboxSelected>>', load_template)

		def save_template():
			
			global templates, original_template_name
			new_name = name_entry.get()
			prompt = primer_entry.get("1.0", "end-1c")

			# Check if editing an existing template
			if original_template_name:
				# Delete the original template if the name has been changed
				if original_template_name != new_name:
					del templates[original_template_name]
			# Save (or overwrite) the template with the new name and prompt
			templates[new_name] = prompt

			with open('templates.json', 'w') as f:
				json.dump(templates, f)

			# Reload the templates from the JSON file
			with open('templates.json', 'r') as f:
				templates = json.load(f)
			
			# Update the values of the dropdown menus
			template_combobox['values'] = list(templates.keys())

			# Reset the original_template_name
			original_template_name = None
			# Update the combobox in the main app
			app_instance.update_combobox()

		save_button = tk.Button(window, text="Spara", command=save_template, font=default_font)
		save_button.pack(pady=10)

		def delete_template():
			global templates
			# Delete the template
			del templates[name_entry.get()]
			with open('templates.json', 'w') as f:
				json.dump(templates, f)

			# Reload the templates from the JSON file
			with open('templates.json', 'r') as f:
				templates = json.load(f)

			# Update the values of the dropdown menus
			template_combobox['values'] = list(templates.keys())

			# Clear the name and primer fields
			name_entry.delete(0, 'end')
			primer_entry.delete('1.0', 'end')

			# Update the combobox in the main app
			app_instance.update_combobox()

		delete_button = tk.Button(window, text="Radera", command=delete_template, font=default_font)
		delete_button.pack()
	


	def button_callback(self):
		self.textbox.insert("insert", "\n3. Val: " + self.combobox.get() + "\n")
		self.choice_made = self.combobox.get()
		print("\n3. " + self.choice_made)

		if self.choice_made == "--- Välj mall ---":
			self.textbox.insert("insert", "\nDu måste välja en mall i rullgardinsmenyn.")
		
		elif self.choice_made == "Endast transkribering":

			whisper_thread = threading.Thread(target=send_to_whisper, args=(self, self.choice_made,))
			whisper_thread.start()

		elif self.choice_made == "Översätt till engelska":

			whisper_thread = threading.Thread(target=translate_with_whisper, args=(self, self.choice_made,))
			whisper_thread.start()

		elif self.choice_made == "Learning Lab":

			def process_choice(app_instance):
				global transcribed_audio_exists
				
				if transcribed_audio_exists == False:
					send_to_whisper(app_instance, self.choice_made)
				while not transcribed_audio_exists:
					time.sleep(0.1)

				send_to_gpt(c.LEARNINGLAB_PROMPT_PRIMER, c.GPT4, app_instance, self.choice_made)
				
				write_promtp_dall_e(chat_response)
				
				write_to_file()

			process_thread = threading.Thread(target=process_choice, args=(self,))
			process_thread.start()


		elif self.choice_made == "Projektbeskrivning":

			def process_choice(app_instance):
				global transcribed_audio_exists
				
				if transcribed_audio_exists == False:
					send_to_whisper(app_instance, self.choice_made)
				while not transcribed_audio_exists:
					time.sleep(0.1)

				send_to_gpt(c.PROJECT_PROMPT_PRIMER, c.GPT4, app_instance, self.choice_made)

			process_thread = threading.Thread(target=process_choice, args=(self,))
			process_thread.start()
	
		else:
			#self.textbox.insert("insert", "\nDin text transkriberas nu och skickas\ndärefter till GPT.")
			# Get the primer for the selected template
			primer = templates[self.choice_made]

			def process_choice(app_instance):
				global transcribed_audio_exists

				if transcribed_audio_exists == False:
					send_to_whisper(app_instance, self.choice_made)
				while not transcribed_audio_exists:
					time.sleep(0.1)

				# Send the primer to GPT
				send_to_gpt(primer, c.GPT4, app_instance, self.choice_made)

			process_thread = threading.Thread(target=process_choice, args=(self,))
			process_thread.start()


if __name__ == "__main__":
	app = App()
	app.mainloop()


