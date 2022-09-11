from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    IntegerField,
    ListField,
    SerializerMethodField,
    ValidationError,
)

from apps.match.models import Match, MatchSeatInfo


class MatchSerializer(ModelSerializer):

    match_info = SerializerMethodField()

    def get_match_info(self, match: Match) -> dict:

        match_datetime = match.datetime

        return {
            'stadium': match.stadium.name,
            'host_team': match.host_team.name,
            'guest_team': match.guest_team.name,
            'date': match_datetime.strftime('%d %b %Y'),
            'time': match_datetime.strftime('%H : %M'),
        }

    class Meta:

        model = Match
        fields = (
            'stadium',
            'host_team',
            'guest_team',
            'datetime',
            'match_info',
        )

        extra_kwargs = {
            'stadium': {'write_only': True},
            'host_team': {'write_only': True},
            'guest_team': {'write_only': True},
            'datetime': {'write_only': True},
            }

    def validate(self, data):

        if data['host_team'] == data['guest_team']:
            raise ValidationError(_("Both teams can't be same"))

        match = Match.objects.filter(
            stadium=data['stadium'],
            datetime=data['datetime'],
            )
        if match.exists():
            raise ValidationError(
                _(('Match with this stadium and datetime already exists.'))
            )

        return data


class MatchSeatInfoSerializer(ModelSerializer):

    match_seat_info = SerializerMethodField()

    def get_match_seat_info(self, match_seat: MatchSeatInfo) -> dict:

        return {
            'match': str(match_seat.match),
            'seat': str(match_seat.seat),
            'price': match_seat.price,
        }

    class Meta:

        model = MatchSeatInfo
        fields = ('match', 'seat', 'price', 'match_seat_info')

        extra_kwargs = {
            'match': {'write_only': True},
            'seat': {'write_only': True},
            'price': {'write_only': True},
            }

    def validate(self, data):

        match = data['match']
        seat = data['seat']

        match_seat = MatchSeatInfo.objects.filter(
            match=match,
            seat=seat,
            )

        if match_seat.exists():
            raise ValidationError(
                _(('This seat is already defined for this match.'))
            )

        if not match.stadium.seats.only('id').contains(seat):
            # Here, we check if selected seat, belongs to stadium or not

            raise ValidationError(
                _(
                    f'Stadium of this match, does not have seat '
                    f'with this code: {seat.code}')
                )

        return data


class ListCreateMatchSeatInfoSerializer(Serializer):

    match = IntegerField()
    price = IntegerField()
    seats = ListField(child=IntegerField(), min_length=2)

    def validate_match(self, match_pk):

        match = Match.objects.filter(pk=match_pk)

        if not match.exists():

            raise ValidationError('Match does not exist')

        return match.first()

    def validate(self, data):

        match = data['match']
        seats = data['seats']
        seats_number = len(seats)

        if MatchSeatInfo.objects.filter(
            match=match,
            seat_id__in=seats,
        ).exists():
                raise ValidationError(
                    _(('One of seats is already defined for the match.'))
                )

        if match.stadium.seats.filter(pk__in=seats).aggregate(count=Count('pk'))['count'] != seats_number:
            # Here, we check if all selected seats, belong to stadium or not.

            raise ValidationError(
                _(
                    'Stadium of this match, does not have one of seats.'
                )
            )

        return data


class ListUpdateMatchSeatInfoSerializer(Serializer):

    seats = ListField(child=IntegerField(), min_length=1, max_length=10)

    def __init__(self, *args, **kwargs):

        self.match = kwargs.pop('match', None)
        super().__init__(*args, **kwargs)

    def validate(self, data):

        seats = data['seats']
        seats_number = len(seats)

        if MatchSeatInfo.objects.filter(
            match=self.match,
            seat_id__in=seats,
            is_reserved=True,
        ).exists():
                raise ValidationError(
                    _(('One of seats is already reserved for the match.'))
                )

        if self.match.stadium.seats.filter(pk__in=seats).aggregate(count=Count('pk'))['count'] != seats_number:
            # Here, we check if all selected seats, belong to stadium or not.

            raise ValidationError(
                _(
                    'Stadium of this match, does not have one of seats.'
                )
            )

        return data
