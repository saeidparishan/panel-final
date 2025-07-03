from django.contrib import admin

from hr.models.leave_request import LeaveRequest
from hr.models.suggestions import Suggestion
# Register your models here.
from hr.models import *


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'start_day',
        'start_hour',
        'end_day',
        'end_hour',
        'status',
        'created_at',
        'monthly_used_hours',
        'monthly_remaining_hours',
        'rejected_by_display',
        'status_updated',
    ]
    list_filter = ['status', 'start_day', 'end_day', 'created_at', 'user__role', 'user__department']
    search_fields = ['user__username',]
    ordering = ['-created_at']

    def monthly_used_hours(self, obj):
        try:
            return f"{obj.used_hours_this_month:.1f}"
        except Exception:
            return 'خطا'
    monthly_used_hours.short_description = 'monthly_used_hours'   #'ساعت مصرف‌شده ماه'

    def monthly_remaining_hours(self, obj):
        try:
            remain = obj.MAX_MONTHLY_HOURS - obj.used_hours_this_month
            return f"{remain:.1f}"
        except Exception:
            return 'خطا'
    monthly_remaining_hours.short_description = 'monthly_remaining_hours'  # 'ساعت باقی‌مانده ماه'

    def rejected_by_display(self, obj):
        if obj.status.startswith('rejected') and hasattr(obj, 'rejected_by') and obj.rejected_by:
            return obj.rejected_by.username
        return '-'
    rejected_by_display.short_description = 'رد شده توسط'

    def status_updated(self, obj):
        return obj.status_updated_at.strftime('%Y-%m-%d %H:%M') if obj.status_updated_at else '-'
    status_updated.short_description = 'آخرین تغییر وضعیت'


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user_display', 'request', 'is_anonymous', 'get_departments']
    list_filter = ['is_anonymous', 'department']
    search_fields = ['request', 'user__username', 'user__first_name', 'user__last_name']
    filter_horizontal = ['department']
    autocomplete_fields = ['user']

    def get_user_display(self, obj):
        request = getattr(self, 'request', None)
        if request is None:
            if obj.is_anonymous or not obj.user:
                return "Anonymous"
            return str(obj.user)

        user = request.user
        allowed_roles = ['admin', 'manager']

        if user.is_superuser or (hasattr(user, 'role') and user.role in allowed_roles):
            if obj.user:
                return str(obj.user)
            return "Anonymous"

        # بقیه کاربران فقط نام ناشناس رو می‌بینند
        if obj.is_anonymous or not obj.user:
            return "Anonymous"

        return str(obj.user)

    get_user_display.short_description = 'User'

    def get_departments(self, obj):
        return ", ".join([str(dept) for dept in obj.department.all()])
    get_departments.short_description = 'Departments'

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

admin.site.register(Reports) 
admin.site.register(Advancehr)
admin.site.register(Resume)
admin.site.register(Define_User)