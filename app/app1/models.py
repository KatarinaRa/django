from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from enum import Enum

class Uloga(Enum):
    ADMIN = 'ADMIN'
    PROFESOR =  'PROFESOR'
    STUDENT  = 'STUDENT'

    

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('uloga', 'ADMIN') 
        return self.create_user(username, password, **extra_fields)
        
class Korisnici(AbstractUser):
    STATUS_CHOICES = [
        ('NONE', 'none'),
        ('REDOVNI', 'redovni'),
        ('IZVANREDNI', 'izvanredni'),
    ]
    ULOGA_CHOICES= [
        ('ADMIN', 'admin'),
        ('PROFESOR', 'profesor'),
        ('STUDENT', 'student'),
    ]

    status = models.CharField(choices=STATUS_CHOICES, max_length=50)
    uloga = models.CharField(choices=ULOGA_CHOICES, max_length=50)
    objects = UserManager()
    def __str__(self):
         return '%s %s' % (self.first_name,self.last_name)

class Predmeti(models.Model):
    ime =  models.CharField(max_length=30)
    kod =  models.CharField(max_length=30)
    program =  models.CharField(max_length=30)
    bodovi = models.IntegerField()
    sem_redovni = models.IntegerField()
    sem_izvanredni = models.IntegerField()
    DA = 'DA'
    NE = 'NE'
    IZBORNI_CHOICES = [
        ('DA', 'da'),
        ('NE', 'ne'),
    ]
    izborni = models.CharField(choices=IZBORNI_CHOICES,default=NE, max_length=50)
    nositelj = models.ForeignKey(Korisnici, on_delete=models.CASCADE)
    def __str__(self):
        return '%s' % (self.ime)

class Upisi(models.Model):
    korisnici = models.ForeignKey(Korisnici, on_delete=models.CASCADE)
    predmeti = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    UPISAN = 'UPISAN'
    POLOZEN = 'POLOZEN'
    DOBIO_POTPIS = 'DOBIO_POTPIS'
    IZGUBIO_POTPIS = 'IZGUBIO_POTPIS'
    STATUS_CHOICES = [
        ('UPISAN', 'upisan'),
        ('POLOZEN', 'polozen'),
        ('DOBIO_POTPIS', 'dobio_potpis'),
        ('IZGUBIO_POTPIS', 'izgubio_potpis'),
    ]

    status = models.CharField(choices=STATUS_CHOICES, default=UPISAN,max_length=50)
    def __str__(self):
        return '%s, %s, %s' % (self.korisnici, self.predmeti, self.status)