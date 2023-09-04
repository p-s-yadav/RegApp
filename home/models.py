from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Documents(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   description = models.TextField()
   upload_date = models.DateTimeField(auto_created=True)
   update_date = models.DateTimeField(auto_now=True)
   file = models.FileField(upload_to='documents/')

   def delete_document(self):
        if self.file:
            if os.path.exists(self.file.path):
                os.remove(self.file.path)
        self.delete()

   def update_document(self, new_file, description):
        self.delete_document()
        self.file = new_file
        self.description = description
        self.save()
        