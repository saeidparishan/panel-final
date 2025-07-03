from datetime import time as datetime_time

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import jdatetime

from accounts.models import User

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending_2', 'منتظر تایید مدیر بخش'),
        ('approved_2', 'تایید توسط مدیر بخش'),
        ('rejected_2', 'رد توسط مدیر بخش'),
        ('pending_3', 'منتظر تایید منابع انسانی'),
        ('approved_3', 'تایید توسط منابع انسانی'),
        ('rejected_3', 'رد توسط منابع انسانی'),
        ('pending_4', 'منتظر تایید مدیر کل'),
        ('approved_4', 'تایید نهایی'),
        ('rejected_4', 'رد نهایی'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    
    start_day = models.DateField(verbose_name='start_day') 
    start_hour = models.TimeField(verbose_name='start_hour', default=datetime_time(9, 30), blank=True)
    
    end_day = models.DateField(verbose_name='end_day')
    end_hour = models.TimeField(verbose_name='end_hour', default=datetime_time(17, 30), null=True, blank=True)
    
    description = models.TextField(verbose_name='description')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_2')
    created_at = models.DateTimeField(auto_now_add=True)
    status_updated_at = models.DateTimeField(null=True, blank=True)
    rejected_by = models.ForeignKey(
    User, null=True, blank=True, on_delete=models.SET_NULL, related_name='rejected_requests'
)
    MAX_MONTHLY_HOURS = 16

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'LeaveRequest'
        verbose_name_plural = 'LeaveRequests'

    def __str__(self):
        return f'درخواست مرخصی {self.user.username} - {self.start_day} تا {self.end_day}'

    @property
    def total_leave_hours(self):
        start = timezone.datetime.combine(self.start_day, self.start_hour)
        end = timezone.datetime.combine(self.end_day, self.end_hour or datetime_time(0, 0))
        duration = end - start
        return max(duration.total_seconds() / 3600, 0)

    @property
    def used_hours_this_month(self):
        now = timezone.now()
        now_jdate = jdatetime.date.fromgregorian(date=now.date())
        first_of_month = jdatetime.date(now_jdate.year, now_jdate.month, 1).togregorian()

        approved_requests = LeaveRequest.objects.filter(
            user=self.user,
            status='approved_4',
            created_at__date__gte=first_of_month
        )
        return sum([req.total_leave_hours for req in approved_requests])

    def clean(self):
        if self.start_day > self.end_day or (
            self.start_day == self.end_day and self.start_hour >= self.end_hour
        ):
            raise ValidationError("تاریخ یا ساعت شروع باید قبل از پایان باشد.")

        if self.status == 'approved_4':
            if self.used_hours_this_month + self.total_leave_hours > self.MAX_MONTHLY_HOURS:
                remain = self.MAX_MONTHLY_HOURS - self.used_hours_this_month
                raise ValidationError(f".شما فقط 16 ساعت مرخصی در ماه دارید")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not is_new:
            old = LeaveRequest.objects.get(pk=self.pk)
            if self.status != old.status:
                self.status_updated_at = timezone.now()
                # اگر رد شد، ثبت کن چه کسی رد کرده
                if self.status.startswith('rejected_'):
                    self.rejected_by = kwargs.pop('rejected_by', None)
        else:
            self.status_updated_at = timezone.now()

        self.full_clean()
        super().save(*args, **kwargs)

    def remaining_leave_hours(self):
        return max(self.MAX_MONTHLY_HOURS - self.used_hours_this_month, 0)
