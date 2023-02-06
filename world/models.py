# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, UserManager

from phonenumber_field.modelfields import PhoneNumberField




class City(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=35)  # Field name made lowercase.
    countrycode = models.ForeignKey('Country', models.DO_NOTHING, db_column='CountryCode')  # Field name made lowercase.
    district = models.CharField(db_column='District', max_length=20)  # Field name made lowercase.
    population = models.IntegerField(db_column='Population')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'city'


class Country(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=3)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=52)  # Field name made lowercase.
    continent = models.CharField(db_column='Continent', max_length=13)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=26)  # Field name made lowercase.
    surfacearea = models.FloatField(db_column='SurfaceArea')  # Field name made lowercase.
    indepyear = models.SmallIntegerField(db_column='IndepYear', blank=True, null=True)  # Field name made lowercase.
    population = models.IntegerField(db_column='Population')  # Field name made lowercase.
    lifeexpectancy = models.FloatField(db_column='LifeExpectancy', blank=True, null=True)  # Field name made lowercase.
    gnp = models.FloatField(db_column='GNP', blank=True, null=True)  # Field name made lowercase.
    gnpold = models.FloatField(db_column='GNPOld', blank=True, null=True)  # Field name made lowercase.
    localname = models.CharField(db_column='LocalName', max_length=45)  # Field name made lowercase.
    governmentform = models.CharField(db_column='GovernmentForm', max_length=45)  # Field name made lowercase.
    headofstate = models.CharField(db_column='HeadOfState', max_length=60, blank=True,
                                   null=True)  # Field name made lowercase.
    capital = models.IntegerField(db_column='Capital', blank=True, null=True)  # Field name made lowercase.
    code2 = models.CharField(db_column='Code2', max_length=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'country'


class Countrylanguage(models.Model):
    countrycode = models.ForeignKey(Country, models.DO_NOTHING, db_column='CountryCode',
                                    primary_key=True)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=30)  # Field name made lowercase.
    isofficial = models.CharField(db_column='IsOfficial', max_length=1)  # Field name made lowercase.
    percentage = models.FloatField(db_column='Percentage')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'countrylanguage'
        unique_together = (('countrycode', 'language'),)

    def __unicode__(self):
        return ("country-code: %s language: %s") % (self.countrycode.name, self.language)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class MyCustomUserManager(BaseUserManager):
    def create_user(self, email_id, password, username, first_name="Null", last_name="Null", gender="FEMALE",
                    phone_number="+19001234567", user_group="MANAGER", driver_license=0, plate_number="0"):
        """
        Creates and saves a User with the given email and password.
        """
        if not email_id:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyCustomUserManager.normalize_email(email_id),
            first_name=first_name,
            last_name=last_name,
            user_name=username,
            password=password,
            gener=gender,
            phone_number=phone_number,
            user_group=user_group,
            driver_license=driver_license,
            plate_number=plate_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def update_user(self, request):
    #     body = json.loads(request.body)
    #
    #     try:
    #         user = User.objects.get(email=body.get("email", ""))
    #     except ObjectDoesNotExist:
    #         result = {"success": False, "message": "Unknown error happens! Please try again!"}
    #         return JsonResponse(result)
    #
    #     user.update(password = body.get("password", ""))
    #     user.update(username = body.get("username", ""))
    #     user.update(phone_number = body.get("phone_number", ""))
    #     user.update(gender = body.get("gender", "FEMALE"))
    #     user.update(driver_license = body.get("driver_license", ""))
    #     user.update(plate_number = body.get("plate_number", ""))
    #
    #     if body.get("is_driver", False):
    #         user.update(user_group = "DRIVER")
    #
    #     return user

    def create_superuser(self, email, password, username, user_group):
        user = self.model(
            email=MyCustomUserManager.normalize_email(email),
            username=username,
            password=password,
            user_group=user_group,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    first_name = models.CharField(max_length=64, default="Null")
    last_name = models.CharField(max_length=64, default="Null")
    username = models.CharField(max_length=64, default="Null")
    password = models.CharField(max_length=64, default="Null")
    GENDER = (
        ('Female', 'FEMALE'),
        ('Male', 'MALE'),
        ('Others', 'OTHERS'),
        ('Hope not to say', 'UNKNOWN'),
    )
    gender = models.CharField(max_length=20, choices=GENDER, default="Female")
    email = models.CharField(max_length=100, primary_key=True)
    phone_number = PhoneNumberField(default="+19001234567")
    USER_GROUP = (
        ('Passenger', 'PASSENGER'),
        ('Driver', 'DRIVER'),
        ('Manager', 'MANAGER'),
    )
    user_group = models.CharField(max_length=20, choices=USER_GROUP, default="Passenger")
    driver_license = models.IntegerField(default=0)
    plate_number = models.CharField(max_length=10, default="0")

    objects = MyCustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "username", "user_group"]
