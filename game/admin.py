from django.contrib import admin

from game.forms import PlayerTicketAdminForm
from game.forms import ResultatEuromillionAdminForm
from game.models import EuroMillionGame
from game.models import EuroMillionMessage
from game.models import EuroMilllionPatner
from game.models import PlayerTicket
from game.models import ResultatEuromillion
from game.models import VideoEuroMillion


@admin.register(ResultatEuromillion)
class ResultatEuromillionAdmin(admin.ModelAdmin):
    list_display = ("date", "jackpot", "winners")
    search_fields = ("date", "jackpot")
    list_filter = ("date",)
    form = ResultatEuromillionAdminForm


@admin.register(PlayerTicket)
class PlayerTicketAdmin(admin.ModelAdmin):
    list_display = ("code", "player_alias", "draw_date")
    search_fields = ("code", "player_alias")
    list_filter = ("draw_date",)
    form = PlayerTicketAdminForm


admin.site.register(
    [EuroMilllionPatner, EuroMillionGame, VideoEuroMillion, EuroMillionMessage]
)
