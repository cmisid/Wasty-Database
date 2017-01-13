from io import BytesIO

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.gis.db import models as geo
from django.core.files.base import ContentFile
from django.core.mail import send_mail

from .managers import UserManager
from .util import create_image_placeholder


class City(models.Model):
    """Définition de la classe ville, qui référence les différentes villes."""
    city_name = models.CharField(max_length=1028)

    class Meta:
        db_table = 't_cities'


class District(models.Model):
    """Définition de la classe quartier, qui référence les différents
    quartiers."""
    district_name = models.CharField('name district', max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    density = models.IntegerField(blank=True, null=True)
    polygon = geo.PolygonField(blank=True, null=True)

    class Meta:
        db_table = 't_districts'


class Address(models.Model):
    """Définition de la classe adresse, qui référence les différentes
    adresses."""
    street_number = models.IntegerField(null=True)
    street_name = models.CharField('Street name', max_length=1028)
    postal_code = models.IntegerField()
    complement = models.CharField('Complement address', max_length=1028, blank=True,
                                  null=True)
    address_city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    location = geo.PointField(blank=True, null=True)

    class Meta:
        db_table = 't_addresses'


class User(AbstractBaseUser, PermissionsMixin):
    """Définition de la classe points de collectes, qui référence les
    différents points de collectes."""
    GENDER = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )

    CSP = (
        ('1', 'artisans, commercants, chefs entreprise'),
        ('2', 'cadres et professions intellectuelles superieures'),
        ('3', 'professions intermediaires'),
        ('4', 'employes'),
        ('5', 'ouvriers'),
        ('6', 'retraites'),
        ('7', 'chomeurs'),
        ('8', 'etudiants'),
        ('9', 'autres'),
    )

    SIZE = (
        ('1', 'petite voiture'),
        ('2', 'moyenne voiture'),
        ('3', 'grande voiture'),
    )

    date_joined = models.DateTimeField('Date joined', auto_now_add=True)
    email = models.EmailField('Email address', unique=True)
    first_name = models.CharField('First name', max_length=604, blank=True)
    user_img = models.ImageField(upload_to='users', blank=True, null=True)
    user_img_placeholder = models.ImageField(upload_to='users', blank=True,
                                             null=True)
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    last_name = models.CharField('Last name', max_length=604, blank=True)
    #oauth_id = models.CharField('OAuth id', max_length=1028, unique=True)
    oauth_id = models.CharField('OAuth id', max_length=1028, blank=True, null=True)
    user_permission = models.IntegerField(blank=True, null=True)
    date_unsubscribe = models.DateTimeField('Date unsubscribe',  blank=True,
                                            null=True)
    gender = models.CharField(max_length=100, choices=GENDER, blank=True,
                              null=True)
    date_birth = models.DateField('Date birth', blank=True, null=True)
    social_professional_category = models.CharField(max_length=500, choices=CSP,
                                                   blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    home_address = models.ForeignKey(Address, on_delete=models.CASCADE,
                                    blank=True, null=True)
    car_size = models.CharField('car size', max_length=20, choices=SIZE, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 't_users'
        verbose_name_plural = 'Users'
        ordering = ('date_joined',)

    def save(self, *args, **kwargs):
        """Surcharge de la méthode save, qui permettait d'enregistrer un tuple.
        Cette nouvelle méthode permet d'enregistrer l'image floutée de
        l'utilisateur avec une taille réduite."""
        if self.user_img:
            placeholder = create_image_placeholder(self.user_img)
            placeholder_io = BytesIO()
            placeholder.save(placeholder_io, format='JPEG')

            self.user_img_placeholder.save(
                '.'.join(str(self.img).split('/')[-1].split('.')[:-1]) +
                '_placeholder.jpg',
                content=ContentFile(placeholder_io.getvalue()), save=False
            )

        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        """Revois le prénom et le nom avec un espace au milieu."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Renvois le prénom de l'utilisateur."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Envois un email à l'utilisateur."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class PickUpPoint(models.Model):
    """Définition de la classe points de collectes, qui référence les
    différents points de collectes."""
    RECOVERY_TYPE = (
        ('1', 'emballage'),
        ('2', 'verre'),
        ('3', 'textile'),
    )

    pickup_point_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    recovery_type = models.CharField('recovery type', choices=RECOVERY_TYPE,
                                     max_length=20)

    class Meta:
        db_table = 't_pickup_Points'


class Category(models.Model):
    """Définition de la classe catégorie, qui référence les différentes
    catégories d'objets."""
    CATEGORY = (
        ('1', 'mobilier'),
        ('2', 'decos'),
        ('3', 'jardin'),
        ('4', 'materiaux'),
        ('5', 'electromenager'),
        ('6', 'petits_electromenagers'),
        ('7', 'textiles'),
        ('8', 'vaisselles'),
        ('9', 'transports'),
        ('10', 'divers'),
    )
    category_name = models.CharField('category name', max_length=20,
                                     choices=CATEGORY)

    class Meta:
        db_table = 't_categories'


class SubCategory(models.Model):
    """Définition de la classe sous-catégorie, qui référence les différentes
    sous-catégories d'objets."""
    SUB_CATEGORY = (
        ('1', 'armoire'),
        ('2', 'buffet'),
        ('3', 'canape'),
        ('4', 'chaise'),
        ('5', 'commode'),
        ('6', 'etagere'),
        ('7', 'fauteuil'),
        ('8', 'fenetre'),
        ('9', 'lit'),
        ('10', 'matelas'),
        ('11', 'porte'),
        ('12', 'pouf'),
        ('13', 'table'),
        ('14', 'table_chevet'),
        ('15', 'tabouret'),
        ('16', 'bougeoire'),
        ('17', 'cadre'),
        ('18', 'coussin'),
        ('19', 'luminaire'),
        ('20', 'miroir'),
        ('21', 'pendule'),
        ('22', 'rideaux'),
        ('23', 'tapis'),
        ('24', 'vase'),
        ('25', 'barbecue'),
        ('26', 'echelle'),
        ('27', 'hamac'),
        ('28', 'parasol'),
        ('29', 'bois'),
        ('30', 'carton'),
        ('31', 'ceramique'),
        ('32', 'metal'),
        ('33', 'papier'),
        ('34', 'plastique'),
        ('35', 'tissu'),
        ('36', 'verre'),
        ('37', 'aspirateur'),
        ('38', 'climatiseur'),
        ('39', 'congelateur'),
        ('40', 'four'),
        ('41', 'refrigerateur'),
        ('42', 'lave_vaisselle'),
        ('43', 'lave_linge'),
        ('44', 'poele_a_bois'),
        ('45', 'ventilateur'),
        ('46', 'balance'),
        ('47', 'batteur'),
        ('48', 'bouilloire'),
        ('49', 'cafetiere'),
        ('50', 'crepiere'),
        ('51', 'fer_a_repasser'),
        ('52', 'friteuse'),
        ('53', 'gauffrier'),
        ('54', 'grille_pain'),
        ('55', 'machine_a_fondue'),
        ('56', 'micro_onde'),
        ('57', 'mixeur'),
        ('58', 'pese_personne'),
        ('59', 'plancha'),
        ('60', 'plaque_de_cuisson'),
        ('61', 'raclette'),
        ('62', 'radiateur'),
        ('63', 'bonnet'),
        ('64', 'chaussure'),
        ('65', 'chemise'),
        ('66', 'couverture'),
        ('67', 'gant'),
        ('68', 'pantalon'),
        ('69', 'pull'),
        ('70', 'serviette'),
        ('71', 'short'),
        ('72', 't_shirt'),
        ('73', 'veste'),
        ('74', 'assiette'),
        ('75', 'carsserole'),
        ('76', 'couvert'),
        ('77', 'faitout'),
        ('78', 'plateau'),
        ('79', 'poele'),
        ('80', 'saladier'),
        ('81', 'theiere'),
        ('82', 'verre'),
        ('83', 'roller'),
        ('84', 'skateboard'),
        ('85', 'ski'),
        ('86', 'snowboard'),
        ('87', 'trottinette'),
        ('88', 'velo'),
        ('89', 'baignoire'),
        ('90', 'bocal'),
        ('91', 'boite'),
        ('92', 'bouteille'),
        ('93', 'lavabo'),
        ('94', 'sac'),
        ('95', 'tonneau'),
        ('96', 'valise'),
    )
    sub_category_name = models.CharField('Sub-category name', max_length=20,
                                         choices=SUB_CATEGORY)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 't_sub_categories'


class Advert(models.Model):
    """Définition de la classe annonces, qui référence les différentes
    annonces."""
    VOLUME = (
       ('1', 'peu encombrant'),
       ('2', 'encombrant'),
       ('3', 'tres encombrant'),
    )
    OBJECT_STATE = (
       ('1', 'mauvais etat'),
       ('2', 'etat moyen'),
       ('3', 'bon etat'),
    )

    TYPE_PLACE = (
        ('1', 'chez un particulier'),
        ('2', 'dans la rue'),
        ('3', 'dans un point de collecte'),
    )

    ADVERT_STATE = (
        ('1', 'en ligne'),
        ('2', 'expire'),
        ('3', 'recupere'),
        ('4', 'valide'),
        ('5', 'supprimer'),
    )

    SITUATION = (
        ('1', 'a vendre'),
        ('2', 'a donner'),
        ('3', 'a debarrasser'),
    )

    BUY_PLACE = (
        ('1', 'grande distribution'),
        ('2', 'artisan'),
        ('3', 'magasin specialise'),
        ('4', 'indefini'),
    )


    title = models.CharField('title Advert', max_length=300)
    advert_date = models.DateTimeField('Advert date', auto_now_add=True)
    advert_state = models.CharField('Advert state', max_length=10,
                                    choices=ADVERT_STATE)
    situation = models.CharField('situation', max_length=20, choices=SITUATION)
    price = models.FloatField(blank=True, null=True)
    type_place = models.CharField('type place ', max_length=20,
                                  choices=TYPE_PLACE)
    description = models.CharField('description', max_length=1028, blank=True,
                                   null=True)
    advert_img = models.ImageField(upload_to='adverts', blank=True, null=True)
    advert_img_placeholder = models.ImageField(upload_to='adverts', blank=True,
                                               null=True)
    object_state = models.CharField('stateObject', max_length=20,
                                    choices=OBJECT_STATE)
    volume = models.CharField('volume advert', max_length=20, choices=VOLUME)
    weight = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField()
    buy_place = models.CharField('buy place', max_length=20, choices=BUY_PLACE)
    advert_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    advert_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    constraint_time_begin = models.TimeField('time begin', blank=True, null=True)
    constraint_time_end = models.TimeField('time end', blank=True, null=True)


    def save(self, *args, **kwargs):
        """Surcharge de la méthode save, qui permettait d'enregistrer un tuple.
        Cette nouvelle méthode permet d'enregistrer l'image floutée de
        l'annonce avec une taille réduite."""
        if self.advert_img:
            placeholder = create_image_placeholder(self.advert_img)
            placeholder_io = BytesIO()
            placeholder.save(placeholder_io, format='JPEG')
            self.advert_img_placeholder.save(
                '.'.join(str(self.img).split('/')[-1].split('.')[:-1]) +
                '_placeholder.jpg',
                content=ContentFile(placeholder_io.getvalue()), save=False
            )

        super(Advert, self).save(*args, **kwargs)

    class Meta:
        db_table = 't_adverts'
        ordering = ('advert_date',)


class Recovery(models.Model):
    """Définition de la classe récupération, qui référence chaque
    récupérations."""
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    recovery_datetime = models.DateTimeField('recovery date ')
    recovery_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 't_recoveries'
        ordering = ('recovery_datetime',)


class Like(models.Model):
    """Définition de la classe favoris, qui référence les annonces likées."""
    advert_like = models.ForeignKey(Advert, on_delete=models.CASCADE)
    user_like = models.ForeignKey(User, on_delete=models.CASCADE)
    like_datetime = models.DateTimeField('When', auto_now_add=True)

    class Meta:
        db_table = 't_likes'


class Visit(models.Model):
    """Définition de la classe visite, qui référence l'historique des annonces
    visitées."""
    advert_visit = models.ForeignKey(Advert, on_delete=models.CASCADE)
    user_visit = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_datetime = models.DateTimeField('When', auto_now_add=True)

    class Meta:
        db_table = 't_visits'


class CenterOfInterest(models.Model):
    """Définition de la classe centres d'intérêts, qui recense les différents
    centres d'intérêts."""
    name_center_of_interest = models.CharField('name center of interest', max_length=200, blank=True, null=True)

    class Meta:
        db_table = 't_centers_of_interest'


class InterestFor(models.Model):
    """Définition de la classe intérêts pour, qui référence les intérêts des
    utilisateurs."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    center_of_interest = models.ForeignKey(CenterOfInterest,
                                           on_delete=models.CASCADE)

    class Meta:
        db_table = 't_interest_for'