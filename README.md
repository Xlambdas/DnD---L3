
# Avanccé du travail

## fait sur la premiere semaine

- création de la base de donnée et des fonctions de récupération.
- création des classes Race, Classe et player
- début d'interface player (pour le moment non fonctionnelle suite a des modifications - ajout de race et classe)..

## Fait sur la deuxieme semaine

# DnD---L3

game for the final project on informatics L3.

Cute game with all the things an dungeon and dragon need !!

Rules :

Le jeu de role Donjons et Dragons (TSR, puis Wizard of The Coast) est un des grand standar du jeu de rôle. Les règles 3.5 s'appuie sur le D20 System (Wikipedia) dont on peut trouver les règles détaillées sur D20Sytem.

Ce jeu de rôle a donné lieu à divers jeux vidéos implémentant ces règles, comme Baldur's Gate 1 et 2 (règles ADD2), Neverwinter Nights (règles DD 3.5) ou Baldur's Gate 3 (règles DD 5)

L'objectif du projet est d'implémenter les classes et races de personnages, puis de gérer un combat simplifié entre deux groupes de personnages sur une grille de jeux.

Comme pour les autres projets, l'accent sera mis sur une bonne définition des classes pour avoir un moteur de jeu fonctionnel. Il est conseillé d'utiliser le mécanisme d'héritage pour modéliser les classes et les races des personnages.

Une interface texte ou graphique sera ajoutée par la suite. ...

## Autre
--- | others things | ---

lien avec toute la documentation : [docu DnD](https://regles-donjons-dragons.com/page2.html)

Def  - D20 systeme :

- Jet de D20 : Les actions sont généralement résolues en lançant un D20, en y ajoutant des modificateurs (compétence, caractéristique, bonus divers) et en comparant le résultat à une Classe de Difficulté (CD) ou un jet opposé.
- Caractéristiques : Un personnage possède des attributs de base (ex. : Force, Dextérité, Intelligence) qui influencent ses capacités et ses jets de dés.
- Bonus et modificateurs : Les scores de caractéristiques, compétences, dons et équipements donnent des bonus ou malus aux jets de D20.
- Classes et niveaux : Les personnages appartiennent à une/des classes (guerrier, mage, voleur, etc.) et gagnent des niveaux qui améliorent leurs capacités.

Points de vie (PV) et points de mana (PM) : Les personnages ont des PV qui déterminent leur survie et parfois des PM pour la magie.

Combat au tour par tour : Lors d’un affrontement, chaque personnage agit selon une initiative, effectue une attaque (jet d’attaque + modificateur) et inflige des dégâts (jet de dés basé sur l'arme ou la capacité).

Jets de sauvegarde : Lorsqu’un personnage doit résister à une menace (poison, magie, piège), il effectue un jet de sauvegarde basé sur une caractéristique.

Alignement : Un personnage possède une éthique (ex. : Loyal Bon, Chaotique Mauvais) qui influence son rôle et ses décisions.

Évolution du personnage : L’expérience gagnée permet de monter en niveau et d’améliorer les compétences, capacités et caractéristiques.

## Questions pour le prof

comment faire un choix avec deux listes (classes et races) ?

...

## Liste des choses a faire

<!-- Todo -->

Urgent :

- page Création de personnage avec choix de classe parmis une liste.

Autre / objectifs :

- personnage
  - create perso
  - save to database
  - UPDATE : if he already exist : return (waw man, the gamer already exist, find another name nigger)
  - UPDATE :
    - id unique généré par joueur
    - delete player
- Jet de dé
- Caractéristique (force, dextérité, constitution, intelligence, sagesse, charisme)
- Bonus / malus
- classes / niveau
- combat au tour par tour
- sauvegarde
- evolution du personnage

...

fichier a jour :

- utils
- player_creation
- main (bientot)

a faire :

- player
- classe
- race
- main
