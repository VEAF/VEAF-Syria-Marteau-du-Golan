"""La liste des prises : (nom, préfixe de groupe à viser, titre, cap = axe d'engagement, distance oblique, inclinaison)."""
SHOTS = [
    ("01-tellhara", ["EWRTellHara"], "Radar d'alerte de Tell al-Hara", 73, 900, 30),
    ("02-sa6", ["SA6Sasa"], "Batterie SA-6 de Sa'sa'", 47, 1000, 30),
    ("03-sa11", ["SA11Kiswah"], "Batterie SA-11 de Kiswah", 70, 1100, 30),
    ("04-khan-sa15", ["KhanArnabah [r] SA15"], "Khan Arnabah : SA-15", 43, 600, 30),
    ("05-khan-blindes-nord", ["KhanArnabah [r] Armored Platoon#10382"], "Khan Arnabah : blindés nord", 43, 650, 30),
    ("06-khan-blindes-sud", ["KhanArnabah [r] Armored Platoon#10379"], "Khan Arnabah : blindés sud", 43, 700, 30),
    ("07-khan-bmp", ["KhanArnabah [r] KhanArnabah-bmp"], "Khan Arnabah : BMP-2", 43, 600, 30),
    ("08-khan-aaa", ["KhanArnabah [r] Air Defense"], "Khan Arnabah : AAA", 43, 650, 30),
    ("08b-khan-sa13", ["KhanArnabah [r] SA13"], "Khan Arnabah : SA-13", 43, 600, 30),
    ("09-kanaker", ["ArtiKanaker"], "Artillerie de Kanaker", 107, 1000, 30),
    ("10-sasa", ["Sasa "], "Réserve blindée de Sa'sa'", 100, 3400, 52),
    ("11-kiswah", ["Kiswah [r]"], "PC du 1er Corps à Kiswah", 249, 900, 30),
]
# Statiques (absentes de coalition.getGroups) : nom, x, y
STATICS = {"11-kiswah": [("Centre de commandement", -183811, 25553), ("Tour de transmissions", -183686, 25794),
                         ("Bunker de conduite des feux", -183986, 25394), ("Bunker 2", -183636, 25344)]}
