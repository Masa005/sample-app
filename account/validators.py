from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UnicodeUseridValidator(validators.RegexValidator):
    regex = r'^[0-9a-zA-Z.@+-]+$'
    message = _(
        '有効なユーザーIDを入力してください。'
        '半角英数、 @/./+/-/_ を使用できます。'
    )
    flags = 0
