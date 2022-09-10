from django.contrib import admin

from apps.stadium.models import Stadium, Seat


class SeatInline(admin.StackedInline):

    model = Seat
    extra = 1


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):

    inlines = (SeatInline,)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):

    list_display = ('stadium', 'code')
    list_filter = ('stadium',)
