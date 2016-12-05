# Wasty database service

## Installation

## Toolchain

**Démarrage du serveur de développement**

```sh
python manage.py runserver
```

**Effectuer une migration de base de données**

Pour modifier le schéma de la base de données, il faut:

- Modifier les classes nécessaires
- Générer la migration pour les application touchées. Par exemple pour l'application `public`:
    - `python makemigrations public`
    - `python migrate`

**Création d’un utilisateur administrateur¶**

```sh
python manage.py createsuperuser
```
