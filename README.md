![LITRevu banner](assets/LIT_revu_banner.png)

## 1. Fonctionnalités

L’application **LITRevu** permet de :

- Créer un billet pour demander des critiques de livres ou d’articles ;
- Lire et découvrir les critiques partagées par d'autres utilisateurs ;
- Publier vos propres critiques de livres ou d’articles et contribuer à la communauté.

## 2. Initialisation du projet

1. Récupération du projet :

```bash
$ git clone https://github.com/Cyrilebl/p9-LIT_Revu.git
```

2. Création et activation de l'environnement virtuel :

- ### Windows :

```bash
$ cd p9-LIT_Revu
$ python -m venv env
$ ~env\Scripts\activate
```

- ### MacOS/Linux :

```bash
$ cd p9-LIT_Revu
$ python3 -m venv env
$ source env/bin/activate
```

3. Installation des dépendances :

```bash
$ pip install -r requirements.txt
```

4. Lancement du serveur :

```bash
$ python manage.py runserver
```

> **Remarque** : Sur certains systèmes (notamment Linux/MacOS), la commande `python` peut ne pas fonctionner.Utilisez `python3` à la place.

5. Lien vers l'application :

Accédez à l'application via votre navigateur à l'adresse suivante :  
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 3. Se connecter

Vous pouvez créer votre propre compte dans l'application ou utiliser l'utilisateur par défaut :

- **Nom d'utilisateur** : `johndoe`
- **Mot de passe** : `JohnDoe1`
