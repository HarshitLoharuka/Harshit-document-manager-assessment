from django.db import models
from propylon_document_manager.users.models import User

class FileVersion(models.Model):
    file_name = models.CharField(max_length=512)
    version_number = models.IntegerField()
    file_url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
