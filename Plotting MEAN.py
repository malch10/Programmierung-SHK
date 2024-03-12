import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Pfad zur Datenquelle und Zielordner
Pfad = 'D:/Auswertung SHK/Vergleich_aktualisiert.txt'
Plotspeicher = 'D:/Auswertung SHK/Plots_Mean'
df = pd.read_csv(Pfad, sep='\t', encoding='utf-8')

# Liste der Elektrodenpositionen
elektrodenpositionen = ['0-80', '81-161', '162-242', '243-323']

def agg_resistance(daten):
    """Aggregieren der Daten für Durchschnitt, Min, Max und extrahieren zusätzlicher Informationen."""
    return pd.Series({
        'Durchschnitt': daten['Resistance'].mean(),
        'Min': daten['Resistance'].min(),
        'Max': daten['Resistance'].max(),
        # Nehmen Sie das erste Element für Gewicht, Vorschub und Schweißelektrode
        'Gewicht': daten['Messgewicht'].iloc[0],
        'Vorschub': daten['Vorschub in mm/min'].iloc[0],
        'Schweißelektrode': daten['Schweißelektrode'].iloc[0]
    })

for i in range(0, 15, 3):
    df_filtered = df[df['Versuch'].isin([i + 1, i + 2, i + 3])]
    df_filtered['Messpunkt'] = df_filtered['Messpunkt'].astype(int)

    for elektrodenpos in elektrodenpositionen:
        df_agg = df_filtered[df_filtered['Elektrodenposition'] == elektrodenpos].groupby('Messpunkt').apply(agg_resistance).reset_index()

        plt.figure(figsize=(12, 6))
        plt.bar(df_agg['Messpunkt'], df_agg['Durchschnitt'],
                yerr=[df_agg['Durchschnitt'] - df_agg['Min'], df_agg['Max'] - df_agg['Durchschnitt']],
                error_kw=dict(capsize=5, capthick=2, ecolor='gray'), color='skyblue',
                label=f'Durchschnitt (Fehlerbalken: Min/Max)\nGewicht: {df_agg["Gewicht"].iloc[0]}, Vorschub: {df_agg["Vorschub"].iloc[0]}, Elektrode: {df_agg["Schweißelektrode"].iloc[0]}')

        plt.title(f'Durchschnittlicher Widerstand über Messpunkte für Versuch {i + 1} bis {i + 3} (Elektrodenposition {elektrodenpos})')
        plt.xlabel('Messpunkt')
        plt.ylabel('Widerstand')
        plt.xticks(df_agg['Messpunkt'])
        plt.xticks(rotation=45, fontsize=6)
        plt.legend()

        dateiname = f'Durchschnitt_Plot_Versuch_{i + 1}_bis_{i + 3}_Elektrodenpos_{elektrodenpos.replace("-", "bis")}.png'
        voller_pfad = os.path.join(Plotspeicher, dateiname)
        plt.savefig(voller_pfad)
        plt.close()
