from django.db import models
from django.utils import timezone
# Create your models here.

class Custom(models.Model):
	name = models.CharField(max_length=6)
	phone = models.CharField(max_length=11)
	created = models.DateTimeField(default=timezone.now)
	
	class Meta:
		# ordering指定模型返回的排列顺序
		# -created指定模型以倒叙排列
		ordering = ('-created',)
	


	
	def __str__(self):
		return self.name
