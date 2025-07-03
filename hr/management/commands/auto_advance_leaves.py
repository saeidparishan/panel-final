from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from hr.models.leave_request import LeaveRequest


class Command(BaseCommand):
    help = 'پیش‌برد خودکار درخواست‌های مرخصی بعد از گذشت ۳ ساعت در هر مرحله تایید'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        three_hours_ago = now - timedelta(hours=3)
        

        transitions = {
            'pending_2': 'pending_3',
            # 'pending_3': 'pending_4', خودکار سازی مدیر منابع انسانی
            # 'pending_4' مرحله نهایی تایید است و نیازی به پیش‌برد خودکار ندارد
        }

        updated_count = 0

        for current_status, next_status in transitions.items():
            requests = LeaveRequest.objects.filter(
                status=current_status,
                status_updated_at__lt=three_hours_ago
            )

            for request in requests:
                request.status = next_status
                request.status_updated_at = now
                request.save()
                updated_count += 1
                self.stdout.write(f"درخواست {request.id} به {next_status} منتقل شد.")

        if updated_count == 0:
            self.stdout.write("درخواستی برای بروزرسانی وجود ندارد.")
        else:
            self.stdout.write(self.style.SUCCESS(f'{updated_count} درخواست بروزرسانی شد.'))