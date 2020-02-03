import factory
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()
import datetime

class UserFactory(factory.django.DjangoModelFactory):
    """
    ユーザー情報モデルのテストデータ
    """
    factory.Faker._DEFAULT_LOCALE = 'ja_JP'
    class Meta:
        model = User
    uuid =factory.LazyFunction(uuid.uuid4)
    username = factory.Sequence(lambda n: 'user%d' % n)
    #'sampleapp'をハッシュ化
    password = 'pbkdf2_sha256$150000$JYJw9nECjdhy$gG1tQJPaGf4tN8SllLO6fHw9C1UZTZohJOSBKEGsdT0='
    name = factory.Faker('name')
    email = factory.Sequence(lambda n: 'address%d@example.com' % n)
    birthday = factory.Faker('date_of_birth',minimum_age=0, maximum_age=115)
    is_staff = 0
    is_active = 1
    date_joined = datetime.datetime.now()
