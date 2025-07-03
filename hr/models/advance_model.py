from django.db import models

from accounts.models import User

class Advancehr(models.Model):
    STATUS_CHOICES = [
        ('pending_1', 'منتظر تایید مدیر بخش'),
        ('approved_1', 'تایید توسط مدیر بخش'),
        ('rejected_1', 'رد توسط مدیر بخش'),
        ('pending_2', 'منتظر تایید مدیر منابع انسانی'),
        ('approved_2', 'تایید توسط مدیر منابع انسانی'),
        ('rejected_2', 'رد توسط مدیر منابع انسانی'),
        ('pending_3', 'منتظر تایید مالی'),
        ('approved_3', 'تایید توسط مالی'),
        ('rejected_3', 'رد توسط مدیر مالی'),
        ('pending_4', 'منتظر تایید مدیر'),
        ('approved_4', 'تایید نهایی'),
        ('rejected_4', 'رد نهایی'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.CharField(max_length=20)
    status = models.CharField(max_length=35, choices=STATUS_CHOICES,default='pending_1')
    department_manager_amount = models.CharField(max_length=20, blank=True, null=True)
    human_resources_amount = models.CharField(max_length=20, blank=True, null=True)
    supervisor_amount = models.CharField(max_length=20, blank=True, null=True)
    admin_amount = models.CharField(max_length=20, blank=True, null=True)