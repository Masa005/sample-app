from django.forms import ModelForm
from short_post.models import PostContent
from django import forms
from short_post.models import Follow


class PostForm(ModelForm):
    """
    投稿フォーム
    """
    class Meta:
        model = PostContent
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={
            'class': 'form-control rows="5"',
            'placeholder': '投稿内容を入力'})
        self.fields['content'].error_messages = {'max_length': '投稿内容は172 文字'
                                                 '以下で入力してください'}


class FollowForm(ModelForm):
    """
    フォローフォーム
    """
    class Meta:
        model = Follow
        fields = ('followed_user',)
