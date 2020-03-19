from django import forms
from django.contrib.auth.models import User
from .models import Profile


class Userform(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class Registerform(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        # 别写错Meta中的预定义参数名，model 和 fields
        model = User
        fields = ('username', 'email')

    # 对两次输入密码进行判断，此clean_[字段]形式的函数，Django会自动调用！！
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致，请重新输入！')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('style', 'avatar', 'bio')