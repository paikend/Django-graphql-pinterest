import pytz
from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.urls import reverse
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from enum import auto



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, type, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, type=type, **extra_fields)
        user.set_password(password)
        print(password, type, email)
        user.save(using=self._db)
        return user

    def create_user(self, email, type, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, type, password, **extra_fields)

    def create_superuser(self, email, type, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, type, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    customized User
    """
    email = models.EmailField(
        verbose_name=_('email id'),
        max_length=64,
        unique=True,
        help_text='이메일(아이디)'
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_delete = models.DateTimeField(
        default=None,
        blank=True, 
        null=True,
        help_text=_('계정 삭제 여부')
    )
    type = models.CharField(
        _('user type'),
        max_length=1,
        choices=(
            ('g', '일반 계정'),
            ('b', '비니지스 계정'),
            ('a', '관리자'),
        ), blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['type']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

class UserProfile(models.Model):
    """
    profile about  user
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        help_text='연결된 계정',
        blank=True, null=True,
        on_delete=models.CASCADE,
    )
    # necessary fields
    name = models.CharField(
        verbose_name='name',
        help_text='이름',
        max_length=20,
        null=True, blank=True,
    )
    gender = models.CharField(
        verbose_name='gender',
        help_text='성별',
        max_length=6,
        null=True, blank=True,
    )
    personal_presentation = models.TextField(
        verbose_name='personal presentation',
        help_text='자기 소개',
        null=True, blank=True,
    )
    location = models.TextField(
        verbose_name='location',
        help_text='위치',
        null=True, blank=True,
    )
    web_site = models.URLField(
        verbose_name='web site',
        help_text='웹사이트',
        null=True, blank=True,
    )
    country_code = models.TextField(
        verbose_name=_('contry code'),
        max_length=2,
        blank=True, 
        null=True,
        help_text='국가 코드'
    )
    is_adult = models.BooleanField(
        _('adult certification'),
        default=False,
        help_text=_('성인 여부'),
    )

    def __str__(self):
        return f'({self.user.email})'



