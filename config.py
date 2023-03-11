# version = 0.2

### API KEYS AND CREDENTIALS

OPEN_AI_API_KEY = 'yourapikeyforopenai'


### NOTES APP

NOTES_APP = 'obsidian'


### FILE PATHS

OBSIDIAN_FILE_PATH = '/Users/micke/Obsidian/Micke/Möteanteckningar/'


### TEXT FORMATS - GPT AND DALL-E PROMPT PRIMERS

DALL_E_PROMT_PRIMER = "As a graphic designer, write a prompt for DALL-E that you think matches the \
							text below. Avoid using text in the image."

LINKED_IN_PROMPT_PRIMER = 'Sammanfatta texten på ett kreativt sätt i form av ett LinkedIn-inlägg på svenska. \
							Lägg till #-tags om du tycker att det behövs.'

IDEAS_PROMPT_PRIMER = 'Agera som assistent och sammanfatta minnessanteckningarna. Använd ingress \
							innehållandes det viktigaste först och därefter sammanfattning.'

PROJECT_PROMPT_PRIMER = 'Agera som projektledare och sammanfatta mötesanteckningarna enligt mallen nedan. \
						Det ska formatteras som markdown för Obsidian. \nMALL----\n \
						# Projektnamn: {{projektnamn}} \n\nLänkar:: [[projektbeskrivning]]\nDatum:: \
						 {{date}}\nTid:: {{time}}\nStatus:: #status-ny #status-pågående #status-avslutad \
						  #status-reflektion\nMOC:: \nKontext::\n\n## Inledning\n{{hur sammanfattar du \
						  och förklarar projektet mycket kort?}}\n\n## Bakgrund\n{{Vad är projektets \
						  bakgrund och varför finns det? För vem och vilket behov?}}\n\n## Syfte och \
						  mål\n{{Vad är projektets syfte? Vilka (SMARTa) mål har projektet?}}\n\n## \
						  Genomförande\n{{Hur ska projektet genomföras? Finns det några faser eller \
						  steg i projektet som måste genomföras? Vilka metoder används i projektets \
						  genomförande?}}\n\n## Organisering\n{{Hur organiseras projektet? Hur ser \
						  projektets ledning och styrning ut? Hur går det till att fatta beslut i \
						  projektet? Vilka är projektets primära resurser och kompetenser?}}\n\n## \
						  Förväntade resultat\n{{När projektet har uppnått sina målsättningar, vilka \
						  är de förväntade resultaten som uppstår när målen uppfylls? Vilka långsiktiga \
						  effekter finns att vänta av att projektets mål och resultat uppstår?}}\n\n## \
						  Budget\n{{Vilka intäkter och kostnader har projektet? Hur säkrar projektet \
						  sin finansiering?}}\n\n## Samverkan\n{{Vilken samverkan behöver finnas på \
						  plats för att projektet ska uppnå sina resultat? Vilka andra intressenter \
						  finns? Hur förhåller sig projektet till sina intressenter?}}\n\n## \
						  Kontaktuppgifter\n{{Vem kontaktar man för att veta mer om projektet?}}\n\n## \
						  Källor\n{{Här skrivs vilka externa källor, om sådana finns, projektbeskrivningen \
						  syftar till}}'

