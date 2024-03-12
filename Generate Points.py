import pandas as pd
from PIL import Image, ImageDraw, ImageFont

def widerstand_zu_farbe(widerstand):
    # Beispiel für Farbabstufungen basierend auf Widerstandswerten
    if widerstand <= 10:
        return "green"
    elif widerstand <= 20:
        return "yellow"
    elif widerstand <= 30:
        return "orange"
    else:
        return "red"

def generate_points():
    img_path_template = "R:/G-Code/230130_Widerholungsversuche_2_roh.png"
    save_path_template = "R:/G-Code/230130_Widerholungsversuche_{versuch}_eingezeichnet.png"

    # Lese die CSV-Dateien
    csv_path = 'R:/G-Code/230130_Widerholungsversuche_2.csv'
    vergleich_path = 'R:/Auswertung SHK/Vergleich_aktualisiert.txt'
    nc_punkte = pd.read_csv(csv_path)
    data = pd.read_csv(vergleich_path, sep='\t')
    Widerstand = data[['Messpunkt', 'Resistance', 'Versuch']]
    # Entferne die erste Spalte in nc_punkte, wenn nicht benötigt
    nc_punkte.drop(columns=nc_punkte.columns[0], axis=1, inplace=True)

    # Gruppiere die Daten nach 'Versuch'
    gruppierte_daten = Widerstand.groupby('Versuch')

    for versuch, gruppe in gruppierte_daten:
        if versuch > 9:
            # Öffne ein neues Bild für jeden passenden Versuch
            img = Image.open(img_path_template)
            draw = ImageDraw.Draw(img)

            for index, row in gruppe.iterrows():
                # Passe den Messpunkt an (um 1 verringern)
                aangepasster_messpunkt = row['Messpunkt'] + 1
                # Finde den passenden Messpunkt in nc_punkte
                punkt = nc_punkte[nc_punkte['Messpunkt'] == aangepasster_messpunkt].iloc[0]
                a, b = int(punkt['x']), int(punkt['y'])
                c = str(punkt['Messpunkt'])  # Füge 1 hinzu, um die ursprüngliche Nummerierung zu zeigen
                widerstand = row['Resistance']
                farbe = widerstand_zu_farbe(widerstand)

                draw.line((a - 3, b - 3, a + 3, b + 3), fill=farbe, width=3)
                draw.line((a + 3, b - 3, a - 3, b + 3), fill=farbe, width=3)
                draw.text((a + 5, b + 5), c, fill="white", stroke_width=1, stroke_fill='black', font_size = 7)

            # Speichere das modifizierte Bild für jeden Versuch
            img.save(save_path_template.format(versuch=versuch), 'PNG')

generate_points()
