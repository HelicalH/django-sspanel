from django import forms
from django.contrib.auth.forms import AuthenticationForm as auth_login_form
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Announcement, Node, Shop, User


class RegisterForm(UserCreationForm):
    '''注册时渲染的表单'''

    username = forms.CharField(label='用户名', help_text='8～32个字符。可包含字母、数字和 @ . + - _ 符号。',
                               widget=forms.TextInput(
                                   attrs={'class': 'input is-info', 'placeholder': "用户名，必填。", 'maxlength': '32', 'minlength': '8'})
                               )

    email = forms.EmailField(label='邮箱', help_text='''''',
                             widget=forms.TextInput(
                                 attrs={'class': 'input is-warning', 'placeholder': "邮箱，必填。找回密码时使用。", 'maxlength': '32', 'minlength': '8'})
                             )
    invitecode = forms.CharField(label='邀请码', help_text='网站邀请码页面获取',
                                 widget=forms.TextInput(
                                     attrs={'class': 'input is-success', 'placeholder': "邀请码，必填。", 'maxlength': '24', 'minlength': '24'})
                                 )
    password1 = forms.CharField(label='密码', help_text='''8～32个字符。不能与其他个人信息太相似。不能全部为数字。''',
                                widget=forms.TextInput(
                                    attrs={'class': 'input is-primary', 'type': 'password', 'placeholder': "密码，必填。", 'maxlength': '32', 'minlength': '8'})
                                )
    password2 = forms.CharField(label='重复密码',help_text='''''',
                                widget=forms.TextInput(
                                    attrs={'class': 'input is-danger', 'type': 'password', 'placeholder': "再次输入密码，必填。", 'maxlength': '32', 'minlength': '8'})
                                )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        t = User.objects.filter(email=email)
        if len(t) != 0:
            raise forms.ValidationError('该邮箱已经注册过了')
        else:
            return email

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('invitecode','username', 'email', 'password1', 'password2', )


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': "用户名",
                'maxlength': '32',
                'minlength': '8',
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'class': 'input',
                'placeholder': "密码",
                'type': 'password',
                'maxlength': '32',
                'minlength': '8',
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()


class NodeForm(ModelForm):
    class Meta:
        model = Node
        fields = '__all__'


class ShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'


class AnnoForm(ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['balance', 'level', 'level_expire_time',]
        widgets = {
            'balance': forms.NumberInput(attrs={'class': 'input'}),
            'level': forms.NumberInput(attrs={'class': 'input'}),
            'level_expire_time': forms.DateTimeInput(attrs={'class': 'input'}),
        }

