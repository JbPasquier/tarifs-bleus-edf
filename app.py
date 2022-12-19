import io
import os
import pandas
from PyPDF2 import PdfFileReader
import re
from urllib.request import Request, urlopen

url = "https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille_prix_Tarif_Bleu.pdf"
remote_file = urlopen(Request(url)).read()
memory_file = io.BytesIO(remote_file)
pdf_file = PdfFileReader(memory_file)

# extracting text from page
pdf_text = pdf_file.getPage(0).extractText().splitlines()
next_is_base = False
next_is_hchp = False
next_is_tempo = False
base = []
hchp = []
tempo = []

for line in pdf_text:
  if next_is_base:
    if line[0].isdigit():
      base.append(re.split(r"\s+", line.strip()))
    else:
      next_is_base = False
  elif next_is_hchp:
    if line[0].isdigit():
      hchp.append(re.split(r"\s+", line.strip()))
    else:
      next_is_hchp = False
  elif next_is_tempo:
    if line[0].isdigit():
      tempo.append(re.split(r"\s+", line.strip()))
    else:
      next_is_tempo = False
  elif line.find("(€ TTC/mois ) (cts € TTC/kWh)") != -1:
    next_is_base = True
  elif line.find("Creuses") != -1:
    next_is_hchp = True
  elif line.find("HP") != -1:
    next_is_tempo = True

if not os.path.exists('output'):
  os.makedirs('output')

pandas.DataFrame(base, columns=['kVA', 'Abonnement (€)', 'ct€/kWh']).to_csv('output/base.csv', index=False)
pandas.DataFrame(hchp, columns=['kVA', 'Abonnement (€)', 'HP (ct€/kWh)', 'HC (ct€/kWh)']).to_csv('output/hchp.csv', index=False)
pandas.DataFrame(tempo, columns=['kVA', 'Abonnement (€)', 'Bleu HP (ct€/kWh)', 'Bleu HC (ct€/kWh)', 'Blanc HP (ct€/kWh)', 'Blanc HC (ct€/kWh)', 'Rouge HP (ct€/kWh)', 'Rouge HC (ct€/kWh)']).to_csv('output/tempo.csv', index=False)
