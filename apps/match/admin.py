from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.match.models import Match, MatchSeatInfo


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):

    list_display = ('host_team', 'guest_team', 'stadium', 'datetime')
    list_filter = ('stadium',)


@admin.register(MatchSeatInfo)
class MatchSeatInfoAdmin(admin.ModelAdmin):

    list_display = (
        'match', 'seat', 'price', 'is_reserved', 'is_paid', 'buyer'
    )
