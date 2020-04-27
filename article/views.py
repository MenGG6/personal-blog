import markdown
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Article, ArticleColumn
from comment.models import Comment
from .form import ArticleForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# 引入分页模块
from django.core.paginator import Paginator
from django.db.models import Q
from comment.forms import CommentForm


# Create your views here.

def article_list(request):
	search = request.GET.get('search')
	order = request.GET.get('order')
	# 获取模板传回的column值
	column = request.GET.get('column')
	#初始化文章总数,获取指定登录用户的文章总数，避免搜索引擎交叉互联
	#articles_all = Article.objects.filter(author=request.user)
	#此处修改：博客网站可以允许非登录用户浏览，所以此处获取的应该为数据库中所有的文章总数！
	articles_all = Article.objects.all()
	# 判断是否有搜索
	if search:
		column = ''
		if order == 'total':
			article_li = articles_all.filter(Q(topic__icontains=search)|Q(entry__icontains=search)).order_by('-total')
		else:
			article_li = articles_all.filter(Q(topic__icontains=search)|Q(entry__icontains=search))
	elif column: 
        # Q对象中的icontains是不区分大小写的意思
        # 对于get和filter的获取值只能为id
		search = ''
		if order == 'total':
			article_li = articles_all.filter(column=column).order_by('-total')
		else:
			article_li = articles_all.filter(column=column)
	else:
        # 防止当用户没有操作时，把search=None传递给服务器
		column = ''
		search = ''
		if order == 'total':
			article_li = articles_all.order_by('-total')
		else:
			article_li = articles_all
	#实例化页码类，每六页为一页
	paginator = Paginator(article_li, 6)
	#在request中获取当前页面的页码
	page = request.GET.get('page')
	articles = paginator.get_page(page)
	context = {'articles': articles, 'order': order, 'search': search, 'column': column}
	return render(request, 'article/list.html', context)



def article_context(request, id):
	#article = Article.objects.get(id=id)  修改为错误404
	article = get_object_or_404(Article, id=id)
	comments = Comment.objects.filter(article=id)
	md = markdown.Markdown(
		extensions=[# 包含缩写、表格等扩展功能
		'markdown.extensions.extra',
		# 语法高亮
		'markdown.extensions.codehilite',
		#目录
		'markdown.extensions.toc',
		]
		)
	#将markdown语法的正文转换成html语法
	article.entry = md.convert(article.entry)
	article.total += 1
	article.save(update_fields=['total'])
	comment_count = comments.count
	comment_form = CommentForm()
	context = {
		'article': article, 
		'comments': comments, 
		'comment_form': comment_form, 
		'toc': md.toc,
		'comment_count': comment_count,
		}
	return render(request, 'article/context.html', context)


@login_required
def article_create(request):
    if request.method != 'POST':
        form = ArticleForm()
        columns = ArticleColumn.objects.all()
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            # 增加文章栏目的表单处理
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            return redirect('article:article_list')

    context = {'form': form, 'columns': columns }
    return render(request, 'article/create.html', context)


@login_required
def article_delete(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    return redirect('article:article_list')

@login_required
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=id)
        if request.user != article.author:
            return HttpResponse("抱歉，你无权修改这篇文章。")
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

@login_required
def article_edit(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method != 'POST':
        form = ArticleForm(instance=article)
        columns = ArticleColumn.objects.all()
    else:
        form = ArticleForm(data=request.POST, instance=article)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            # 增加文章栏目的表单处理
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            return redirect('article:article_context', id=id)
    context = {'form': form, 'article': article, 'columns': columns}
    return render(request, 'article/edit.html', context)
