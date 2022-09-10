from django.db.models import (
    Model,
    CharField, SlugField,
    ForeignKey,
    UniqueConstraint,
    CASCADE,
)
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Stadium(Model):

    name = CharField(_('name'), max_length=254, unique=True)
    slug = SlugField(_('slug'), max_length=254, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('stadium')
        verbose_name_plural = _('stadiums')


class Seat(Model):
    """
    Each seat belongs to a stadium and has its own code.
    Also, a stadium can't have seats with same code (UniqueConstraint).
    """

    stadium = ForeignKey(
        Stadium,
        on_delete=CASCADE,
        related_name='seats',
        verbose_name=_('stadium'),
    )
    code = CharField(_('code'), max_length=8)

    def __str__(self):
        return f'Code : {self.code} - Stadium : {self.stadium.name}'

    class Meta:
        verbose_name = _('seat')
        verbose_name_plural = _('seats')
        constraints = (
            UniqueConstraint(
                fields=('stadium', 'code'),
                name='unique_seat_stadium_code'
            ),
        )
