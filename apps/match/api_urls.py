from django.urls import path

from apps.match.api_views import (
    MatchCreateAPIView,
    MatchSeatInfoCreateAPIView,
    ListCreateMatchSeatInfoAPIView,
    ListUpdateMatchSeatInfoAPIView,
)


api_urls = [

    path('', MatchCreateAPIView.as_view(), name='api_create_match'),
    path(
        'match_seat/',
        MatchSeatInfoCreateAPIView.as_view(),
        name='api_create_match_seat'
    ),
    path(
        'match_seat_list/',
        ListCreateMatchSeatInfoAPIView.as_view(),
        name='api_create_list_match_seat'
    ),
    path(
        'match_seat_list_booking/<int:match_id>/',
        ListUpdateMatchSeatInfoAPIView.as_view(),
        name='api_update_list_match_seat'
    ),
]
