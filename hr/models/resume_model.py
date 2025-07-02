from django.db import models
from accounts.models import User

class Resume(models.Model):
    EDUCATION_CHOICES = [
        ('blow', 'زیر دیپلم'),
        ('diploma', 'دیپلم'),
        ('diploma_p', 'فوق دیپلم'),
        ('bachelor', 'لیسانس'),
        ('bachelor_p', 'فوق لیسانس'),
        ('phd', 'دکتری'),
        ('phd_p', 'فوق دکتری'),
    ]
    STATUS_CHOICES = [
        ('review', 'درحال بررسی'),
        ('reject', 'عدم تایید'),
        ('accept', 'تایید'),
    ]
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=11)
    email = models.EmailField()
    education = models.CharField(max_length=25 ,choices=EDUCATION_CHOICES,default='blow')
    study_field = models.CharField(max_length=255)
    interesting = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(blank=True,null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='review')
    checkpoint = models.BooleanField(default=False)