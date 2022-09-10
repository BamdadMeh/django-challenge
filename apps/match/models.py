from django.db.models import (
    Model,
    DateTimeField, PositiveBigIntegerField, BooleanField,
    ForeignKey,
    ManyToManyField,
    UniqueConstraint,
    CASCADE,
)
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings

from apps.stadium.models import Stadium, Seat
from apps.team.models import Team


class Match(Model):

    stadium = ForeignKey(
        Stadium,
        on_delete=CASCADE,
        related_name='matches',
        verbose_name=_('stadium')
    )
    host_team = ForeignKey(
        Team,
        on_delete=CASCADE,
        related_name='hmatches',
        verbose_name=_('host team')
    )
    guest_team = ForeignKey(
        Team,
        on_delete=CASCADE,
        related_name='gmatches',
        verbose_name=_('guest team')
    )
    seats = ManyToManyField(
        Seat,
        through='MatchSeatInfo',
        related_name='matches',
        verbose_name=(_('seats')),
    )
    datetime = DateTimeField(_('datetime'))

    def __str__(self):
        return f'Host : {self.host_team.name}, Guest : {self.guest_team.name}'

    class Meta:
        verbose_name = _('match')
        verbose_name_plural = _('matches')
        ordering = ('-datetime',)
        constraints = (
            UniqueConstraint(
                fields=('stadium', 'datetime'),
                name='unique_match_stadium_datetime'
            ),
        )

    def clean(self):

        super().clean()

        if (
            hasattr(self, 'host_team') and
            hasattr(self, 'guest_team') and
            self.host_team == self.guest_team
        ):

            raise ValidationError(_("Both teams can't be same"))


class MatchSeatInfo(Model):

    match = ForeignKey(
        Match,
        on_delete=CASCADE,
        related_name='match_seats_info',
        verbose_name=_('match')
    )
    seat = ForeignKey(
        Seat,
        on_delete=CASCADE,
        related_name='match_seats_info',
        verbose_name=_('seat')
    )
    price = PositiveBigIntegerField(_('price'))

    buyer = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='bought_seats',
        verbose_name=_('buyer'),
        null=True,
        blank=True,
    )
    is_reserved = BooleanField(
        _('reserved status'),
        default=False,
        help_text=_('Designates whether the seat is reserved or not.'),
    )
    is_paid = BooleanField(
        _('paid'),
        default=False,
        help_text=_('Designates whether the seat is bought or not. '),
    )
    date_reserved = DateTimeField(_('date reserved'), null=True, blank=True)

    def __str__(self):
        return f'Match : {self.match}, Code : {self.seat.code}'

    class Meta:
        verbose_name = _('match seat info')
        verbose_name_plural = _('match seats info')
        constraints = (
            UniqueConstraint(
                fields=('match', 'seat'),
                name='unique_info_match_seat'
            ),
        )

    def clean(self):

        super().clean()

        if (
            hasattr(self, 'match') and
            hasattr(self, 'seat') and
            not self.match.stadium.seats.only('id').contains(self.seat)
        ):
            # Here, we check if selected seat, belongs to stadium or not

            raise ValidationError(
                _(
                    f'Stadium of this match, does not have seat '
                    f'with this code: {self.seat.code}')
                )

        if self.is_reserved and not self.date_reserved:
            raise ValidationError(
                _("Can't reserve without date of reservation !")
            )

        if self.date_reserved and not self.is_reserved:
            raise ValidationError(
                _("Can't set date of reservation without reserving !")
            )

        if self.is_paid and not self.is_reserved:
            raise ValidationError(_("Can't be paid without reserving !"))
