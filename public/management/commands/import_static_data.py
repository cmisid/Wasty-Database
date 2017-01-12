import json

from django.core.management.base import BaseCommand

from public.models import City, District


class Command(BaseCommand):

    help = 'Import bootstrap data'

    def add_arguments(self, parser):
        pass

    def import_districts(self):
        data = json.loads((open('bootstrap_data/toulouse_census_2011.geojson').read()))

        for feature in data['features']:

            """ Extrait les coordonnees dans un format connu. """
            coords = feature['geometry']['coordinates'][0]
            wkt = 'POLYGON (({}))'.format(', '.join((
                '{} {}'.format(coord[0], coord[1])
                for coord in coords
            )))

            """ Insère la ville si elle n'existe pas. """
            city_name = feature['properties']['libcom']
            if not City.objects.filter(name=city_name).exists():
                city = City(name=city_name).save()
            else:
                city = City.objects.get(name=city_name)

            """ Insère un quartier si il n'exite pas. """
            district_name = feature['properties']['libgq']
            if not District.objects.filter(name=district_name).exists():
                District(name=district_name, poly=wkt, city=city).save()

    def handle(self, *args, **options):
        self.import_districts()
