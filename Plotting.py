import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Pfad zur Datenquelle
Pfad = 'D:/Auswertung SHK/Vergleich_aktualisiert.txt'
Plotspeicher = 'D:/Auswertung SHK/Plots'
df = pd.read_csv(Pfad, sep='\t', encoding='utf-8')

# Liste der Elektrodenpositionen
elektrodenpositionen = ['0-80', '81-161', '162-242', '243-323']

# Schleife über alle Versuchsgruppen
for i in range(0, 15, 3):
    # Filtern der Daten für die aktuelle Versuchsgruppe
    df_filtered = df[df['Versuch'].isin([i + 1, i + 2, i + 3])]
    df_filtered['Messpunkt'] = df_filtered['Messpunkt'].astype(int)

    # Schleife über alle Elektrodenpositionen
    for elektrodenpos in elektrodenpositionen:
        # Filtern der Daten für die aktuelle Elektrodenposition
        df_filtered_pos = df_filtered[df_filtered['Elektrodenposition'] == elektrodenpos]

        # Erstellen des Barplots
        plt.figure(figsize=(12, 6))
        barplot = sns.barplot(data=df_filtered_pos, x='Messpunkt', y='Resistance', hue='Versuch', errorbar=None, palette=['red', 'green', 'blue'])

        plt.title(f'Widerstand über Messpunkte für Versuch {i + 1} bis {i + 3} (Elektrodenposition {elektrodenpos})')
        plt.xlabel('Messpunkt')
        plt.ylabel('Widerstand')

        # Anpassen der Legende mit zusätzlichen Informationen
        ax = plt.gca()
        handles, labels = ax.get_legend_handles_labels()
        new_labels = []
        for label in labels:
            versuchsdaten = df_filtered[df_filtered['Versuch'] == int(label)]
            gewicht = versuchsdaten['Messgewicht'].iloc[0]
            vorschub = versuchsdaten['Vorschub in mm/min'].iloc[0]
            schweisselektrode = versuchsdaten['Schweißelektrode'].iloc[0]
            new_label = f'Versuch {label}: Gewicht={gewicht}, Vorschub={vorschub}, Elektrode={schweisselektrode}'
            new_labels.append(new_label)
        plt.legend(handles, new_labels, title='Versuchsdetails', loc='upper right')

        # Anpassen der Schriftgröße der Tick-Labels auf der X-Achse
        barplot.set_xticklabels(barplot.get_xticklabels(), fontsize=7, rotation=45)
        plt.tight_layout()
        # Speichern des Plots
        dateiname = f'Plot_Versuch_{i+1}_bis_{i+3}_Elektrodenpos_{elektrodenpos.replace("-", "bis")}.png'
        voller_pfad = os.path.join(Plotspeicher, dateiname)
        plt.savefig(voller_pfad)
        plt.close()  # Schließt die Figur, um Ressourcen freizugeben
