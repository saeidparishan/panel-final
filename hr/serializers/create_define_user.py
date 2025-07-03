import random, string
from rest_framework import serializers
from accounts.models import User,Department
from hr.models import Define_User
from django.utils import timezone

class DefineUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Define_User
        fields = '__all__'

    def create(self, validated_data):
        username = validated_data.get('username')
        user_role = validated_data.get('user_role')
        department_id = validated_data.get('department')
        try:
            department_instance = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise serializers.ValidationError("دپارتمانی با این شناسه وجود ندارد.")
       
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        
        user = User.objects.create_user(
            username=username,
            password=random_password,
            role=user_role,
            department=department_instance,
            is_active=True
        )
        
        define_user = Define_User.objects.create(
            **validated_data,
            password_created_at=timezone.now()
        )

        print(f"🔑 Username: {username} - Password: {random_password}")

        return define_user