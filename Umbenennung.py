import os
import re
import scipy.io
import numpy as np

#Pfad zum Zielordner, bitte anpassen
ordner_pfad = 'D:\Export'

# Liste aller Dateien im Ordner
dateien = os.listdir(ordner_pfad)

# Gruppieren der Dateien nach Versuchsnummer
versuchs_gruppen = {}
for datei in dateien:
    match = re.match(r'Versuch(\d+)_(\d+).mat', datei)
    if match:
        versuchs_nummer = int(match.group(1))
        if versuchs_nummer not in versuchs_gruppen:
            versuchs_gruppen[versuchs_nummer] = []
        versuchs_gruppen[versuchs_nummer].append(datei)
print(versuchs_gruppen[4])
for versuchs_nummer, datei_liste in versuchs_gruppen.items():
    anzahl_dateien = len(datei_liste)
    # Ausgabe der Versuchsnummer und der Anzahl der Dateien
    print(f'Versuch {versuchs_nummer}: {anzahl_dateien} Datei(en)')

for item in versuchs_gruppen[1]:
    print(item)
#     # Umnummerierung innerhalb jeder Gruppe
for versuchs_nummer, datei_liste in versuchs_gruppen.items():
    datei_liste.sort()
    print(datei_liste)
    # Sortieren der Dateien, falls nötig
    for neue_nummer, datei in enumerate(datei_liste, start=0):
        alter_pfad = os.path.join(ordner_pfad, datei)
        neuer_dateiname = f'Versuch{versuchs_nummer}_{str(neue_nummer).zfill(4)}.mat'
        neuer_pfad = os.path.join(ordner_pfad, neuer_dateiname)
        print(neuer_pfad)
        #os.rename(alter_pfad, neuer_pfad)  # Umbenennen der Datei

print("Umbenennung abgeschlossen.")

def compare_mat_files(file_path1, file_path2):
    data1 = scipy.io.loadmat(file_path1)
    data2 = scipy.io.loadmat(file_path2)

    # Entfernen der Felder '__version__', '__header__', '__globals__'
    data1 = {k: v for k, v in data1.items() if k not in ['__version__', '__header__', '__globals__']}
    data2 = {k: v for k, v in data2.items() if k not in ['__version__', '__header__', '__globals__']}

    # Vergleichen der Schlüsselsets
    if set(data1.keys()) != set(data2.keys()):
        return False

    # Vergleichen der Werte für jeden Schlüssel
    for key in data1.keys():
        if not np.array_equal(data1[key], data2[key]):
            return False

    return True
#

# Ersetzen Sie die Pfade mit Ihren tatsächlichen Dateipfaden
file_path1 = 'D:\Export\Versuch10_0179.mat'
file_path2 = 'D:\Export - Kopie\Versuch10_0179.mat'

if compare_mat_files(file_path1, file_path2):
    print("Die Inhalte der Dateien sind identisch.")
else:
    print("Die Inhalte der Dateien sind unterschiedlich.")
