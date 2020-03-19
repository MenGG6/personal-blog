from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse

from .forms import Userform, Registerform, ProfileForm
from .models import Profile


# Create your views here.
def user_login(request):
    if request.method != 'POST':
        form = Userform()
    else:
        form = Userform(data=request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            # 从数据库中调取用户信息
            user = authenticate(username=user_data['username'], password=user_data['password'])
            if user:
                login(request, user)
                return redirect('article:article_list')
            else:
                message = '账号或密码输入错误，请重新输入!'
                return render(request, 'users/login.html', {'message': message})
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('article:article_list')


def user_register(request):
    if request.method != 'POST':
        form = Registerform()
    else:
        form = Registerform(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            #保存用户数据之后登陆
            login(request, new_user)
            return redirect('article:article_list')
        else:
            message = '注册内容输入有误，请重新输入！'
            return render(request, 'users/register.html', {'message': message})

    return render(request, 'users/register.html', {'form': form})

@login_required
def user_delete(request, id):
    user = User.objects.get(id=id)
    if request.user == user:
        logout(request)
        user.delete()
        return redirect('account_login')
    else:
        message = '抱歉您目前没有权限！'
        return render(request, 'user/header.html', {'message': message})


@login_required
def user_display(request, id):
    user = User.objects.get(id=id)
    # 判断profile表是否存在，如果存在就获取值，不存在就创建表
    # 此处修改BUG，应该是Profile表
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    context = {'user': user, 'profile': profile}
    return render(request, 'users/display.html', context)


@login_required
def user_edit(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)
    if request.method != 'POST':
        form = ProfileForm()
        context = {'profile': profile, 'user': user}
        #别忘了将Form传递给模板！！！
        return render(request, 'users/edit.html', context)
    else:
        if request.user != user:
            message = '对不起，您暂时没有权限！'
            return render(request, 'users/edit.html', {'message': message})
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form_cd = form.cleaned_data
            profile.style = form_cd['style']
            profile.bio = form_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = form_cd['avatar']
            profile.save()
            return redirect('users:display', id=id)
        else:
            message = '输入有误，请重新输入'
            return render(request, 'users/edit.html', {'message': message})






