from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class PostContent(models.Model):
    """
    投稿内容モデル
    ユーザーの投稿したデータを管理する
    """
    def make_and_set_user(self):
        user = User.objects.get_or_create(name="deleted_user")
        return user

    post_id = models.UUIDField(default=uuid.uuid4,
                            primary_key=True, editable=False)
    user = models.ForeignKey(User,on_delete=models.SET(make_and_set_user),db_constraint=False)
    content = models.CharField(_('投稿内容'), max_length=172)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        db_table = 'post_content'
        verbose_name = _('post_content')
        verbose_name_plural = _('post_contents')

class Favorite(models.Model):
    """
    お気に入りモデル
    ユーザ－がお気に入り登録した投稿を管理する
    """
    def make_and_set_post_content(self):
        post_content = PostContent.objects.get_or_create(name="deleted_post_content")
        return post_content

    def make_and_set_user(self):
        user = User.objects.get_or_create(name="deleted_user")
        return user

    favorite_id = models.UUIDField(default=uuid.uuid4,
                            primary_key=True, editable=False)
    post_content = models.ForeignKey(PostContent,on_delete=models.SET(make_and_set_post_content),db_constraint=False)
    user = models.ForeignKey(User,on_delete=models.SET(make_and_set_user),db_constraint=False)

    class Meta:
        db_table = 'favorite'
        verbose_name = _('favorite')
        verbose_name_plural = _('favorites')
