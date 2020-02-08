import factory
import uuid
from short_post.models import PostContent
import datetime
from account.factory import UserFactory


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
