"""Assemble le briefing Marteau du Golan : docs/briefing.pptx et docs/briefing.pdf, au modèle VEAF."""
import math
from pathlib import Path

from alts import TARGET_FT, WP_M
from data import BULLSEYE, HELOS, JETS, OBJECTIVES
from deck import (BLUE, BORDEAUX, DARK, GREY, LIGHT, Img, P, Para, RP, Rect, Run, Slide, Table, Text, to_pdf,
                  to_pptx)
from geo import dcs_to_latlon, to_dms

DOCS = Path(__file__).parent.parent
MAPS = DOCS / "maps-hd"
PAGES = Path(__file__).parent / "pages"
RECON_DIR = DOCS / "recon"
RECON = {"EWRTellHara": ["01-tellhara"], "SA6Sasa": ["02-sa6"], "SA11Kiswah": ["03-sa11"],
         "KhanArnabah": ["04-khan-sa15", "05-khan-blindes-nord", "06-khan-blindes-sud", "07-khan-bmp", "08-khan-aaa", "08b-khan-sa13"],
         "ArtiKanaker": ["09-kanaker"], "Sasa": ["10-sasa"], "Kiswah": ["11-kiswah"]}
PAGES.mkdir(exist_ok=True)


def be(x, y):
    dx, dy = x - BULLSEYE[0], y - BULLSEYE[1]
    return f"{(math.degrees(math.atan2(dy, dx)) + 360) % 360:03.0f}° / {math.hypot(dx, dy) / 1852:.1f} nm"


def coords(x, y):
    lat, lon = dcs_to_latlon(x, y)
    return f"{to_dms(lat, 'N', 'S')} {to_dms(lon, 'E', 'W')}"


S = []

# 1 — Couverture
S.append(Slide(items=[
    Rect(0, 0, 13.333, 7.5, fill=(255, 255, 255)),
    Text(0.7, 2.2, 7.2, 1.6, [P("Marteau du Golan", 54, True)]),
    Text(0.7, 3.7, 7.2, 1.2, [P("Mission VEAF — Syria", 22, color=GREY), P("Soirée du 29 octobre 2026 — 6 à 12 pilotes", 18, color=GREY)]),
    Rect(8.4, 1.4, 0.04, 4.7, fill=BLUE),
    Text(8.7, 1.5, 4.3, 4.6, [P("Sommaire", 20, True, after=12)] + [P(t, 16, after=8) for t in (
        "Situation stratégique", "Situation générale", "ATO", "Situation tactique", "Objectifs et cibles",
        "Déroulement de la mission", "Plan de vol, étape par étape", "Déploiement et coordination",
        "Plan de fréquences")]),
]))

# 2 — Situation stratégique
S.append(Slide("Situation stratégique", [Text(0.6, 1.2, 12.1, 6.0, [
    P("Depuis l'automne, le plateau du Golan est redevenu une ligne de fracture. Le 1er Corps syrien a avancé ses brigades jusqu'au contact de la Purple Line, a installé un réseau sol-air serré entre Damas et Quneitra, et ses artilleurs ont pris pour cible, à plusieurs reprises, les villages et les positions alliées du plateau. Les appels à la désescalade sont restés sans effet : chaque semaine, la menace d'une offensive syrienne vers la Galilée se précise.", 17, after=14),
    P("La coalition a reçu un mandat limité : briser la capacité offensive du 1er Corps sur le Golan, sans viser Damas ni chercher à occuper le pays. L'objectif politique est de repousser la menace hors de portée des villages alliés et de revenir à la table des négociations en position de force. Cela impose une opération courte, ciblée, menée en une seule séance : si elle s'enlise, les soutiens diplomatiques de la coalition s'effriteront et l'adversaire aura le temps de faire monter ses réserves.", 17, after=14),
    P("Le moment est choisi avec soin. Le 1er Corps a engagé sa ligne avancée à Khan Arnabah, mais sa réserve blindée attend encore à Sa'sa', à quinze nautiques en arrière : la frapper avant qu'elle ne monte au front, c'est priver le Corps de sa seule capacité de contre-attaque. Le PC de Kiswah et le réseau de défense aérienne sont la colonne vertébrale du dispositif : sans eux, le front ne voit plus et ne commande plus.", 17, after=0),
])]))

# 3 — Situation générale
S.append(Slide("Situation générale", [Text(0.6, 1.15, 12.1, 6.2, [
    RP("Contexte :", "la coalition attaque en profondeur, en fin d'après-midi, soleil dans le dos. Les F-16 ouvrent la porte en aveuglant le réseau sol-air, les F/A-18 tiennent le ciel puis frappent le PC du Corps, les A-10 et les Harrier travaillent la ligne de Khan Arnabah. Les hélicoptères contournent le front par le pied de l'Hermon et vont détruire la réserve de Sa'sa' là où elle attend. Quand le front est dégarni, la brigade alliée franchit la ligne à Quneitra.", 15, 10),
    RP("Mission :", "aveugler le réseau sol-air ; détruire la ligne de Khan Arnabah et l'artillerie de Kanaker ; détruire la réserve de Sa'sa' ; tenir le ciel face aux QRA. Objectif secondaire : frapper le PC du 1er Corps à Kiswah, derrière son SA-11.", 15, 10),
    RP("Bullseye :", "Quneitra, la vieille ville (point BULLSEYE de chaque plan de vol).", 15, 10),
    RP("Départ :", "slots dynamiques, au parking. Jets à Ramat David, hélicoptères à Rosh Pina (12 places).", 15, 10),
    RP("Menace :", "SA-11 à Kiswah, SA-6 à Sa'sa', radar d'alerte à Tell al-Hara, en réseau. Au front et en profondeur : SA-15, SA-13, SA-8, SA-19, AAA. En l'air : QRA de MiG-29S à Mezzeh et de MiG-23MLD à Khalkhalah.", 15, 10),
    RP("Météo :", "nuages fragmentés (broken) à 3 000 m (9 800 ft), qui couvrent environ 70 % du ciel ; l'Hermon (2 790 m) culmine juste dessous. Vent du 270 : 10 kt au sol à Ramat David, 13 kt à Rosh Pina, 17 kt sur le plateau du Golan ; 18 à 20 kt en basse couche (500 à 2 000 ft sol), 16 kt au FL100, 27 kt au-dessus du FL220. Visibilité maximale, 18 °C.", 15, 10),
    RP("Horaire :", "16 avril, 15h00 locale ; attaque vers 15h30, retour avant la nuit.", 15, 0),
])]))

# 4 — ATO
flights = [("NINJA", "F-16C", "SEAD", "Ramat David", "HARM, Maverick"), ("ARCTIC", "F/A-18C", "BARCAP puis strike", "Ramat David", "AMRAAM, JDAM"),
           ("ARCHER", "A-10C", "CAS", "Ramat David", "Armement libre"), ("JEDI", "AV-8B", "CAS", "Ramat David", "Armement libre"),
           ("BLADE", "AH-64D, OH-58D, Mi-24P", "Percée, réserve", "Rosh Pina", "Armement libre")]
items = [Text(0.5, 1.05, 4, 0.4, [P("PACKAGE", 16, True)])]
for i, (cs, ac, role, base, load) in enumerate(flights):
    col, row = i % 2, i // 2
    x, y = 0.5 + col * 4.2, 1.5 + row * 1.95
    items += [Rect(x, y, 4.0, 1.8, line=(180, 180, 180)),
              Text(x + 0.05, y + 0.05, 3.9, 0.75, [Para([Run(cs, True, color=BLUE), Run(f"  {ac}", True)], 15, space_after=0),
                                                    Para([Run(f"{role} — {base}, slot dyn", italic=True, color=GREY)], 12, space_after=0)]),
              Text(x + 0.05, y + 0.8, 2.2, 1.0, [P(f"{n}.", 11, color=GREY, after=0) for n in range(1, 5)]),
              Text(x + 2.2, y + 0.8, 1.75, 1.0, [P("Emport", 11, True, after=0), P(load, 11, after=0)])]
items += [Rect(8.95, 1.05, 0.03, 6.0, fill=(200, 200, 200)),
          Text(9.15, 1.05, 3.8, 6.2, [
              P("MOYENS DE SOUTIEN", 16, True, after=8),
              Para([Run("MAGIC  ", True, color=BORDEAUX), Run("AWACS, E-3A")], 13, space_after=4),
              Para([Run("TEXACO-1  ", True, color=BORDEAUX), Run("ravitailleur à panier, KC-135MPRS, FL180, 60Y")], 13, space_after=4),
              Para([Run("ARCO-1  ", True, color=BORDEAUX), Run("ravitailleur à perche, KC-135, FL220, 64Y")], 13, space_after=4),
              Para([Run("ABU NADA  ", True, color=BORDEAUX), Run("JTAC au sol, Tel Abu Nada, code 1511")], 13, space_after=4),
              Para([Run("FAT COW  ", True, color=BORDEAUX), Run("CH-47 du CTLD, pour les hélicoptères")], 13, space_after=14),
              P("CONTRÔLE", 16, True, after=8),
              Para([Run("GCI  ", True, color=BORDEAUX), Run("Magic")], 13, space_after=4),
              Para([Run("ATC  ", True, color=BORDEAUX), Run("tours silencieuses : auto-annonces sur la fréquence de la base")], 13, space_after=4),
          ])]
S.append(Slide("ATO", items))

# 5-6 — Situation tactique
S.append(Slide("Situation tactique", [Img(1.08, 1.05, 11.18, 6.3, str(MAPS / "sitac-generale.png"))]))
S.append(Slide("Situation tactique — zone des combats", [Img(1.08, 1.05, 11.18, 6.3, str(MAPS / "sitac-front.png"))]))

# 7… — objectifs : carte + récit, puis fiches cibles
STORY = {
    "EWRTellHara": "Sur sa colline, au sud du front, un radar d'alerte avancée 55G6 voit tout le plateau et renseigne les batteries du réseau. Tant qu'il vit, les batteries restent éteintes et ne s'allument qu'au dernier moment ; quand il tombe, elles passent en autonome et restent allumées, ce qui en fait des cibles plus faciles pour les missiles antiradar.",
    "SA6Sasa": "Elle couvre Sa'sa' et la sortie du col de Beit Jinn, que les hélicoptères doivent franchir. C'est la clé de la manœuvre : tant qu'elle n'est pas détruite, Blade attend à MASADA. Portée de tir d'environ 24 km.",
    "SA11Kiswah": "Elle protège le PC du Corps, et son enveloppe (environ 25 nm) s'étend jusqu'à TELLHARA et à la limite de Khan Arnabah. La frappe sur Kiswah ne part qu'après sa chute.",
    "KhanArnabah": "Des chars et des BMP-2 retranchés autour du bourg, couverts par de la AAA, un SA-13 et un SA-15 : c'est le verrou de la route de Quneitra. Sa chute ouvre la route à la brigade alliée ; elle pourrait aussi pousser le 1er Corps à contre-attaquer rapidement.",
    "ArtiKanaker": "Quatre obusiers 2S1 et trois lance-roquettes BM-21 appuient la ligne : la poussée alliée n'a aucune chance tant qu'ils tirent.",
    "Sasa": "Des T-72 et des BMP-2 en attente à l'est du bourg, sous la protection d'un SA-8 et d'un SA-19. C'est la cible principale des hélicoptères. Le renseignement estime que, si Khan Arnabah tombe, le Corps pourrait engager ce qui lui reste de blindés par la route de Quneitra : si une colonne se présente, elle doit être cassée avant le contact avec nos lignes.",
    "Kiswah": "Un centre de commandement, une tour de transmissions et deux bunkers, sur l'emprise militaire au nord-ouest du bourg. Sous la couche à 3 000 m, une bombe guidée par GPS est le choix le plus sûr ; une bombe laser larguée au-dessus des nuages risque de perdre la tache.",
}
WHO = {"EWRTellHara": "Ninja", "SA6Sasa": "Ninja", "SA11Kiswah": "Ninja, Arctic en escorte", "KhanArnabah": "Archer, Jedi, Blade (JTAC Abu Nada)",
       "ArtiKanaker": "Archer, Jedi, Blade", "Sasa": "Blade, Archer, Jedi", "Kiswah": "Arctic"}
k = 0
for zone, title, wp, c, r, targets in OBJECTIVES:
    sec = " (secondaire)" if zone in ("SA11Kiswah", "Kiswah") else ""
    S.append(Slide(f"{wp} — {title}{sec}", [
        Img(0.4, 1.05, 8.9, 8.9 * 1350 / 2400, str(MAPS / f"objectif-{zone.lower()}.png")),
        Text(9.5, 1.05, 3.5, 6.2, [
            P(STORY[zone], 14, after=12),
            RP("Pour :", WHO[zone], 14, 8),
            RP("Bullseye :", be(*c), 14, 8),
            RP("Point :", f"{wp} du plan de vol", 14, 0),
        ]),
    ]))
    photos = RECON.get(zone, [])
    for j in range(0, len(photos), 2):
        pair = photos[j:j + 2]
        if len(pair) == 1:
            S.append(Slide(f"{wp} — photo de reconnaissance", [
                Img(0.4, 1.05, 9.2, 9.2 * 1810 / 2650, str(RECON_DIR / f"{pair[0]}.jpg")),
                Text(9.8, 1.05, 3.2, 6.0, [P("Prise de vue dans l'axe d'engagement prévu ; le cap est inscrit sur la photo.", 13, after=10),
                                           P("Les groupes tirés au hasard par la zone peuvent différer le soir de la mission.", 12, color=GREY, italic=True)])]))
        else:
            S.append(Slide(f"{wp} — photos de reconnaissance", [
                Img(0.4, 1.3, 6.15, 6.15 * 1810 / 2650, str(RECON_DIR / f"{pair[0]}.jpg")),
                Img(6.78, 1.3, 6.15, 6.15 * 1810 / 2650, str(RECON_DIR / f"{pair[1]}.jpg")),
                Text(0.4, 5.75, 12.5, 0.6, [P("Prises de vue dans l'axe d'engagement prévu (cap inscrit sur chaque photo). Les groupes tirés au hasard par la zone peuvent différer le soir de la mission.", 12, color=GREY, italic=True)])]))
    cards = []
    for i, (name, kind, x, y, role) in enumerate(targets):
        col, row = i % 3, i // 3
        X, Y = 0.5 + col * 4.15, 1.1 + row * 3.1
        cards += [Rect(X, Y, 4.0, 2.95, fill=LIGHT),
                  Img(X + 0.1, Y + 0.1, 1.55, 1.55, str(MAPS / f"cible-{zone.lower()}-{i}.png")),
                  Text(X + 1.75, Y + 0.08, 2.2, 1.6, [P(name, 14, True, after=2), P(kind, 11, color=GREY, after=4),
                                                       P(role or " ", 11, after=0)]),
                  Text(X + 0.1, Y + 1.75, 3.85, 1.15, [P(coords(x, y), 11, after=2),
                                                        P(f"Sol : {TARGET_FT[k]} ft   Bullseye : {be(x, y)}", 11, after=0)])]
        k += 1
    S.append(Slide(f"{wp} — fiches cibles", cards + [
        Text(0.5, 7.05, 12.3, 0.35, [P("Les groupes « tirage VEAF » sont composés à l'activation de la zone : leur nature exacte varie d'une partie à l'autre.", 10, color=GREY, italic=True)])]))

# Déroulement de la mission
S.append(Slide("Déroulement de la mission", [Text(0.6, 1.1, 12.1, 6.3, [
    RP("Objectifs principaux :", "le radar de Tell al-Hara, la ligne de Khan Arnabah, l'artillerie de Kanaker et la réserve de Sa'sa'. L'opération est terminée quand ils sont tous tombés ; le message « L'opération Marteau du Golan est terminée » le dit à tous. Le SA-6 de Sa'sa' est le préalable au passage des hélicoptères.", 15, 8),
    RP("Objectifs secondaires :", "le SA-11 et le PC du 1er Corps à Kiswah, pour le vol de frappe s'il y en a un.", 15, 12),
    RP("Opposition aérienne :", "pas de patrouille ennemie en vol au départ. Si personne ne tient la BARCAP, le Mission Maker peut engager une patrouille alliée de deux F-15C au-dessus de MASADA. Deux alertes au sol : des MiG-29S à Mezzeh (deux, quatre si quatre avions alliés ou plus entrent dans leur zone, autour du sud-ouest de Damas) et des MiG-23MLD à Khalkhalah (zone qui couvre Tell al-Hara). Elles sont prêtes à H+15 min et décollent dès qu'un avion allié entre dans leur zone ; elles ne réagissent pas aux hélicoptères.", 15, 12),
    RP("Défenses antiaériennes :", "le SA-11 couvre de TELLHARA à la limite de KHAN : on n'y travaille en altitude qu'après la SEAD. KHAN est juste hors du SA-6. La route des hélicoptères par le pied de l'Hermon n'est vue que sur 3,7 km par le SA-15 du front (contre 14,6 km par la trouée de Quneitra, mesuré sur le relief à 30 m sol), mais elle sort à découvert devant le SA-6 au col de Beit Jinn. Au front et en profondeur, rester hors de portée des armes à vue.", 15, 12),
    RP("Autres informations :", "le JTAC Abu Nada désigne les véhicules du front (code 1511, FM 35.55). Sous la couche, une bombe laser larguée de haut peut perdre la tache : préférer le GPS, ou la désignation par le JTAC ou un hélicoptère. Vent de face au retour. Dégagement : Haifa, Megiddo, Kiryat Shmona.", 15, 0),
])]))

# Plan de vol, étape par étape
for plan, pts, start, label in (("jets", JETS, "Ramat David", "Jets"), ("helos", HELOS, "Rosh Pina", "Hélicoptères")):
    prev = start
    for i, (name, x, y, hdg, nm, role) in enumerate(pts, start=1):
        alt = WP_M.get(name)
        S.append(Slide(f"Plan de vol {label} — W{i} {name}", [
            Img(0.4, 1.05, 8.6, 8.6 * 900 / 1300, str(MAPS / f"etape-{plan}-{i:02d}.png")),
            Text(9.2, 1.05, 3.8, 6.2, [
                Para([Run(f"W{i}", True, color=BLUE), Run(f"  {name}", True)], 24, space_after=12),
                RP("Depuis :", prev, 14, 4),
                RP("Cap :", f"{hdg:03d}°", 14, 4),
                RP("Distance :", f"{nm:g} nm", 14, 4),
                RP("Sol :", f"{round(alt * 3.281):,} ft".replace(",", " ") if alt else "—", 14, 4),
                RP("Bullseye :", be(x, y), 14, 14),
                P(role, 15, after=0),
            ]),
        ]))
        prev = name

# Déploiement et coordination
S.append(Slide("Déploiement et coordination", [Table(0.5, 1.05, [1.9, 2.0, 8.4], [
    ["Quand (estimation)", "Qui", "Quoi"],
    ["H+0", "Ninja, Arctic", "Mise en route en premier à Ramat David."],
    ["H+10", "Ninja, Arctic", "Décollage. Arctic monte en BARCAP au-dessus de MASADA, entre le front et les deux QRA, hors de portée du SA-11."],
    ["H+15", "—", "Les QRA de Mezzeh et de Khalkhalah sont prêtes : elles décollent dès qu'un avion allié entre dans leur zone."],
    ["H+15", "Archer, Jedi, Blade", "Archer et Jedi décollent et attendent à PUSH. Blade décolle de Rosh Pina et transite bas vers MASADA (environ 11 min)."],
    ["H+20 à H+35", "Ninja", "SEAD dans l'ordre : SA-15 de Khan Arnabah, SA-6 de Sa'sa', radar de Tell al-Hara. Annonce « PORTE OUVERTE » quand le SA-6 tombe."],
    ["H+25 à H+60", "Archer, Jedi", "Khan Arnabah d'abord (défense aérienne, puis blindés), puis l'artillerie de Kanaker, avec le JTAC Abu Nada."],
    ["PORTE OUVERTE", "Blade", "Passage du col de Beit Jinn, attaque de la réserve de Sa'sa' : le Kiowa repère et désigne, les Apache et le Mi-24 frappent."],
    ["Après le SA-6", "Ninja, Arctic", "Ninja traite le SA-11 ; Arctic frappe Kiswah dès que le SA-11 est tombé."],
    ["MARTEAU", "Mission Maker", "Khan Arnabah est tombé : le Mission Maker lance la poussée alliée (Khan Arnabah en une dizaine de minutes, Sa'sa' en vingt-cinq)."],
    ["ENCLUME", "Blade, Archer, Jedi", "Une colonne de contre-attaque est repérée sur la route de Sa'sa' : la casser entre COLONNE et KHAN."],
    ["Fin", "Tous", "Retour par EGRESS (jets) ou Quneitra (hélicoptères). Le tout tient en 1 h 30 à 1 h 45 de vol."],
], size=12, row_h=0.42)]))
S.append(Slide("Coordination : mots-codes et radios", [
    Table(0.5, 1.05, [2.4, 4.2, 5.7], [
        ["Mot-code (Package)", "Sens", "Qui réagit"],
        ["PORTE OUVERTE", "Le SA-6 de Sa'sa' est détruit.", "Blade franchit le col."],
        ["MARTEAU", "La ligne de Khan Arnabah est tombée.", "Le Mission Maker lance la poussée."],
        ["ENCLUME", "Une colonne de contre-attaque est en route.", "Blade, Archer et Jedi la prennent à partie."],
        ["PORTE FERMÉE", "Le SA-11 vit encore.", "Arctic ne part pas sur Kiswah."],
    ], size=13, row_h=0.45),
    Text(0.5, 3.6, 12.3, 3.7, [
        RP("Package (291.0) :", "tout le monde, pour les mots-codes et la coordination entre les vols.", 14, 6),
        RP("Magic (282.2) :", "la situation aérienne. Arctic l'écoute en permanence ; les autres, en entrée et en sortie de zone.", 14, 6),
        RP("JTAC Abu Nada (FM 35.55, code 1511) :", "Archer et Jedi pour les cibles du front. Il ne désigne que des véhicules, à moins de 10 km de Tel Abu Nada.", 14, 6),
        RP("Fat cow :", "les CH-47 du CTLD ravitaillent et réarment les hélicoptères ; le Mission Maker annonce où ils se posent.", 14, 6),
        RP("Ravitaillement en vol :", "Texaco-1 (panier, FL180) pour les F/A-18 et les Harrier, Arco-1 (perche, FL220) pour les F-16 et les A-10, au-dessus de la Galilée.", 14, 0),
    ]),
]))

# Plan de fréquences
S.append(Slide("Plan de fréquences", [
    Text(0.6, 1.1, 6.0, 6.2, [P("UHF (radio 1)", 18, True, after=10)] + [P(t, 15, after=5) for t in (
        "Package Ch. 1 : 291.000 MHz", "Archer Ch. 2 : 390.000 MHz", "Jedi Ch. 3 : 394.100 MHz", "Ninja Ch. 4 : 390.500 MHz",
        "Arctic Ch. 5 : 390.100 MHz", "Blade Ch. 6 : 390.800 MHz", "Magic Ch. 7 : 282.200 MHz", "Texaco-1 Ch. 8 : 290.100 MHz",
        "Arco-1 Ch. 9 : 290.500 MHz")]),
    Text(6.9, 1.1, 6.0, 6.2, [P("Bases (radio 2)", 18, True, after=10)] + [P(t, 15, after=5) for t in (
        "Ramat David Ch. 1 : 251.300 MHz", "Rosh Pina Ch. 2 : 251.500 MHz", "Haifa, Megiddo, Kiryat Shmona : Ch. 3 à 5 (dégagement)")] + [
        P("FM", 18, True, after=10), P("JTAC Abu Nada : 35.550 MHz", 15, after=14),
        P("Les canaux sont préréglés dans chaque appareil ; la numérotation exacte dépend des radios de l'appareil (voir la planchette des fréquences).", 12, color=GREY, italic=True)]),
]))

to_pptx(S, DOCS / "briefing.pptx")
try:
    warnings = to_pdf(S, DOCS / "briefing.pdf", PAGES)
except PermissionError:  # PDF ouvert dans un lecteur
    warnings = to_pdf(S, DOCS / "briefing-nouveau.pdf", PAGES)
    print("briefing.pdf verrouillé : écrit sous briefing-nouveau.pdf")
print(len(S), "pages")
for w in warnings:
    print("ATTENTION", w)
