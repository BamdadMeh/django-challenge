from django.db.models import Model, CharField
from django.utils.translation import gettext_lazy as _


class Team(Model):

    name = CharField(_('name'), max_length=254, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')
