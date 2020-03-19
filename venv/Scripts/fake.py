import os
import sys
import pathlib
import random
from datetime import timedelta


import django
import faker
from django.utils import timezone


#获取文件所在的目录路径，相当于CMD命令的“cd..”
back = os.path.dirname
#获取项目所在的根目录
BASE_DIR = back(back(os.path.abspath(__file__)))
#将项目根目录添加到python的模块搜素路径
sys.path.append(BASE_DIR)

if __name__ == '__main__':
	 #设置环境变量，并启动Django
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings')
	django.setup()
	#添加Django项目的模型
	from article.models import Article
	from comment.models import Comment
	from django.contrib.auth.models import User
	 
	 
	print('清除数据库...')
	Article.objects.all().delete() 
	Comment.objects.all().delete() 
	print('生成测试数据完成')
	fake = faker.Faker('zh_CN')
	author = User.objects.get(id=1)
	created_time = fake.date_time_between(
		start_date='-1y', 
		end_date="now",
		tzinfo=timezone.get_current_timezone()
	)
	for _ in range(20):
		article = Article.objects.create(
			author = author,
			topic = fake.sentence().rstrip('.'),
			entry = '\n\n'.join(fake.paragraphs(10)),
			created = created_time 
		)
		article.save()
	articles = Article.objects.all()
	for article in articles:
		for _ in range(3):
			comment = Comment(
				article=article,
				user=author,
				body='\n\n'.join(fake.paragraphs(1)),
				created=created_time
			)
			comment.save()
#运行代码 python -m Scripts.fake
		
	

