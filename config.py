
### CHOOSE YOUR ENGINES

WHISPER_VERSION = "OpenAI" # HF = Hugging Face, OpenAI
LLM = "OpenAI" # Azure, OpenAI, HF = Hugging Face


### API KEYS AND CREDENTIALS

# OpenAI
OPEN_AI_API_KEY = 'sk-your-key'

# OpenAI models
GPT3 = "gpt-3.5-turbo"
GPT3_16K = "gpt-3.5-turbo-16k"
GPT4 = "gpt-4"
GPT4_32K = "gpt-4-32k"

# Microsoft Azure
AZURE_OPENAI_KEY = 'your-azure-key'
AZURE_OPENAI_ENDPOINT='https://uk-south-openai-instance.openai.azure.com/'

# Eleven Labs
ELEVENLABS_API_KEY = 'your-elevenlabs-key'

# Hugging Face
WHISPER_API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"
LLAMA_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat-hf"
FALCON_API_URL = ""
headers = {"Authorization": "Bearer hf_your_key"}


### NOTES APP

NOTES_APP = 'obsidian'


### FILE PATHS

OBSIDIAN_FILE_PATH = '/Users/micke/Obsidian/Micke/Möten/'


### TEXT FORMATS - GPT AND DALL-E PROMPT PRIMERS

LEARNINGLAB_PROMPT_PRIMER = '''
Agera som expert inom livslångt lärande och lärande i organisationer. 
Sammanfatta och summera denna utmaning på svenska.
'''


DALL_E_PROMT_PRIMER = '''
Du är en framstående och världsledande artist som målar i olja. Skapa en 
prompt till ett motiv på en tavla utifrån nedanstående text genom 
att lyfta ut det viktigaste i texten. Prompten ska gå att använda 
i DALL-E.
'''


PROJECT_PROMPT_PRIMER = '''
Agera som projektledare och sammanfatta mötesanteckningarna enligt mallen nedan. 
Det ska formatteras som markdown för Obsidian. 
\nMALL----\n
# Projektnamn: {{projektnamn}} \n\nLänkar:: [[projektbeskrivning]]\nDatum:: 
{{date}}\nTid:: {{time}}\nStatus:: #status-ny #status-pågående 
#status-avslutad #status-reflektion\nMOC:: \nKontext::\n\n## Inledning\n{{hur sammanfattar du 
och förklarar projektet mycket kort?}}\n\n## Bakgrund\n{{Vad är projektets 
bakgrund och varför finns det? För vem och vilket behov?}}\n\n## Syfte och 
mål\n{{Vad är projektets syfte? Vilka (SMARTa) mål har projektet?}}\n\n## 
Genomförande\n{{Hur ska projektet genomföras? Finns det några faser eller 
steg i projektet som måste genomföras? Vilka metoder används i projektets 
genomförande?}}\n\n## Organisering\n{{Hur organiseras projektet? Hur ser 
projektets ledning och styrning ut? Hur går det till att fatta beslut i 
projektet? Vilka är projektets primära resurser och kompetenser?}}\n\n## 
Förväntade resultat\n{{När projektet har uppnått sina målsättningar, vilka 
är de förväntade resultaten som uppstår när målen uppfylls? Vilka långsiktiga 
effekter finns att vänta av att projektets mål och resultat uppstår?}}\n\n## 
Budget\n{{Vilka intäkter och kostnader har projektet? Hur säkrar projektet 
sin finansiering?}}\n\n## Samverkan\n{{Vilken samverkan behöver finnas på 
plats för att projektet ska uppnå sina resultat? Vilka andra intressenter 
finns? Hur förhåller sig projektet till sina intressenter?}}\n\n## 
Kontaktuppgifter\n{{Vem kontaktar man för att veta mer om projektet?}}\n\n## 
Källor\n{{Här skrivs vilka externa källor, om sådana finns, projektbeskrivningen syftar till}}
'''

