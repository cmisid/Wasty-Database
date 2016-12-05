# Wasty database service

## Installation

Il faut au préalable avoir installé Python 3. Pour cela [la distribution Anaconda](https://www.continuum.io/downloads) est recommandée. De plus il fortement conseillé d'utiliser un [environnement virtuel](http://conda.pydata.org/docs/using/envs.html).

```sh
cd /chemin/vers/application/
pip install -r setup/requirements.txt
pip install -r setup/dev-requirements.txt
```

En plus de Django, les librairies externes utilisées sont

- [django-autofixture](https://github.com/gregmuellegger/django-autofixture) pour la simulation de données factices.
- [djangorestframework](http://www.django-rest-framework.org/) pour l'API REST.


Vous pouvez lancer `python manage.py` pour afficher une liste de commandes à dispositions. Les plus fréquentes d'utilisation sont:

- `python manage.py runserver` pour lancer l'application en local
- `python manage.py makemigrations <app>` pour créer des fichiers de migration (`<app>` est par exemple `public`)
- `python manage.py migrate` pour effectuer les migrations en retard
- `python manage.py createsuperuser` pour créer un utilisateur administrateur
- `python manage.py generate_fake_data` pour remplir la base de données avec des données simulées (oui, vraiment!)
