from rest_framework import generics
from hr.models import Define_User
from hr.serializers import DefineUserSerializer

class DefineUserCreateView(generics.CreateAPIView):
    queryset = Define_User.objects.all()
    serializer_class = DefineUserSerializer