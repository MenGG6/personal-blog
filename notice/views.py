from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from article.models import Article
# Create your views here.
#写一波高级用法————视图函数，学习学习
class Comnotview(LoginRequiredMixin, ListView):
	'''通知列表'''
	context_object_name = 'notices'
	template_name = 'notice/list.html'
	#重定向
	login_url = '/accounts/login/'
	
	def get_queryset(self):
		return self.request.user.notifications.unread()


class Comnotupdateview(View):
	'''更新通知状态'''
	#处理get
	def get(self, request):
		#获取未读消息
		notice_id = request.GET.get('notice_id')
		#获取评论的文章
		article_id = request.GET.get('article_id')
		#更新单条通知
		if notice_id:
			article = Article.objects.get(id=article_id)
			request.user.notifications.get(id=notice_id).mark_as_read()
			return redirect(article)		
		#更新全部通知
		else:
			request.user.notifications.mark_all_as_read()
			return redirect('notice:list')
