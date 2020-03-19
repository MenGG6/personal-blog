from django.db import models
from article.models import Article
from users.models import User
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.
class Comment(MPTTModel):
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	body = RichTextField()
	created = models.DateTimeField(auto_now_add=True)
	#mptt树形结构
	parent = TreeForeignKey(
		'self',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name='children',
	)
	#记录二级评论回复
	reply_to = models.ForeignKey(
		User,
		null=True,
		blank=True,
		on_delete=models.CASCADE,
		related_name='replyers',
	)
	class MPTTMeta:
		order_insertion_by = ['created']

	def __str__(self):
		return self.body[:20]
