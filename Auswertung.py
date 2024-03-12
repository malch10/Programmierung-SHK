import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import glob
import os
from natsort import natsorted
from scipy.integrate import simps
from scipy import integrate
import scipy.io as sio
import pandas as pd
import re
from natsort import natsorted

workdirectory = 'D:\Export'
savedirectory = 'D:\Auswertung SHK'


def moving_average(a, n=1):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

df = pd.DataFrame()



Daten=[f for f in os.listdir(workdirectory) if f.endswith('.mat')]




def find_numbers_in_filename(filename):
    # Sucht nach allen Vorkommen von Zahlen im Dateinamen
    numbers = re.findall(r'\d+', filename)

    # Überprüft, ob mindestens zwei Zahlen gefunden wurden
    if len(numbers) >= 2:
        # Konvertiert die gefundenen Zeichenketten in Integer und gibt die ersten beiden zurück
        return int(numbers[0]), int(numbers[1])
    else:
        # Gibt einen Hinweis zurück, falls weniger als zwei Zahlen gefunden wurden
        return None, None

Daten = natsorted(Daten)

for d in Daten:
    f = os.path.join(workdirectory, f'{d}')
    print(d)
    first_number, second_number = find_numbers_in_filename(d)
    try:
        file = sio.loadmat(f)

        header = sorted(file.keys())
        for key in header:                                                                                          # Daten aus Datei mittels Überschriften entsprechendem Array zuordnen
            if 'spannung' in key.lower() and not 'time' in key.lower():
                U = np.array(list(file[key]))
            elif 'strom' in key.lower() and not 'time' in key.lower():
                I = np.array(list(file[key]))
            elif 'spannung' in key.lower() and 'time' in key.lower():
                t = np.array(list(file[key]))
        I1 = moving_average(I,50)
        U1 = np.abs(moving_average(U,50))
        t1 = moving_average(t,50)

        U1=U1 - np.mean(U1[(t1> 0.2)&(t1<0.4)])#offset spannung
        R=U1/I1
        R_mean=np.mean(R[(t1>13)&(t1<15)])
        write = {'Versuchsnummer': first_number,'Messpunkt': second_number, 'Resistance': R_mean}
        df_dictionary = pd.DataFrame([write])
        df = pd.concat([df, df_dictionary], ignore_index=True)
    except ValueError as e:
        print(f"Fehler beim Lesen der Datei {f}: {e}")



