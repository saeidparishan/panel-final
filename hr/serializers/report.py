from rest_framework import serializers
from hr.models import Reports

class ReportSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reports
        fields = ['id','description','user']