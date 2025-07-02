from rest_framework import serializers
from hr.models import Advancehr

class Advance_HR_Serializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Advancehr
        fields = '__all__'
        read_only_fields = ['user','status']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)