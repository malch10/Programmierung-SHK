import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

def widerstand_zu_magma_farbe(widerstand):
    # Stellen Sie sicher, dass der Widerstandswert im erwarteten Bereich liegt
    widerstand = max(0, min(widerstand, 50))

    # Umrechnen des Widerstandswerts in einen Wert zwischen 0 und 1
    normierter_wert = widerstand / 50

    # Zugriff auf die Plasma-Farbkarte und Berechnung der entsprechenden Farbe
    farbe = plt.cm.magma(normierter_wert)

    # Konvertiere die Farbe zu einem RGB-Format mit Ganzzahlwerten
    return tuple(int(kanal * 255) for kanal in farbe[:3])




def generate_points():


    #Anpassen an das aktuelle Ausgangsbild (Bei gleichem Bild ist keine Änderung erforderlich)
    img_path_template = "R:/G-Code/230130_Widerholungsversuche_2_roh.png"
    save_path_template = "R:/G-Code/Bildspeicher/230130_Widerholungsversuche_{versuch}_eingezeichnet.png"

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

        #Anpassen wenn sich das Ausgangsbild nach einer Anzahl an Versuchen ändert
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
                farbe = widerstand_zu_magma_farbe(widerstand)

                draw.line((a - 3, b - 3, a + 3, b + 3), fill=farbe, width=3)
                draw.line((a + 3, b - 3, a - 3, b + 3), fill=farbe, width=3)
                draw.text((a + 5, b + 5), c, fill="white", stroke_width=1, stroke_fill='black', font_size = 7)

            # Speichere das modifizierte Bild für jeden Versuch
            img.save(save_path_template.format(versuch=versuch), 'PNG')
            path = "R:/G-Code/Bildspeicher/230130_Widerholungsversuche_" + str(versuch) + "_eingezeichnet.png"
            unterteile_bild_und_fuege_farbskala_hinzu(path, 50, 0)


####################################################################################################################


def erzeuge_farbskala(legende_hoehe, legende_breite):
    # Farbverlauf erzeugen
    legende_img = Image.new("RGB", (legende_breite, legende_hoehe))
    legende_draw = ImageDraw.Draw(legende_img)

    for y in range(legende_hoehe):
        normierter_wert = y / legende_hoehe
        farbe = plt.cm.magma(normierter_wert)[:3]
        farbe_rgb = tuple(int(kanal * 255) for kanal in farbe)
        legende_draw.line((0, y, legende_breite, y), fill=farbe_rgb)
    return legende_img


def unterteile_bild_und_fuege_farbskala_hinzu(bildpfad, min_widerstand, max_widerstand):
    img = Image.open(bildpfad)
    breite, hoehe = img.width // 2, img.height // 2

    # Farbskala-Einstellungen
    legende_breite = 25
    legende_hoehe = 100
    legende_img = erzeuge_farbskala(legende_hoehe, legende_breite)

    teilbilder = []

    # Bild in vier Teile unterteilen und Farbskala hinzufügen
    for i in range(2):
        for j in range(2):
            box = (i * breite, j * hoehe, (i + 1) * breite, (j + 1) * hoehe)
            teilbild = img.crop(box)
            draw = ImageDraw.Draw(teilbild)
            teilbild.paste(legende_img, (breite - legende_breite - 10, hoehe - legende_hoehe - 10))

            # Füge Text für die Legende hinzu
            try:
                font = ImageFont.truetype("arial.ttf", 10)
            except IOError:
                font = ImageFont.load_default()
            draw.text((breite - legende_breite - 5, hoehe - legende_hoehe - 20), str(max_widerstand), fill="black",
                      font=font)
            draw.text((breite - legende_breite - 5, hoehe - 10), str(min_widerstand), fill="white", font=font)

            teilbilder.append(teilbild)

    # Teilbilder speichern oder anzeigen
    for index, bild in enumerate(teilbilder):
        elektrode= number(index)
        neuer_dateiname = "{}_{}.png".format(bildpfad.rsplit('.', 1)[0], elektrode)
        bild.save(neuer_dateiname, 'PNG')



#Funktin number macht, dass der Elektrode der richte Namen zugeordnet wird
def number(number):
    if number == 0:
        return 4
    elif number ==1:
        return 1
    elif number ==2:
        return 3
    else:
        return 2

###################################################################################################################################
generate_points()

