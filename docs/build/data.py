"""Données de la mission Marteau du Golan, en coordonnées DCS (x nord, y est), relevées dans la recette."""

BULLSEYE = (-210166, -13463)

BASES = {
    "Ramat David": (-259121, -75105),
    "Rosh Pina": (-225278, -37688),
}
RED_BASES = {
    "Mezzeh": (-172160, 24866),
    "Khalkhalah": (-217202, 53275),
}

JETS = [  # (nom, x, y, cap, nm, rôle)
    ("PUSH", -228000, -30000, 55, 29.6, "Point d'attente au-dessus du lac de Tibériade, hors de portée de toutes les batteries. Ravitaillement juste à l'ouest (Texaco, Arco)."),
    ("TELLHARA", -217882, 3524, 73, 19, "Le radar d'alerte 55G6. On entre ici dans l'enveloppe du SA-11."),
    ("KHAN", -203930, -7802, 321, 10, "La ligne avancée de Khan Arnabah, au contact."),
    ("COLONNE", -193800, 3500, 48, 8, "Sur la route de Sa'sa' : là où une contre-attaque se formerait."),
    ("KANAKER", -196500, 12500, 107, 5, "L'artillerie : 2S1 et BM-21."),
    ("SASA", -192000, 7500, 312, 4, "La réserve blindée de Sa'sa'."),
    ("SA6", -188500, 12500, 55, 3, "La batterie SA-6."),
    ("SA11", -181500, 31500, 70, 11, "La batterie SA-11."),
    ("KISWAH", -183810, 25553, 249, 3, "Le PC du 1er Corps, sur l'emprise militaire."),
    ("EGRESS", -232000, -25000, 226, 38, "Sortie, hors de portée de toutes les batteries, puis Ramat David (242° / 31 nm)."),
    ("BULLSEYE", -210166, -13463, 28, 13, "Quneitra, la référence de position."),
]
JETS_FROM = ("Ramat David", -259121, -75105)

HELOS = [
    ("MASADA", -198055, -19506, 34, 17.7, "Point d'attente au pied de l'Hermon, derrière la ligne alliée. On y attend « PORTE OUVERTE »."),
    ("HADAR", -194401, -11930, 64, 5, "Entrée dans le relief, en suivant les vallées."),
    ("BEITJINN", -189302, -7953, 38, 3, "Le col : le relief culmine vers 1 370 m. En sortant, on est vu du SA-6 : il doit être détruit."),
    ("SASA", -192000, 7500, 100, 8, "La réserve blindée : l'objectif principal."),
    ("KANAKER", -196500, 12500, 132, 4, "L'artillerie, si elle tient encore."),
    ("COLONNE", -193800, 3500, 287, 5, "Sur la route de Sa'sa' : guetter une contre-attaque, la prendre en flanc."),
    ("KHAN", -203930, -7802, 228, 8, "Retour par la route de Quneitra, en appui de la poussée alliée."),
    ("BULLSEYE", -210166, -13463, 222, 5, "Quneitra, puis Rosh Pina (environ 20 nm)."),
]
HELOS_FROM = ("Rosh Pina", -225278, -37688)

# Menaces connues : (nom, x, y, portée de tir m, détection m ou None)
SAMS = [
    ("SA-6 Sa'sa'", -188500, 12500, 24000, None),
    ("SA-11 Kiswah", -181500, 31500, 46300, 83300),
]
QRA = [
    ("QRA Mezzeh", -185000, 20000, 30000),
    ("QRA Khalkhalah", -210000, 30000, 30000),
]

# Objectifs : zone, titre, centre, rayon, cibles (nom, type lisible, x, y, rôle)
OBJECTIVES = [
    ("EWRTellHara", "Radar d'alerte de Tell al-Hara", "TELLHARA", (-217882, 3524), 600, [
        ("Radar 55G6", "EWR 55G6", -217882, 3524, "Alerte avancée de tout le réseau"),
        ("AAA", "AAA (tirage VEAF)", -217700, 3700, "Défense rapprochée du radar"),
    ]),
    ("SA6Sasa", "Batterie SA-6 de Sa'sa'", "SA6", (-188500, 12500), 1000, [
        ("Radar 1S91", "SA-6 radar", -188500, 12500, "Conduite de tir de la batterie"),
        ("Lanceur 1", "SA-6 2P25", -188200, 12200, ""),
        ("Lanceur 2", "SA-6 2P25", -188800, 12200, ""),
        ("Lanceur 3", "SA-6 2P25", -188200, 12800, ""),
        ("Lanceur 4", "SA-6 2P25", -188800, 12800, ""),
    ]),
    ("SA11Kiswah", "Batterie SA-11 de Kiswah", "SA11", (-181500, 31500), 1000, [
        ("Radar 9S18", "SA-11 radar", -181500, 31500, "Acquisition de la batterie"),
        ("PC 9S470", "SA-11 PC", -181650, 31650, "Poste de commandement"),
        ("Lanceur 1", "SA-11 9A310", -181150, 31200, ""),
        ("Lanceur 2", "SA-11 9A310", -181850, 31200, ""),
        ("Lanceur 3", "SA-11 9A310", -181150, 31850, ""),
        ("Lanceur 4", "SA-11 9A310", -181850, 31850, ""),
    ]),
    ("KhanArnabah", "Front de Khan Arnabah", "KHAN", (-203800, -7500), 3500, [
        ("Blindés nord", "Groupe blindé (tirage VEAF)", -202800, -8800, "Chars et véhicules retranchés"),
        ("Blindés sud", "Groupe blindé (tirage VEAF)", -205200, -8200, "Chars et véhicules retranchés"),
        ("BMP-2", "3 × BMP-2", -204000, -9500, "Infanterie mécanisée"),
        ("AAA", "AAA (tirage VEAF)", -202600, -7300, "Défense rapprochée"),
        ("SA-13", "SA-13 Strela-10", -204800, -6800, "Missiles infrarouges, courte portée"),
        ("SA-15", "SA-15 Tor", -202500, -5500, "Missiles à guidage radar, la menace n° 1 du front"),
    ]),
    ("ArtiKanaker", "Artillerie de Kanaker", "KANAKER", (-196500, 12500), 1500, [
        ("Obusiers", "4 × 2S1 Gvozdika", -196800, 12200, "Feux sur la ligne de contact"),
        ("Lance-roquettes", "3 × BM-21 Grad", -196100, 12900, "Saturation de zone"),
        ("AAA", "AAA (tirage VEAF)", -196500, 12600, "Défense rapprochée"),
    ]),
    ("Sasa", "Réserve blindée de Sa'sa'", "SASA", (-192000, 7500), 2500, [
        ("T-72B3", "4 × T-72B3", -191500, 6500, "Le cœur de la réserve"),
        ("BMP-2", "3 × BMP-2", -192800, 8200, "Infanterie mécanisée"),
        ("Blindés", "Groupe blindé (tirage VEAF)", -190800, 8800, "Renfort de la réserve"),
        ("SA-8", "SA-8 Osa", -191200, 7600, "Missiles à guidage radar, environ 10 km"),
        ("SA-19", "SA-19 Tunguska", -192600, 6300, "Canons et missiles"),
    ]),
    ("Kiswah", "PC du 1er Corps à Kiswah", "KISWAH", (-183825, 25509), 1200, [
        ("Centre de commandement", "Bâtiment", -183811, 25553, "Le commandement du Corps"),
        ("Tour de transmissions", "Pylône", -183686, 25794, "Les liaisons avec le front"),
        ("Bunker de conduite des feux", "Bunker", -183986, 25394, "La coordination de l'artillerie"),
        ("Bunker 2", "Bunker", -183636, 25344, "Abri du commandement"),
        ("AAA", "AAA (tirage VEAF)", -184186, 25894, "Défense rapprochée"),
    ]),
]

COLONNE_ROUTE = [(-193800, 3500), (-197693, -2500), (-203930, -7802), (-208500, -12500)]
POUSSEE_ROUTE = [(-211000, -15500), (-210166, -13463), (-203930, -7802), (-197693, -2500), (-193800, 3500)]
FRONT_LINE = [(-222000, -11500), (-213000, -13800), (-206000, -15200), (-200500, -16500), (-195500, -17500)]

FRIENDLIES = [  # (nom, x, y)
    ("Merkava", -207500, -17500),
    ("Merkava", -213100, -17200),
    ("Infanterie", -200000, -18500),
    ("M109", -217300, -21000),
    ("Avenger", -209500, -19500),
    ("PC brigade", -215000, -22000),
]
JTAC = ("JTAC Abu Nada", -206900, -16700)

SUPPORT = [  # (nom, (x1, y1), (x2, y2), libellé)
    ("Magic", (-262000, -78000), (-232000, -78000), "Magic (AWACS) FL300"),
    ("Texaco", (-250000, -55000), (-225000, -55000), "Texaco-1 FL180 (panier)"),
    ("Arco", (-255000, -48000), (-230000, -48000), "Arco-1 FL220 (perche)"),
]
