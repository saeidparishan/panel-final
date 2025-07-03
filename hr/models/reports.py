from django.db import models
from accounts.models import User

class Reports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    # check = models.BooleanField(default=False)