from autofixture import AutoFixture, generators
from django.core.management.base import BaseCommand

from public.models import Item
from public.models import Person

import datetime as dt
import random


class ItemNameGenerator(generators.Generator):
    """ Generates a random name for items """

    sample_items = [
        'Fauteuil', 'Lecteur CD', 'Adaptateur carte Compact Flash', 'Bijoux fantaisie',
        'Matelas', 'Imprimante multi fonction', 'Lavabo', 'Télécommnade télé',
        'Lave linge', 'Machine à café', 'Appareil photo numérique', 'Séche linge', 'Chevalet',
        'Veste cuir', 'Tasses et soucoupes', 'Porte serviette', 'Jeu de couverts', 'Théière',
        'TV 52cm', 'Jupe kaki', 'Tente 3 personnes', 'Chaise enfant', 'Monopoly', 'Tabourets de bar',
        'Table de chevet', 'Chaine neige', 'Evier', 'Fax', 'Frigo', 'Tire - lait',
        'Cartouches d\'encre', 'Ecran d\'ordinateur', 'Sommier', 'Bavoir', 'Caisson à roulettes',
        'Lot de "L\'automobile magazine"', 'Magazines Studio', 'Canapé clic - clac',
        'Housse de couette', 'Lot de vétement pour bb fille', 'Grille pain', 'Chaise de bureau',
        'Table basse', 'Poussette - canne', 'Dictionnaires Larousse', 'Commode',
        'Boules de sapin de Noel', 'Lot de manuels scolaire', 'Sac à main', 'Orchidées',
        'Lot de mi - bas', 'Manteau femme', 'Raquette de tenni', 'Litière', 'Manteau homme',
        'Sèche cheveux', 'Paire d\'enceintes', 'Miroir', 'Orchidées', 'Boites de rangement',
        'Ballerines', 'Petite bouilloire', 'Housses de tennis', 'Presse agrumes',
        'Buffet en meriser', 'Lot de 4 bavoirs', 'Range CD', 'Lampe architecte', 'Piano droit',
        'Sapin de Noël en plastique', 'Noix de lavage', 'Lecteur DVD', 'Livres pour enfants',
        'écouteur pour téléphone', 'Vétements enfants', 'Foulard', 'Aimants de frigo',
        'Valise à roulettes', 'Plante verte', 'Livres', 'Jeux PS2', 'Poëles', 'Micro-onde',
        'Cartons de déménagement', 'Griffoir', 'Bons de réduction', 'Balance', 'Pot de cirage',
        'Magazines', 'Chapeau', 'Gilet jaune fluo', 'Circuit de train', 'Coquillage',
        'Ours en peluche', 'Chaises', 'Paire de chaussure femme', 'Aspirateur', 'Rollers',
        'Table pliante', 'Pots de confitures', 'Plaque vitrocéramique', 'Nappe', 'Table à langer'
    ]

    def __init__(self):
        pass

    def generate(self):
        return random.choice(self.sample_items)


class Command(BaseCommand):

    help = 'Generate fake data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # 1. Persons
        AutoFixture(Person, field_values={
            'first_name': generators.FirstNameGenerator(),
            'last_name': generators.LastNameGenerator(),
            # We are a young company so just set join_date to 1-2 years
            'join_date': generators.DateGenerator(
                min_date=dt.date.today() - dt.timedelta(365 * 2),
                max_date=dt.date.today() - dt.timedelta(365 * 1)
            ),
            # Generates random birth dates between 7-77 yo
            'birth_date': generators.DateGenerator(
                min_date=dt.date.today() - dt.timedelta(365 * 77),
                max_date=dt.date.today() - dt.timedelta(365 * 7)
            )}
        ).create(10)

        # 2. Items
        AutoFixture(Item, field_values={
            'name': ItemNameGenerator(),
            'img': generators.ImageGenerator(
                width=200,
                height=200,
                path=''
            ),
            'img_url': generators.MediaFilePathGenerator(
                path=''
            )
        }
        ).create(80)
