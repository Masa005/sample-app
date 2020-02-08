from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from account import validators
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
import uuid


class UserManager(BaseUserManager):
    """
    ユーザーマネージャーモデル

    """
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    ユーザー情報モデル

    """
    uuid = models.UUIDField(default=uuid.uuid4,
                            primary_key=True, editable=False)
    userid_validator = validators.UnicodeUseridValidator()

    username = models.CharField(
        _('ユーザー名'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters,digits'
                    ' and @/./+/-/_ only.'),
        validators=[userid_validator],
        error_messages={
            'unique': _("このユーザー名は既に登録済みです。"),

        },
    )
    name = models.CharField(_('name'), max_length=180, blank=False)
    email = models.EmailField(_('email address'), blank=False, unique=True,
                              error_messages={'unique': _("このメールアドレスは"
                                                          "既に登録済みです。")}, )
    birthday = models.DateField(_('生年月日'), null=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into '
                    'this admin site.'), )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'birthday']

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_name(self):
        """Return the name for the user."""
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
