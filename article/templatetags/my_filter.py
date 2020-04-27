from django import template
from django.utils import timezone
#注册过滤器
register = template.Library()

@register.filter(name="trans_time")
def trans_time_func(value):
	now = timezone.now()
	time = now - value
	#一分钟之内的显示刚刚
	if time.days == 0 and time.seconds < 60:
		return "刚刚"
	#X分钟前发送
	elif time.days == 0 and time.seconds < 3600:
		return  str(int(time.seconds/60))+"分钟前"
	#X小时前发送
	elif time.days == 0 :
		return  str(int(time.seconds/3600))+"小时前"
	#X天前发送
	elif time.days >=1 and time.days < 32:
		return str(time.days)+"天前"
	#X月前发送
	elif time.days >=32 and time.days < 365:
		return str(int(time.days/30))+"月前"
	#X年前发送
	elif time.days >=365:
		return str(int(time.days/365))+"年前"
	else:
		return "来自未来(手动狗头)"
	
@register.filter(name="trans_watched")
def trans_watched_func(value):
	if value <= 20:
		return "热度低温"
	elif value <=100:
		return "热度中温"
	elif value <=1000:
		return "热度高温"
	else:
		return "热度超高温"
