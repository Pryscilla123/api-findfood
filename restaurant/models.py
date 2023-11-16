from django.db import models
from django.core.validators import RegexValidator
from cloudinary.models import CloudinaryField
from utils.models import BaseModel


# Create your models here.


class Restaurant(BaseModel):
    name = models.CharField(null=False, max_length=100)
    type = models.CharField(null=False, max_length=100)
    img = CloudinaryField('img')


class Address(BaseModel):
    line1 = models.CharField(null=False, max_length=255)
    line2 = models.CharField(null=False, max_length=255)
    number = models.IntegerField(null=False, unique=True)
    postal_code = models.CharField(null=False, unique=True,
                                   validators=[
                                       RegexValidator(regex='^(\\d{5}(\\-\\d{3})?)?$', message='Invalid postal code!')])
    restaurant_id = models.OneToOneField(Restaurant, on_delete=models.CASCADE, null=False,
                                         related_name='restaurant_address')


class Interval(BaseModel):
    days = (
        ('Segunda', 'Segunda-Feira'),
        ('Terca', 'Terça-Feira'),
        ('Quarta', 'Quarta-Feira'),
        ('Quinta', 'Quinta-Feira'),
        ('Sexta', 'Sexta-Feira'),
        ('Sabado', 'Sábado'),
        ('Domingo', 'Domingo')
    )

    day = models.CharField(null=False, max_length=10, choices=days)
    open = models.TimeField(null=False, auto_now=False)
    close = models.TimeField(null=False, auto_now=False)


class Schedule(BaseModel):
    interval_id = models.ForeignKey(Interval, on_delete=models.CASCADE, null=False)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False, related_name='opening_days')


class Contact(BaseModel):
    social = (
        ('insta', 'Instagram'),
        ('whats', 'Whatsapp'),
        ('face', 'Facebook'),
        ('ifood', 'Ifood'),
        ('tnl', 'Tonolucro')
    )

    type = models.CharField(null=False, choices=social, max_length=20)
    information = models.CharField(null=False, max_length=100)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False, related_name='socials')
