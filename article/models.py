from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.
'''
null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空。
blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填
'''
# 添加文章栏目
class ArticleColumn(models.Model):
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title


class Article(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	column = models.ForeignKey(ArticleColumn, null=True, blank=True, on_delete=models.CASCADE)
	topic = models.CharField(max_length=50)
	entry = models.TextField()
	# created = models.DateTimeField(auto_now=True)此函数
	created = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	# 存储正整数的字段
	total = models.PositiveIntegerField(default=0)
	#增加图片字段，增加此字段可以为空
	avatar = models.ImageField(upload_to='article/%Y-%m-%d/', blank=True, null=True)
	
	class Meta:
		# ordering指定模型返回的排列顺序
		# -created指定模型以倒叙排列
		ordering = ('-created',)

	def __str__(self):
		return self.topic
	#获取文章地址,重定向到文章详情页

	def get_absolute_url(self):
		return reverse('article:article_context', args=[self.id])

	#保存时处理图片
	def save(self, *args, **kwargs):
		article = super(Article, self).save(*args, **kwargs)
		'''
		#固定图片缩放大小
		if self.avatar and not kwargs.get('update_fields'):
			image = Image.open(self.avatar)
			(x, y) = image.size
			new_x = 1000
			new_y = int(new_x * (y / x))
			resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
			resized_image.save(self.avatar.path)
		'''
		return article
