# Wasty database service

## Installation

- Il faut au préalable avoir installé Python 3 (de préférence la version 3.5.2). Pour cela [la distribution Anaconda](https://www.continuum.io/downloads) est recommandée. De plus il fortement conseillé d'utiliser un [environnement virtuel](http://conda.pydata.org/docs/using/envs.html).
- Il faut aussi installer et [PostgreSQL](https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/content/optional_postgresql_installation/) et [PostGIS](https://docs.djangoproject.com/en/1.7/ref/contrib/gis/install/postgis/) qui est l'extension géographique de PostgreSQL.

```sh
cd /chemin/vers/application/
pip install -r setup/requirements.txt
pip install -r setup/dev-requirements.txt
```

Enfin il faut créer un fichier nommé `.env` pour configurer l'application selon votre installation. Ces variables sont personnelles et c'est pour cela qu'elles ne sont pas versionnées. Copiez/collez le code suivant et remplacez les valeurs selon vos besoins.

```sh
DEBUG=on # Indique si le débogueur est allumé ou pas
SECRET_KEY='3qy8$j3798ccwflqx58p9h$eb()zd83%gag)(uk^$3g@l9%cdh' # Clé secrète
DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5432/wasty # URI pointant vers la base de données
```

## Développement

Vous pouvez lancer `python manage.py` pour afficher une liste de commandes à dispositions. Les plus fréquentes d'utilisation sont:

- `python manage.py runserver` pour lancer l'application en local
- `python manage.py makemigrations <app>` pour créer des fichiers de migration (`<app>` est par exemple `public`)
- `python manage.py migrate` pour effectuer les migrations en retard
- `python manage.py createsuperuser` pour créer un utilisateur administrateur
- `python manage.py flush` pour vider la base de données

De plus, des commandes spécifiques à cette application sont disponibles:

- `python manage.py generate_fake_data` pour remplir la base de données avec des données simulées
- `python manage.py import_static_data` pour insérer les données statiques tels que les informations sur les quartiers
