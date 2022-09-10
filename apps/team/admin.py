from django.contrib import admin

from apps.team.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    search_fields = ('name',)
