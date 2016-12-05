from autofixture import AutoFixture
from django.core.management.base import BaseCommand

from public.models import Item
from public.models import Person


class Command(BaseCommand):

    help = 'Generate fake data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # 1. Persons
        AutoFixture(Person).create(10)
        # 2. Items
        AutoFixture(Item).create(80)
