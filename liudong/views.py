from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Custom
from .forms import CustomForm
# Create your views here.

def liudong_note(request):
	if request.method != 'POST':
		form = CustomForm()
	else:
		form = CustomForm(data=request.POST)
		if form.is_valid():
			new_form = form.save()
			new_form.save()
			return HttpResponse('保存成功！')
	context = {'form': form}
	return render(request, 'liudong/liudong_note.html', context)
