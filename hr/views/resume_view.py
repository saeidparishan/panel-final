from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import HttpResponse

from hr.models import Resume
from hr.serializers import ResumeSerial

@api_view(["GET","POST"])
def Resume_View(request):
    if request.method == "GET":
        resumes = Resume.objects.all()
        serializer = ResumeSerial(resumes,many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ResumeSerial(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)