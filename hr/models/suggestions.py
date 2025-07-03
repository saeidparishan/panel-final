from django.db import models
from accounts.models import User, Department

class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='suggestions')
    request = models.TextField()
    department = models.ManyToManyField(Department, related_name='suggestions')
    is_anonymous = models.BooleanField(default=False)
    

    def __str__(self):
        if self.is_anonymous:
            return "Anonymous Suggestion"
        return f"Suggestion by {self.user}"

    class Meta:
        verbose_name = "Suggestion"
        verbose_name_plural = "Suggestions"
