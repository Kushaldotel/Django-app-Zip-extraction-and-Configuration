# models.py

from django.db import models

class FileUpload(models.Model):
    zip_file = models.FileField(upload_to='uploads/')
