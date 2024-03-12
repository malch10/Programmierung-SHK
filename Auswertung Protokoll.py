import pandas as pd
import re

# Pfad zu Ihren Dateien (bitte entsprechend anpassen)
protokoll_pfad = 'D:/Auswertung SHK/Protokoll.txt'
vergleich_pfad = 'D:/Auswertung SHK/Vergleich.txt'

# Dateien einlesen
df_P = pd.read_csv(protokoll_pfad, sep='\t', encoding='utf-16')  # Pfad und Optionen ggf. anpassen
df_V = pd.read_csv(vergleich_pfad, sep='\t')  # Pfad und Optionen ggf. anpassen

# Funktion zur Extraktion von Zahlen aus einem Namen
def extract_numbers(name):
    if isinstance(name, str):
        numbers = re.findall(r'\d+', name)
        return int(numbers[0])
    else:
        return []

# Funktion zum Überprüfen, ob ein Wert im Bereich liegt
def in_range(range_str, value):
    start, end = [int(x) for x in range_str.split('-')]
    return start <= value <= end

# Zahlen aus dem Namen extrahieren und in separate Spalten einfügen (falls noch benötigt)
df_P['Versuch'] = df_P['Versuchsnummer'].apply(extract_numbers)

# Ergebnisliste vorbereiten
results = []

for index_v, row_v in df_V.iterrows():
    for index_p, row_p in df_P.iterrows():
        #print(row_p['Elektrodenposition'],row_v['Messpunkt'],row_p['Versuch'],row_v['Versuchsnummer'])
        # Überprüfen, ob der Messpunkt im Bereich liegt, der in der Spalte Elektrodenposition angegeben ist
        if in_range(row_p['Elektrodenposition'], int(row_v['Messpunkt'])) and row_p['Versuch'] == int(row_v['Versuchsnummer']):
            # Erstelle ein Dictionary aus den Zeilen von df_V und df_P
            combined_data = {**row_v.to_dict(), **row_p.to_dict()}
            results.append(combined_data)
            break  # Unterbreche die Schleife, wenn eine Übereinstimmung gefunden wurde


# Neuen DataFrame aus den Ergebnissen erstellen
df_V_expanded = pd.DataFrame(results)

# Speichern des aktualisierten DataFrames
speicherpfad = 'D:/Auswertung SHK/Vergleich_aktualisiert.txt'
df_V_expanded.to_csv(speicherpfad, sep='\t', encoding='utf-8', index=False)

# Ausgabe der ersten Zeilen des aktualisierten DataFrames zur Überprüfung
print(df_V_expanded.describe())

