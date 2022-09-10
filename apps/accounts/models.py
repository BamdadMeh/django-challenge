from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import EmailField, BooleanField, DateTimeField
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    A User model with admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """

    email = EmailField(
        _('email address'),
        unique=True,
        help_text=_(
            'Required. 254 characters or fewer. '
            'It must be a valid email address.'
        ),
        error_messages={
            'unique': _('A user with that email address already exists.'),
        },
    )
    is_staff = BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user '
            'can log into this admin site.'
        ),
    )
    is_active = BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
