from rest_framework import serializers
from datetime import time as datetime_time

from hr.models.leave_request import LeaveRequest


class LeaveRequestSerializer(serializers.ModelSerializer):
    total_leave_hours = serializers.ReadOnlyField()
    used_hours_this_month = serializers.ReadOnlyField()
    remaining_leave_hours = serializers.SerializerMethodField()
    rejected_by = serializers.StringRelatedField()

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'user', 'start_day', 'start_hour', 'end_day', 'end_hour',
            'description', 'status', 'created_at', 'status_updated_at',
            'total_leave_hours', 'used_hours_this_month', 'remaining_leave_hours',
            'rejected_by',
        ]
        read_only_fields = ['user', 'status', 'status_updated_at', 'created_at', 'total_leave_hours', 'used_hours_this_month']

    def get_remaining_leave_hours(self, obj):
        return obj.remaining_leave_hours()
