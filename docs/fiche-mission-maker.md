# Marteau du Golan — fiche Mission Maker

> Pour le Mission Maker seulement : ce n'est pas dans le briefing des pilotes.
> Menus et effets vérifiés le 28/10 sur la version de test (`VEAF_Syria_MarteauDuGolan_LOCAL_TEST.miz`), sauf mention contraire.

## Ce que la mission fait toute seule

- Au démarrage, l'opération « Marteau du Golan » est active avec quatre objectifs : le radar de Tell al-Hara, la ligne de Khan Arnabah, l'artillerie de Kanaker et la réserve de Sa'sa'.
- Le SA-6 de Sa'sa', le SA-11 et le PC de Kiswah sont actifs aussi, mais hors opération : l'opération se termine sans eux, et chacun a sa propre commande « Désactiver la zone ». Une zone qui fait partie de l'opération n'en a pas : on ne peut désactiver que l'opération entière.
- Les QRA de Mezzeh (2 à 4 MiG-29S) et de Khalkhalah (2 MiG-23MLD) sont prêtes à H+15 et ne réagissent pas aux hélicoptères.
- La chute de Khan Arnabah déclenche une colonne de contre-attaque cinq minutes plus tard, depuis Sa'sa'.

## Les commandes du Mission Maker (menu F10)

| Commande | Où | Effet |
|---|---|---|
| Lancer la poussée alliée | VEAF > ZONES DE COMBAT > Mission Maker > Lancer la poussée alliée > Activer la zone | Le groupement d'assaut (7 véhicules) apparaît devant Quneitra, rejoint la ville en tout-terrain puis prend la route de Khan Arnabah et de Sa'sa'. À lancer au mot-code « MARTEAU ». |
| CAP alliée | VEAF > MISSIONS > CAP alliée (2 F-15C, MASADA) > Good > scale 1 > Activer la mission | Deux F-15C IA (AIM-120 et AIM-9) apparaissent vers 27 000 ft puis tiennent l'hippodrome au FL250 au-dessus de MASADA, hors de portée du SA-11. VEAF propose aussi « Excellent » et « scale 2 » : seule la combinaison Good / scale 1 a été essayée (elle donne 2 F-15C). |
| Désactiver une zone | VEAF > ZONES DE COMBAT > Batterie SA-6 de Sa'sa' (ou SA-11, ou PC de Kiswah) > Désactiver la zone | Retire les unités de la zone (mesuré sur le SA-11 : 6 unités, puis 0). Utile quand personne ne fait de SEAD. |

## Selon qui est là

| Situation | Ce que fait le Mission Maker |
|---|---|
| Personne en BARCAP (pas de F/A-18 ni de F-16 disponible pour la couverture) | Appeler la CAP alliée au décollage des premiers jets, avant H+15. |
| Personne en SEAD | Désactiver le SA-6 de Sa'sa' avant que les hélicoptères quittent MASADA ; désactiver aussi le SA-11 si un vol doit aller sur Kiswah. Le dire sur la fréquence Package (« PORTE OUVERTE »). |
| Pas de vol de frappe | Rien à faire : Kiswah et le SA-11 sont secondaires, l'opération se termine sans eux. |
| Pas d'hélicoptères | Rien à faire : Archer et Jedi traitent Sa'sa' et Kanaker. La route du col reste inutilisée. |
| Moins de 6 pilotes | Appeler la CAP alliée, désactiver le SA-11, et concentrer tout le monde sur Khan Arnabah puis Sa'sa'. Lancer la poussée dès que le SA-15 et les blindés de Khan Arnabah sont tombés. |
| Beaucoup de pilotes (10-12) | Ne rien désactiver ; un second vol en BARCAP peut escorter Arctic sur Kiswah. |

## À vérifier avant la soirée

1. Que la CAP alliée engage bien un chasseur ennemi (sa tâche d'engagement est écrite, mais aucun combat n'a été observé).
2. Que la commande « Lancer la poussée alliée » demande bien le niveau Mission Master sur le serveur VEAF : la version de test a la sécurité désactivée, ce n'est pas vérifiable dessus.
3. Après une désactivation, le réseau Skynet garde quelques minutes un site fantôme dans son décompte (limitation connue, sans effet sur le combat).

Les autres notes (fréquence du JTAC, fat cow, mots-codes) sont dans `briefing-contenu.md`, section « Notes pour le Mission Maker ».
