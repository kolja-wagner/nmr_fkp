# Kernspinresonans-Spektroskopie
Teil des Fortgeschrittenenpraktikum der LUH.
Datenauswertung für den Versuch.



## Daten:

- Die Ordner `data_day_one / *_two, / *_three` enthalten die an den drei Tagen aufgenommen Messwerte. (Aufnahme mit digitalem Speicheroszilloskop).
- Eine Liste der zusätzlich aufgenommenen Parameter ist in `data_day_one.csv / *_two.csv / *_three.csv` gespeichert.
- In `datetime.csv` sind die Aufnahmezeitpunkte der einzelnen Messungen extrahiert.
- `IMAGES` ist der Export-Pfad für alle mit matplotlib generierten Abbildungen.

## Code:

- `config_parser.py`: Datenstruktur und Parser für die Config-Dateien des Speicheroszilloskop
- `file_organizer.py`: Einlesen und Verarbeiten von Messreihen in pd.Dataframes
- `ctime.py`: Auslesen des Aufnahmezeitpunkt aus den Rohdaten.
- `func.py`: Diverse Hilfsfunktionen.

Die Notebooks entsprechen den einzelnen Abschnitten der Versuchsauswertung. 
