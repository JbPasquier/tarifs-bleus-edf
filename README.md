# Tarifs Bleus EDF

Generate 3 csv files (base, hchp, tempo) from [this PDF](https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille_prix_Tarif_Bleu.pdf).

## Prerequisite

* Python 3.11
* Pandas (`pip install pandas`)
* PyPDF2 (`pip install PyPDF2`)

You may also want to use a virtualenv.

## Run

```bash
python app.py
```

3 CSV files will be generated on the `output` folder.
