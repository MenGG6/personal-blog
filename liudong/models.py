from django.db import models
from django.utils import timezone
# Create your models here.

class Custom(models.Model):
	name = models.CharField(max_length=6)
	phone = models.CharField(max_length=11)
	


	
	def __str__(self):
		return self.name
