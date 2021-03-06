from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱', widget=forms.TextInput(attrs=
    {'class':'form-control', 'placeholder':"请输入用户名或邮箱"}))
    
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs=
    {'class':'form-control', 'placeholder':"请输入密码"}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('密码不正确')
        else: # 输入的是用户名 
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=30, min_length=3, 
    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"请输入用户名(3~30个字符)"}))
    
    password = forms.CharField(label='密码', max_length=15, min_length=6, widget=forms.PasswordInput(attrs=
    {'class':'form-control', 'placeholder':"请输入密码(6~15个字符)"}))

    password_again = forms.CharField(label='确认密码', max_length=15, min_length=6, widget=forms.PasswordInput(attrs=
    {'class':'form-control', 'placeholder':"再次输入密码"}))

    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(
                                attrs={'class':'form-control', 'placeholder':"请输入邮箱地址"}))

    verification_code = forms.CharField(
        label='验证码', required=False, max_length=30, widget=forms.TextInput(attrs=
        {'class':'form-control', 'placeholder':"点击“发送验证码”发送到邮箱"})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)


    def clean(self):
        # 判断验证码是否正确
        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if not (code != "" and verification_code == code):
            raise forms.ValidationError('验证码错误')
        
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在！')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱地址已存在！')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致！')
        return password_again

    def clean_verification_code(self):
        # 判断验证码是否为空
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if verification_code == "":
            raise forms.ValidationError("验证码不能为空！")
        return verification_code


class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label='新的昵称', max_length=30, widget=forms.TextInput(attrs=
    {'class':'form-control', 'placeholder':"请输入新的昵称"}))


    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)


    def clean(self):  # 前端页面不可信原则
        # 判断用户是否登录
        if not self.user.is_authenticated:
            raise forms.ValidationError('用户尚未登录！')
        else:
            self.cleaned_data['user'] = self.user
            return self.cleaned_data


    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new','').strip()
        if nickname_new == '':
            raise forms.ValidationError('昵称不能为空！')
        return nickname_new


class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱', widget=forms.EmailInput(attrs=
        {'class':'form-control', 'placeholder':"请输入一个有效的邮箱地址"})
    )
    verification_code = forms.CharField(
        label='验证码', required=False, max_length=30, widget=forms.TextInput(attrs=
        {'class':'form-control', 'placeholder':"点击“发送验证码”发送到邮箱"})
    )


    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)


    def clean(self):  # 前端页面不可信原则
        # 判断用户是否登录
        if not self.request.user.is_authenticated:
            raise forms.ValidationError('用户尚未登录！')
        else:
            self.cleaned_data['user'] = self.request.user
        
        # 判断验证码是否为空
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if verification_code == "":
            raise forms.ValidationError("验证码不能为空！")

        # 判断用户是否已经绑定邮箱
        if self.request.user.email != "":
            raise forms.ValidationError('你已经绑定邮箱！')

        # 判断邮箱是否已经被绑定
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定 请更换邮箱')

        # 判断验证码是否正确
        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if not (code != "" and verification_code == code):
            raise forms.ValidationError('验证码错误')

        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧的密码', widget=forms.PasswordInput(attrs=
    {'class':'form-control', 'placeholder':"请输入旧的密码"}))

    new_password = forms.CharField(label='新的密码',  max_length=15, widget=forms.PasswordInput(attrs=
    {'class':'form-control', 'placeholder':"请输入新的密码"}))

    new_password_again = forms.CharField(label='再次输入新的密码', widget=forms.PasswordInput(attrs=
    {'class':'form-control', 'placeholder':"再次输入新的密码以确认"}))
    
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)


    def clean(self):
        # 验证新的密码是否一致
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        return self.cleaned_data


    def clean_old_password(self):
        # 验证旧的密码是否正确
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码错误')
        return old_password


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱', widget=forms.EmailInput(attrs=
        {'class':'form-control', 'placeholder':"请输入一个有效的已绑定邮箱地址"})
    )
    
    new_password = forms.CharField(label='新的密码',  max_length=15, widget=forms.PasswordInput(attrs=
    {'class':'form-control', 'placeholder':"请输入新的密码"}))

    verification_code = forms.CharField(
        label='验证码', required=False, max_length=30, widget=forms.TextInput(attrs=
        {'class':'form-control', 'placeholder':"点击“发送验证码”发送到邮箱"})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)


    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱未绑定账户')
        return email


    def clean_verification_code(self):
        # 判断验证码是否为空
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if verification_code == "":
            raise forms.ValidationError("验证码不能为空！")

        # 判断验证码是否正确
        code = self.request.session.get('forgot_password_code', '')
        if not (code != "" and verification_code == code):
            raise forms.ValidationError('验证码错误')

        return verification_code
