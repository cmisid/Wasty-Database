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
    city_name = models.CharField(max_length=128)

    class Meta:
        db_table = 't_cities'


class District(models.Model):
    """Définition de la classe quartier, qui référence les différents
    quartiers."""
    DISTRICT_NAME = (
        ('0', 'NULL'),
        ('1', 'CAPITOLE'),
        ('2', 'SAINT-GEORGES'),
        ('3', 'JUNCASSE - ARGOULETS'),
        ('4', 'GRAMONT'),
        ('5', 'LA TERRASSE'),
        ('6', 'ZONES D\'ACTIVITES SUD'),
        ('7', 'FONTAINE-LESTANG'),
        ('8', 'PONT-DES-DEMOISELLES'),
        ('9', 'PATTE D\'OIE'),
        ('10', 'LE BUSCA'),
        ('11', 'CROIX-DE-PIERRE'),
        ('12', 'REYNERIE'),
        ('13', 'MATABIAU'),
        ('14', 'FAOURETTE'),
        ('15', 'SAINT-ETIENNE'),
        ('16', 'SAINT-SIMON'),
        ('17', 'LES IZARDS'),
        ('18', 'SAINT-MARTIN-DU-TOUCH'),
        ('19', 'LES CHALETS'),
        ('20', 'LARDENNE'),
        ('21', 'ARENES'),
        ('22', 'AMIDONNIERS'),
        ('23', 'MIRAIL-UNIVERSITE'),
        ('24', 'LES PRADETTES'),
        ('25', 'COMPANS'),
        ('26', 'GINESTOUS'),
        ('27', 'SAINT-MICHEL'),
        ('28', 'FER-A-CHEVAL'),
        ('29', 'BELLEFONTAINE'),
        ('30', 'SOUPETARD'),
        ('31', 'PAPUS'),
        ('32', 'POUVOURVILLE'),
        ('33', 'BASSO-CAMBO'),
        ('34', 'ARNAUD BERNARD'),
        ('35', 'SAINT-AUBIN - DUPUY'),
        ('36', 'JULES JULIEN'),
        ('37', 'CROIX-DAURADE'),
        ('38', 'CASSELARDIT'),
        ('39', 'MINIMES'),
        ('40', 'RAMIER'),
        ('41', 'LA CEPIERE'),
        ('42', 'EMPALOT'),
        ('43', 'LALANDE'),
        ('44', 'RANGUEIL - CHR - FACULTES'),
        ('45', 'CARMES'),
        ('46', 'LA FOURGUETTE'),
        ('47', 'BARRIERE-DE-PARIS'),
        ('48', 'MONTAUDRAN - LESPINET'),
        ('49', 'SAINT-AGNE'),
        ('50', 'PURPAN'),
        ('51', 'SAUZELONG - RANGUEIL'),
        ('52', 'SAINT-CYPRIEN'),
        ('53', 'BAGATELLE'),
        ('54', 'GUILHEMERY'),
        ('55', 'MARENGO - JOLIMONT'),
        ('56', 'COTE PAVEE'),
        ('57', 'CHATEAU-DE-L\'HERS'),
        ('58', 'ROSERAIE'),
        ('59', 'BONNEFOY'),
        ('60', 'SEPT DENIERS'),
    )

    district_name = models.CharField('name district', max_length=1,
                                     choices=DISTRICT_NAME)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    density = models.IntegerField(blank=True, null=True)
    polygon = geo.PolygonField()

    class Meta:
        db_table = 't_districts'


class Address(models.Model):
    """Définition de la classe adresse, qui référence les différentes
    adresses."""
    street_number = models.IntegerField(null=True)
    street_name = models.CharField('Street name', max_length=128)
    postal_code = models.IntegerField()
    complement = models.CharField('Complement address', max_length=128,
                                  null=True)
    address_city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    location = geo.PointField(blank=False, null=False)

    class Meta:
        db_table = 't_addresses'


class User(AbstractBaseUser, PermissionsMixin):
    """Définition de la classe points de collectes, qui référence les
    différents points de collectes."""
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    CSP = (
        ('1', 'agriculteur'),
        ('2', 'artisans, comm, Cent.'),
        ('3', 'cadres et prof. Intellectuels'),
        ('4', 'prof intermediaire'),
        ('5', 'employes'),
        ('6', 'ouvriers'),
        ('7', 'retraites'),
        ('8', 'chomage'),
        ('9', 'etudiant'),
        ('10', 'autres'),
    )

    SIZE = (
        ('1', 'petite voiture'),
        ('2', 'moyenne voiture'),
        ('3', 'grande voiture'),
    )

    date_joined = models.DateTimeField('Date joined', auto_now_add=True)
    email = models.EmailField('Email address', unique=True)
    first_name = models.CharField('First name', max_length=64, blank=True)
    user_img = models.ImageField(upload_to='users', blank=True, null=True)
    user_img_placeholder = models.ImageField(upload_to='users', blank=True,
                                             null=True)
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    last_name = models.CharField('Last name', max_length=64, blank=True)
    oauth_id = models.CharField('OAuth id', max_length=128, unique=True)
    user_permission = models.IntegerField(blank=True, null=True)
    date_unsubscribe = models.DateTimeField('Date unsubscribe',  blank=True,
                                            null=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True,
                              null=True)
    date_birth = models.DateField('Date birth', blank=True, null=True)
    social_professional_category = models.CharField(max_length=2, choices=CSP,
                                                   blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    home_address = models.ForeignKey(Address, on_delete=models.CASCADE,
                                    blank=True, null=True)
    car_size = models.CharField('car size', max_length=1, choices=SIZE, blank=True)

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
            placeholder = create_image_placeholder(self.img)
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
        ('1', 'recovery packaging'),
        ('2', 'recovery glass'),
        ('3', 'recovery textile'),
    )

    pickup_point_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    recovery_type = models.CharField('recovery type', choices=RECOVERY_TYPE,
                                     max_length=64)

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
        ('6', 'petits electromenagers'),
        ('7', 'textiles'),
        ('8', 'vaisselles'),
        ('9', 'transports'),
        ('10', 'divers'),
    )
    category_name = models.CharField('category name', max_length=1,
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
        ('14', 'table de chevet'),
        ('15', 'tabouret'),
        ('16', 'bougeoire'),
        ('17', 'cadre'),
        ('18', 'coussin'),
        ('19', 'luminaire'),
        ('20', 'miroir'),
        ('21', 'pendule'),
        ('22', 'rideau'),
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
        ('43', 'lave-linge'),
        ('44', 'poele à bois'),
        ('45', 'ventilateur'),
        ('46', 'balance'),
        ('47', 'batteur'),
        ('48', 'bouilloire'),
        ('49', 'cafetiere'),
        ('50', 'crepiere'),
        ('51', 'fer a repasser'),
        ('52', 'friteuse'),
        ('53', 'gauffrier'),
        ('54', 'grille-pain'),
        ('55', 'machine a fondue'),
        ('56', 'pese personne'),
        ('57', 'plancha'),
        ('58', 'plaque de cuisson'),
        ('59', 'raclette'),
        ('60', 'radiateur'),
        ('61', 'bonnet'),
        ('62', 'chaussure'),
        ('63', 'chemise'),
        ('64', 'couverture'),
        ('65', 'gants'),
        ('66', 'pantalon'),
        ('67', 'pull'),
        ('68', 'serviette'),
        ('69', 'short'),
        ('70', 't-shirt'),
        ('71', 'veste'),
        ('72', 'assiette'),
        ('73', 'casserole'),
        ('74', 'faitout'),
        ('75', 'plateau'),
        ('76', 'saladier'),
        ('77', 'theiere'),
        ('78', 'verre'),
        ('79', 'couvert'),
        ('80', 'roller'),
        ('81', 'skateboard'),
        ('82', 'trottinette'),
        ('83', 'velo'),
        ('84', 'baignoire'),
        ('85', 'bocal'),
        ('86', 'boite'),
        ('87', 'bouteille'),
        ('88', 'lavabo'),
        ('89', 'sac'),
        ('90', 'tonneau'),
        ('91', 'valise'),
        ('92', 'mixeur'),
        ('93', 'micro onde'),
        ('94', 'poele'),
        ('95', 'ski'),
        ('96', 'snowboard'),
    )
    sub_category_name = models.CharField('Sub-category name', max_length=1,
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


    title = models.CharField('title Advert', max_length=30)
    advert_date = models.DateTimeField('Advert date', auto_now_add=True)
    advert_state = models.CharField('Advert state', max_length=1,
                                    choices=ADVERT_STATE)
    situation = models.CharField('situation', max_length=1, choices=SITUATION)
    price = models.FloatField(blank=True, null=True)
    type_place = models.CharField('type place ', max_length=1,
                                  choices=TYPE_PLACE)
    description = models.CharField('description', max_length=64, blank=True,
                                   null=True)
    advert_img = models.ImageField(upload_to='adverts', blank=True, null=True)
    advert_img_placeholder = models.ImageField(upload_to='adverts', blank=True,
                                               null=True)
    object_state = models.CharField('stateObject', max_length=1,
                                    choices=OBJECT_STATE)
    volume = models.CharField('volume advert', max_length=1, choices=VOLUME)
    weight = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField()
    buy_place = models.CharField('buy place', max_length=1, choices=BUY_PLACE)
    advert_user = models.ForeignKey(User, on_delete=models.CASCADE)
    advert_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    constraint_time_begin = models.TimeField('time begin', blank=True, null=True)
    constraint_time_end = models.TimeField('time end', blank=True, null=True)


    def save(self, *args, **kwargs):
        """Surcharge de la méthode save, qui permettait d'enregistrer un tuple.
        Cette nouvelle méthode permet d'enregistrer l'image floutée de
        l'annonce avec une taille réduite."""
        if self.advert_img:
            placeholder = create_image_placeholder(self.img)
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
    CENTERS_OF_INTEREST = (
        ('1', 'jardin'),
        ('2', 'sport'),
        ('3', 'decoration'),
        ('4', 'mode'),
        ('5', 'bricolage'),
    )

    name_center_of_interest = models.CharField('name center of interest',
                                               max_length=1,
                                               choices=CENTERS_OF_INTEREST,
                                               blank=True, null=True)

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
