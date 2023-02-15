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


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    begin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    passenger = models.CharField(max_length=100)
    request_time = models.DateTimeField(auto_now=True)

    VEHICLE = (
        ('Economy', '0'),
        ('Comfort', '1'),
        ('Large', '2'),
        ('Pet', '3'),
        ('Green', '4'),
        ('Special', '5'),
    )
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE, default="Economy")
    estimate_pickup_time = models.DateTimeField()
    estimate_fee = models.CharField(max_length=100)

    driver = models.CharField(max_length=100, blank=True, null=True)
    order_taking_time = models.DateTimeField(blank=True, null=True)
    pickup_time = models.DateTimeField(blank=True, null=True)
    arrive_time = models.DateTimeField(blank=True, null=True)
    actual_fee = models.CharField(max_length=100, blank=True, null=True)

    STATUS = (
        ('Request', 'REQUEST'),
        ('Cancelled', 'CANCELLED'),
        ('Order Taking', 'TAKING'),
        ('In Progress', 'PROGRESS'),
        ('Completed', 'COMPLETED'),
    )
    status = models.CharField(max_length=20, choices=STATUS, default="Request")

    peer = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.id


class Vehicle(models.Model):
    plate_number = models.CharField(max_length=10, primary_key=True)
    VEHICLE = (
        ('Economy', '0'),
        ('Comfort', '1'),
        ('Large', '2'),
        ('Pet', '3'),
        ('Green', '4'),
        ('Special', '5'),
    )
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE, default="Economy")
    capacity = models.IntegerField(default=3, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.plate_number


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


