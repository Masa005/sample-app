from django import forms
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms

User = get_user_model()

class LoginForm(auth_forms.AuthenticationForm):
    """
    ログインフォーム
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

    error_messages = {
        'invalid_login': (
            'ユーザー名、またはパスワードが間違っています'
        )
    }

class CreateUserForm(UserCreationForm):
    """
    ユーザー登録フォーム
    """
    class Meta:
        model = User
        fields = ('username','name', 'birthday','email')

    def __init__(self,*args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control'
            ,'placeholder': 'ユーザー名を半角英数字で入力してください'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control'
            ,'placeholder': '半角英数字8文字以上で入力してください'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control'
            ,'placeholder': '半角英数字8文字以上で入力してください'})
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control'
            ,'placeholder': '例）tarou@gmail.com'})
        self.fields['name'].widget = forms.TextInput(attrs={
            'class': 'form-control'
            ,'placeholder': 'アプリ内に表示する名前を入力してください'})
        self.fields["birthday"].widget = forms.SelectDateWidget(attrs={
            'class': 'form-control'
            ,'style': 'width: auto; display: inline-block;'}
            ,years = self.create_year_choice()
            ,empty_label=("年", "月", "日"))

    def create_year_choice(self):
        """
        「年」セレクトボックス項目生成
        """
        this_yaer = datetime.datetime.now().year
        year_choice = [ i for i in range(1900,this_yaer + 1) ]
        return year_choice

    def clean_email(self):
        """
        同じメールアドレスで仮登録段階のアカウントを消去
        """
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email