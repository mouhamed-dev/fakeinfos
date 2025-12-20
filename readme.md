# FakeInfos

## Description

FakeInfos est une application web Django conçue pour générer des identités fictives complètes et cohérentes. Utilisant l'API Google GenAI, l'application crée des données personnelles plausibles pour des fins de test, de développement ou d'illustration. Les identités générées incluent des informations telles que le nom, l'email, le téléphone, l'adresse, les documents d'identification, etc.

**Attention :** Cette application génère uniquement des données fictives. Ne l'utilisez pas pour des activités illégales ou frauduleuses.

## Fonctionnalités

- **Génération d'identités fictives :** Créez des profils complets avec des données cohérentes basées sur le pays et le genre sélectionnés.
- **Sélection personnalisée :** Choisissez le pays et le genre pour adapter les données générées.
- **Sauvegarde en base de données :** Les identités générées sont stockées avec un token unique pour un accès ultérieur.
- **Téléchargement PDF :** Exportez les identités sous forme de fiche PDF professionnelle.
- **Interface web intuitive :** Utilise Django pour une expérience utilisateur fluide.
- **IA intégrée :** Utilise Google GenAI pour assurer la cohérence et la plausibilité des données.

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Un environnement virtuel (recommandé)
- Clé API Google GenAI

### Étapes d'installation

1. **Clonez le dépôt :**

   ```bash
   git clone <url-du-depot>
   cd fakeinfos
   ```

2. **Créez et activez un environnement virtuel :**

   ```bash
   python -m venv env
   # Sur Windows :
   env\Scripts\activate
   # Sur macOS/Linux :
   source env/bin/activate
   ```

3. **Installez les dépendances :**

   ```bash
   pip install -r src/requirements.txt
   ```

4. **Configurez les variables d'environnement :**
   Créez un fichier `.env` dans le dossier `src/fake/` avec les variables suivantes :

   ```
   SECRET_KEY=votre-cle-secrete-django
   GOOGLE_GENAI_API_KEY=votre-cle-api-google-genai
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Appliquez les migrations de base de données :**

   ```bash
   cd src
   python manage.py migrate
   ```

6. **Lancez le serveur de développement :**

   ```bash
   python manage.py runserver
   ```

   L'application sera accessible à l'adresse `http://127.0.0.1:8000/`.

## Utilisation

1. Ouvrez votre navigateur et allez sur `http://127.0.0.1:8000/`.
2. Sélectionnez le pays et le genre souhaité dans le formulaire.
3. Cliquez sur "Générer" pour créer une nouvelle identité fictive.
4. Les données générées s'affichent à l'écran.
5. Utilisez le token fourni pour accéder à l'identité ultérieurement via l'URL `?ref=<token>`.
6. Cliquez sur "Télécharger PDF" pour exporter la fiche d'identité.
7. Testez le projet en ligne sur [Download.MouhaTech](download.mouhatech.com)

## Configuration

- **Base de connaissances :** L'application utilise un fichier PDF (`generateur de fake infos.pdf`) situé dans `src/fake/static/fake/images/` comme base de connaissances pour l'IA.
- **Paramètres Django :** Modifiez `src/fakeinfos/settings.py` pour ajuster les configurations selon vos besoins.
- **Modèle de données :** Le modèle `Identity` dans `src/fake/models.py` définit les champs des identités générées.

## Dépendances

Les principales dépendances sont listées dans `src/requirements.txt` :

- Django : Framework web
- django-countries : Gestion des pays
- google-genai : API Google pour la génération IA
- reportlab : Génération de PDF
- pydantic : Validation des données
- Et autres...

## Structure du projet

```
fakeinfos/
├── src/
│   ├── manage.py
│   ├── requirements.txt
│   ├── fakeinfos/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   └── fake/
│       ├── models.py
│       ├── views.py
│       ├── forms.py
│       ├── download.py
│       ├── templates/
│       ├── static/
│       └── migrations/
├── env/  # Environnement virtuel
└── readme.md
```

## Auteur

Ce projet est développé par Mouhamed Mbaye, développeur web full-stack. Voir son portfolio sur [MouhaTech](https://mouhatech.com).

## Licence

Ce projet est distribué sous licence MIT.  
Vous êtes libre de l’utiliser, le modifier et le redistribuer.  
Voir le fichier [LICENSE](Licence) pour plus de détails.
