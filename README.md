# Marteau du Golan — VEAF_Syria_MarteauDuGolan

Mission VEAF à objectifs sur Syria, pour une soirée de 6 à 12 pilotes, environ 2 h de vol.

## Le scénario

Le 1er Corps syrien tient le Golan face à la Purple Line.
La coalition lance une attaque en profondeur : les jets (F-16C en SEAD, F/A-18C en strike puis BARCAP) aveuglent la défense sol-air et frappent le PC de Kiswah ; les hélicoptères (AH-64D, OH-58D, Mi-24P) percent par le pied de l'Hermon, appuyés par les A-10C et AV-8B en CAS.
Une fois le front dégarni, le Mission Maker lance la poussée de la brigade alliée depuis Quneitra.

| | |
|---|---|
| Date, heure | 16 avril 2024, 15h00 locale |
| Météo | Broken à 3 000 m, vent du 270 à 17 kt au sol, visibilité maximale |
| Départs | Slots dynamiques : Ramat David (jets), Rosh Pina (hélicos, 12 places) |
| Bullseye | Quneitra (vieille ville) |
| Soutien | Magic (E-3A) 282.2 ; Texaco-1 (KC-135MPRS, panier) 290.1 / 60Y FL180 ; Arco-1 (KC-135, perche) 290.5 / 64Y FL220 |
| JTAC | Abu Nada (Tel Abu Nada), code 1511, FM 35.55 (à confirmer en jeu) |

### Objectifs (opération « Marteau du Golan », active au démarrage)

| Zone | Contenu |
|---|---|
| `EWRTellHara` | Radar d'alerte 55G6 et AAA |
| `SA6Sasa` | Batterie SA-6 (radar + 4 lanceurs) |
| `SA11Kiswah` | Batterie SA-11 (radar, PC, 4 lanceurs) |
| `KhanArnabah` | Front : 2 groupes `-armor`, 3 BMP-2, AAA, SA-13, SA-15 |
| `ArtiKanaker` | 4 × 2S1, 3 × BM-21, AAA |
| `Sasa` | Réserve : 4 × T-72B3, 3 × BMP-2, `-armor`, SA-8, SA-19 |
| `Kiswah` | PC du 1er Corps : 4 statiques et AAA (après le SA-11) |

- `ContreAttaque` : colonne T-72/BMP-2/Tunguska, enchaînée 300 s après la chute de `KhanArnabah` ; elle ne compte pas dans la fin de l'opération.
- `Poussee` : groupement allié (4 Merkava, 2 M113, Avenger) dans le sous-menu F10 « Mission Maker », non complétable, protégé par la sécurité VEAF.
- QRA rouges : 2 à 4 MiG-29S à Mezzeh, 2 MiG-23MLD à Khalkhalah, en alerte à H+15 min, sans réaction aux hélicoptères.
- Côté ami, en permanence : Merkava, infanterie, M109 (tir interdit), Avenger et PC de brigade sur la ligne.

## Construire

```
.\veaf-tools.exe build VEAF_Syria_MarteauDuGolan .
```

Version de test locale (sans sécurité, logs en debug, noms lisibles) :

```
.\veaf-tools.exe build VEAF_Syria_MarteauDuGolan . --profile LOCAL_TEST
```

Les deux écrivent le même nom de `.miz` : renommer le premier avant de construire le second.
Les cartes du briefing DCS et les planchettes sont dans la recette : un build les embarque.

## Les fichiers

- `VEAF_Syria_MarteauDuGolan_20261028.miz` : la mission serveur, avec les images de briefing et le kneeboard.
- `VEAF_Syria_MarteauDuGolan_LOCAL_TEST.miz` : la version de test (sans images de briefing).
- `docs/briefing.pptx`, `docs/briefing.pdf` : le briefing VEAF (52 pages) ; `docs/maps-hd/` : les cartes en haute résolution, les vignettes des cibles et des étapes.
- `docs/recon/` : 12 photos de reconnaissance, prises dans DCS dans l'axe d'engagement de chaque cible (cap inscrit), annotées au feutre. Elles sont dans le deck et dans les planchettes.
- `docs/briefing-contenu.md` : le texte du briefing validé, et les notes pour le Mission Maker (hors briefing).
- `docs/fiche-mission-maker.md` : les commandes du Mission Maker et quoi faire selon l'effectif (CAP alliée IA, zones à désactiver, poussée).
- `mission.yaml`, `src/` : la recette (zones, QRA, ASSETS, préréglages, plans de vol, planchettes dans `src/mission/KNEEBOARD/IMAGES`).

## Régénérer le briefing

Le briefing est fait à la main, en attendant que le générateur de VMCT sache le faire (lot en cours) : les scripts sont dans `docs/build/` (Python, avec Pillow, python-pptx et requests ; les tuiles OpenTopoMap sont gardées en cache dans `docs/build/tiles/`).

```
cd docs/build
python steps.py
python kneeboard.py
python build_deck.py
```

`steps.py` rend aussi les cartes (`render_maps.py`).

Les photos de reconnaissance se refont avec DCS lancé sur `docs/build/recon/VEAF_Syria_MarteauDuGolan_RECON.miz` (ciel dégagé, 11h30), en caméra libre F11, avec le hook `dcs-fiddle` installé :

```
cd docs/build/recon
python fiddle.py "return 1"
python shoot_all.py
python process.py
```

`shoot_all.py` lit d'abord la position réelle des unités dans `live_units.txt` (relevé par `units.lua`), place la caméra au cap d'engagement de chaque cible (`shots.py`) et capture la fenêtre DCS ; `process.py` en fait des photos de reco (champ de vue calé à 80°).
Ensuite, recopier les planchettes de `docs/build/kneeboard/` dans `src/mission/KNEEBOARD/IMAGES/` et les cartes dans `src/mission/l10n/DEFAULT/briefing-*.jpg`, puis reconstruire.
Ne pas relancer l'action MCP `build_mission_briefing` : elle remplacerait les planchettes et les images par celles de l'outil.

## Limites connues

- Syria n'a pas de catalogue de terrain dégagé : aucun véhicule n'a été vérifié hors des arbres et des bâtiments. Contrôle possible : `veaf-tools dcs clear-ground-check <mission.miz>` (demande DCS).
- La prise en charge du groupement `Poussee` par GroundAI n'est pas vérifiée : à observer au premier test.
- Le verrou Mission Master de la poussée n'est pas mesuré : sans hash `password_mm_hashes`, les pilotes connus du serveur VEAF peuvent probablement la déclencher.
- La fréquence du JTAC (35.55 FM pour le code 1511) est déduite d'une mesure faite sur l'Open Training Syria : à confirmer en jeu.
- Détruire le radar de Tell al-Hara fait passer les batteries en autonome (allumées en permanence).
