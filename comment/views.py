from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from article.models import Article
from .forms import CommentForm
from .models import Comment
from notifications.signals import notify
from django.contrib.auth.models import User
from django.http import JsonResponse
# Create your views here.
@login_required
def post_comment(request, article_id, parent_comment_id=None):
	article = get_object_or_404(Article, id=article_id)
	#处理POST
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.article = article
			new_comment.user = request.user
			#二级回复
			if parent_comment_id:
				parent_comment = Comment.objects.get(id=parent_comment_id)
				#若回复级数超过二级，则转换为二级
				#MPTT的get_root()方法
				new_comment.parent_id = parent_comment.get_root().id
				#被回复人
				new_comment.reply_to = parent_comment.user
				new_comment.save()
				#如果是二级评论时
				if not parent_comment.user.is_superuser:
					notify.send(
						request.user,
						recipient=parent_comment.user,
						verb='给你留言',
						target=article,
						action_object=new_comment,
					)
				#回复成功
				res = {"code": "200 OK", "new_comment_id": new_comment.id}
				return JsonResponse(res)
			new_comment.save()
			#如果是一级评论时,那评论的对象一定是管理员superuser，所以从User里筛选出管理员
			if not new_comment.user.is_superuser:
				notify.send(
					request.user,
					recipient=User.objects.filter(is_superuser=1),
					verb='给你留言',
					target=article,
					action_object=new_comment,
				)
			#添加描点
			redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
			#当给redirect函数传递一个Model对象时，会自动调用给Model对象的get_absolute_url()函数
			return redirect(redirect_url)
	#处理GET
	elif request.method == 'GET':
		comment_form = CommentForm()
		
		context = {
			'comment_form': comment_form,
			'article_id': article_id,
			'parent_comment_id': parent_comment_id
		}
		return render(request, 'comment/reply.html', context)
	else:
		pass
#评论删除
def comment_delete(request, article_id, comment_id):
	comment = Comment.objects.get(id=comment_id)
	
	comment.delete()
	return redirect('article:article_context', id=article_id)
#评论修改
def comment_edit(request, article_id, comment_id):
	#通过id值来从数据库中获取文章和评论
	article = get_object_or_404(Article, id=article_id)
	comment = get_object_or_404(Comment, id=comment_id)
	#处理post
	if request.method == 'POST':
		form = CommentForm(data=request.POST, instance=comment)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.article = article
			#当你能修改评论时，你肯定为这条评论的作者
			new_comment.user = request.user
			new_comment.save()
			return redirect('article:article_context', id=article_id)
	#处理get
	else:
		form = CommentForm(instance=comment)
		context = {
				'form': form,
				'comment': comment, 
				}
		return render(request, 'comment/edit.html', context)


