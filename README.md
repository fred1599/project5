Cahier des charges
==================


Description du parcours utilisateur
L'utilisateur est sur le terminal. Ce dernier lui affiche les choix suivants :

1. Quel aliment souhaitez-vous remplacer ? 
2. Retrouver mes aliments substitués.

L'utilisateur sélectionne 1. Le programme pose les questions suivantes à l'utilisateur et ce dernier sélectionne les réponses :

* Sélectionnez la catégorie. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant et appuie sur entrée]
* Sélectionnez l'aliment. [Plusieurs propositions associées à un chiffre. L'utilisateur entre le chiffre correspondant à l'aliment choisi et appuie sur entrée]
* Le programme propose un substitut, sa description, un magasin ou l'acheter (le cas échéant) et un lien vers la page d'Open Food Facts concernant cet aliment.
* L'utilisateur a alors la possibilité d'enregistrer le résultat dans la base de données.
 

Fonctionnalités
---------------

Recherche d'aliments dans la base Open Food Facts.
L'utilisateur interagit avec le programme dans le terminal.
Si l'utilisateur entre un caractère qui n'est pas un chiffre, le programme répète la question,
La recherche s'effectue sur une base MySql.

Installation
------------

pip install -r requirements.txt
