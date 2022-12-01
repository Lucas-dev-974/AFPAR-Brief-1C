# Brief 1C - Analysis Features Preprocessing And Research
    Vous êtes un·e développeur·se chez **Analysis Features Preprocessing And Research**, 
    une ESN spécialisée dans la réalisation d’applicatifs de type BI et intelligence artificielle.

    On vous a confié la tâche de réaliser un proof of concept (PoC) dans le cadre d’un projet 
    de dashboard d’aide à la décision pour un client exigeant. 
    Vous avez accès à un fichier de données brutes, matérialisant un export depuis leurs 
    bases de données opérationnelles.

    Ce fichier CSV alimentera votre base analytique et tient lieu de situation initiale. 
    Les CSV des mois suivants vous seront régulièrement transmis.


    4 semaine sont aménager pour la réalisation de ce projet, du 21/11 au 12/12

# Architecture API retenue
    Ici un serveur API utilisant le JsonWebToken à été retenue par le membre de l'équipe.

## Api serveur prérequis
    - Mettre en place un environement virtuel (venv)
      - pip install djangorestframework
      - pip install markdown 
      - pip install django-filter

    - Créer une base de données en local pour le projet

## Lancer le serveur 
    Dans un terminal se placer dans le dossier du serveur aka 'AFPAR' puis lancer les commandes:
    - Configurer la database dans './AFPAR/AFPAR/settings.py'
    - python manage.py migrate
    - python manage.py createsuperuser (configurer le super utilisateur)
    - python manage.py runserveur

