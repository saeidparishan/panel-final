from django.db import models

from accounts.models import Department
from accounts.models import User

def upload_to_phone_number(instance, filename):
    phone = instance.phone_number or 'unknown'
    return f'user_uploads/{phone}/{filename}'

class Define_User(models.Model):
    DEPARTMENT_CHOICES = (
        (1, 'مدیر سیستم'),
        (2, 'مدیریت'),
        (3, 'سایت'),
        (4, 'آی تی'),
        (5, 'منابع انسانی'),
        (6, 'مالی'),
        (7, 'پشتیبانی'),
        (8, 'فروش'),
        (9, 'اداری'),
        (10, 'حضوری'),
        (11, 'محتوا'),
    )
    ROLE_CHOICES = (
        ('admin', 'مدیر سیستم'),
        ('manager', 'مدیریت'),
        ('human_resources', 'مدیر منابع انسانی'),
        ('department_manager', 'مدیر بخش'),
        ('supervisor', 'سرپرست'),
        ('employee', 'کارمند'),
    )
    interviewer = models.CharField(max_length=100)
    interview_date = models.DateField(blank=True,null=True)
    start_day = models.DateField(blank=True,null=True)
    detail_identity = models.ImageField(upload_to=upload_to_phone_number,blank=True,null=True)
    phone_number = models.CharField(max_length=11)
    id_card = models.CharField(max_length=10,blank=True,null=True)
    father_name = models.CharField(max_length=50,blank=True,null=True)
    couple = models.BooleanField(default=False)
    baby_count = models.CharField(max_length=50,blank=True,null=True)
    username = models.CharField(max_length=50)
    password_created_at = models.DateTimeField(auto_now_add= True)
    password_changed = models.BooleanField(default=False)
    user_role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='employee')
    department = models.CharField(max_length=35, choices=DEPARTMENT_CHOICES)
    checkpoint = models.BooleanField(default=False)
    #