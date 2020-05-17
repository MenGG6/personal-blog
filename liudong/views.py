from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Custom
from .forms import CustomForm
from article.models import Article
# Create your views here.

def liudong_note(request):
	articles = Article.objects.all()
	article_arys = []
	
	for article in articles:
		article_arys.append(article)
	article_1 = article_arys[0]
	article_2 = article_arys[1]
	article_3 = article_arys[2]
	article_4 = article_arys[3]
	article_5 = article_arys[4]
	article_6 = article_arys[5]

	if request.method != 'POST':
		form = CustomForm()
	else:
		form = CustomForm(data=request.POST)
		if form.is_valid():
			new_form = form.save()
			new_form.save()
			return HttpResponse('保存成功！')
	context = {'form': form, 'article_1': article_1,  
			'article_2': article_2, 'article_3': article_3, 
			'article_4': article_4, 
			'article_5': article_5, 'article_6': article_6}
	return render(request, 'liudong/liudong_note.html', context)
