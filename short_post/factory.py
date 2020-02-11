import factory
import uuid
from short_post.models import PostContent
import datetime
from account.factory import UserFactory
from short_post.models import Favorite


class PostContentFactory(factory.django.DjangoModelFactory):
    """
    投稿内容モデルのテストデータ
    """
    factory.Faker._DEFAULT_LOCALE = 'ja_JP'

    class Meta:
        model = PostContent
    post_id = factory.LazyFunction(uuid.uuid4)
    content = factory.Faker('realText', length=172)
    date_joined = datetime.datetime.now()
    user = factory.SubFactory(UserFactory)


class FavoriteFactory(factory.django.DjangoModelFactory):
    """
    お気に入りモデルのテストデータ
    """
    factory.Faker._DEFAULT_LOCALE = 'ja_JP'

    class Meta:
        model = Favorite
    favorite_id = factory.LazyFunction(uuid.uuid4)
    post_content = factory.SubFactory(PostContentFactory)
    user = factory.SubFactory(UserFactory)
    date_joined = datetime.datetime.now()
