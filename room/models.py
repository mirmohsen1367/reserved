from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from room.user_manager import CustomUserManager
from room.validator import PhoneValidator, CodeValidators


class Province(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'province'
        ordering = ('-id',)


class County(models.Model):
    name = models.CharField(max_length=20)
    province = models.ForeignKey(Province, on_delete=models.CASCADE,
                                 related_name="provinces", related_query_name='province')

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'county'
        ordering = ('-id',)


class Hotel(models.Model):
    RATING_RANGE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=50)
    phone_number = models.CharField(validators=[PhoneValidator()], max_length=17)
    county = models.ForeignKey(County, on_delete=models.CASCADE,
                               related_name='hotel_countys', related_query_name='hotel_county')
    rating = models.IntegerField(choices=RATING_RANGE)
    owner_profile = models.ForeignKey('OwnerProfile', on_delete=models.CASCADE,
                                      related_name='hotels'
                                      )

    class Meta:
        db_table = 'hotel'
        ordering = ('rating',)


class Room(models.Model):
    TYPE_ROOM = (
        ('normal', 'NORMAL'),
        ('luxury', 'LUXURY'),
        ('suite', 'SUITE'),

    )
    room_no = models.IntegerField(default=101)
    room_type = models.CharField(max_length=200, default='standard')
    no_of_beds = models.IntegerField(default=3)
    hotel = models.ForeignKey(Hotel, related_name='rooms',
                              related_query_name='room', on_delete=models.CASCADE)

    def __str__(self):
        return self.room_type

    class Meta:
        db_table = 'room'
        ordering = ('-id',)


class Cuser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, error_messages={
        'unique': _("A user with that username already exists.")})
    password = models.CharField(null=True, blank=True, default='123', max_length=128)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    full_name = models.CharField(max_length=305, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(validators=[PhoneValidator()], max_length=11)
    REQUIRED_FIELDS = ['mobile']
    objects = CustomUserManager()

    class Meta:
        ordering = ('-id',)
        db_table = 'cuser'


class CustomerProfile(models.Model):

    address = models.TextField(max_length=1000, null=True, blank=True)
    national_code = models.CharField(max_length=50, validators=[CodeValidators()], unique=True)
    postal_code = models.CharField(max_length=50, validators=[CodeValidators()], unique=True)
    user = models.OneToOneField(Cuser, related_name='customers_profiles',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-id',)
        db_table = 'customer_profile'
        verbose_name = 'customer profile'
        verbose_name_plural = 'customer profiles'


class OwnerProfile(models.Model):
    address = models.TextField(max_length=1000, null=True, blank=True)
    national_code = models.CharField(max_length=50, validators=[CodeValidators()], unique=True)
    postal_code = models.CharField(max_length=50, validators=[CodeValidators()], unique=True)
    user = models.OneToOneField(Cuser, related_name='owner_profiles',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-id',)
        db_table = 'owner_profile'
        verbose_name = 'owner profile'
        verbose_name_plural = 'owner profiles'


class Reserved(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='owner_profiles',
                                 related_query_name='owner_profile')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reserveds',
                             related_query_name='reserved')
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        db_table = 'reserved'
        ordering = ('from_date',)
