from rest_framework import serializers

from hr.models import Resume

class ResumeSerial(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"