

### API KEYS AND CREDENTIALS

OPEN_AI_API_KEY = 'sk-youropenaikey'

GPT3 = "gpt-3.5-turbo"
GPT3_16K = "gpt-3.5-turbo-16k"
GPT4 = "gpt-4"
GPT4_32K = "gpt-4-32k"


### NOTES APP

NOTES_APP = 'obsidian'


### FILE PATHS

OBSIDIAN_FILE_PATH = '/Users/micke//DOKUMENT/Obsidian/Möten/'


### TEXT FORMATS - GPT AND DALL-E PROMPT PRIMERS

YOUR_OWN_PROMTP_PRIMER = '''
Agera som sekreterare och lyssna efter hur användaren vill att texten ska 
formatteras och vilken typ av möte, anteckning eller liknande det handlar om 
och formattera texten som markdown för Obsidian.
'''


FORELASNING_PROMPT_PRIMER = '''
Vänligen sammanfatta denna föreläsnings transkribering till en 
översikt som täcker de mest centrala aspekterna på ett koncist och korrekt sätt, 
vad huvudbudskapet var samt centrala teman. Formattera texten som markdown för Obsidian.
'''


GENERAL_MEET_PROMPT_PRIMER = '''
Agera som sekreterare. Sammanställ dessa mötesanteckningar på svenska och 
formattera texten som markdown för Obsidian.
'''


LEARNINGLAB_PROMPT_PRIMER = '''
Agera som expert inom livslångt lärande och lärande i organisationer. 
Sammanfatta och summera denna utmaning på svenska och formattera texten 
som markdown för Obsidian.
'''


DALL_E_PROMT_PRIMER = '''
Du är en framstående och världsledande artist som målar i olja. Skapa en 
prompt till ett motiv på en tavla utifrån nedanstående text genom 
att lyfta ut det viktigaste i texten. Prompten ska gå att använda 
i DALL-E.
'''


LINKED_IN_PROMPT_PRIMER = '''
Sammanfatta texten på ett kortfattat och kreativt sätt i form av ett 
LinkedIn-inlägg på svenska. Lägg till #-tags om du tycker att det behövs.
'''


IDEAS_PROMPT_PRIMER = '''
Agera som assistent och sammanfatta minnessanteckningarna på svenska. 
Använd ingress innehållandes det viktigaste först och därefter sammanfattning. 
Texten ska formatteras som markdown för Obsidian.
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
