from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.views import APIView, Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.status import (

    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
)

from apps.match.models import Match, MatchSeatInfo
from apps.match.serializers import (
    MatchSerializer,
    MatchSeatInfoSerializer,
    ListCreateMatchSeatInfoSerializer,
    ListUpdateMatchSeatInfoSerializer,
)


class MatchCreateAPIView(CreateAPIView):
    """
    Define a new match.
    Permission : Only admin users have access.
    """

    permission_classes = (IsAdminUser,)

    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class MatchSeatInfoCreateAPIView(CreateAPIView):
    """
    Define a new seat for a match with given price.
    Permission : Only admin users have access.
    """

    permission_classes = (IsAdminUser,)

    queryset = MatchSeatInfo.objects.all()
    serializer_class = MatchSeatInfoSerializer


class ListCreateMatchSeatInfoAPIView(APIView):
    """
    Define several seats for a match with given price.
    Permission : Only admin users have access.
    """

    permission_classes = (IsAdminUser,)

    serializer_class = ListCreateMatchSeatInfoSerializer

    def post(self, request, *args, **kwargs):

        srz_data = self.serializer_class(data=request.data)

        if srz_data.is_valid():

            vd = srz_data.validated_data
            match = vd['match']
            price = vd['price']
            seats = vd['seats']
            seats_number = len(seats)

            MatchSeatInfo.objects.bulk_create(
                [
                    MatchSeatInfo(match=match, seat_id=seat, price=price)
                    for seat in seats
                ]
            )

            message = _(
                f'{seats_number} seats were created successfully for the match'
            )

            return Response(
                data={'message': message},
                status=HTTP_201_CREATED,
            )

        return Response(data=srz_data.errors, status=HTTP_400_BAD_REQUEST)


class ListUpdateMatchSeatInfoAPIView(APIView):
    """
    Update several seats for a match.
    Note : This View is used for reserving seats.
    Permission : Only authenticated users have access.
    """

    permission_classes = (IsAuthenticated,)

    serializer_class = ListUpdateMatchSeatInfoSerializer

    def put(self, request, match_id, *args, **kwargs):

        match = get_object_or_404(Match, id=match_id)

        srz_data = self.serializer_class(data=request.data, match=match)

        if srz_data.is_valid():

            seats = srz_data.validated_data['seats']
            seats_number = len(seats)
            now = timezone.now()

            match_seats = MatchSeatInfo.objects.filter(
                match=match,
                seat_id__in=seats,
            )
            match_seats.update(
                is_reserved=True,
                buyer=request.user,
                date_reserved=now,
            )

            message = _(
                f'{seats_number} seats were reserved successfully for the match'
            )

            return Response(
                data={'message': message},
                status=HTTP_202_ACCEPTED,
            )

        return Response(data=srz_data.errors, status=HTTP_400_BAD_REQUEST)
