from django.contrib import admin
from django.utils.html import format_html

from .models import Dragon_Post, Elder_Post, Baron_Post
from .models import Dragon_League, Elder_League, Baron_League
from .models import Dragon_Standings, Elder_Standings, Baron_Standings
from .models import Dragon_Solo_Sign_Ups, Elder_Team_Sign_Ups, Elder_Solo_Sign_Ups, Baron_Team_Sign_Ups

def resetLeague(modeladmin, request, queryset):
    queryset.update(acronym='TBD')
    queryset.update(team_name='Unnamed Team')
    queryset.update(top_laner='Top Laner')
    queryset.update(jungler='Jungler')
    queryset.update(mid_laner='Mid Laner')
    queryset.update(ad_carry='AD Carry')
    queryset.update(support='Support')
    queryset.update(substitute1='')
    queryset.update(sub1_role='N/A')
    queryset.update(substitute2='')
    queryset.update(sub2_role='N/A')
    queryset.update(substitute3='')
    queryset.update(sub3_role='N/A')

    resetLeague.short_description = "Reset a League with filler names."

def resetStandings(modeladmin, request, queryset):
    queryset.update(wins=0)
    queryset.update(losses=0)
    queryset.update(ties=0)

class LeagueAdmin(admin.ModelAdmin):
    list_display = ['acronym', 'team_name']
    ordering = ['team_name']
    actions = [resetLeague]

class StandingsAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'wins', 'losses', 'ties']
    ordering = ['team_name']
    actions = [resetStandings]

class TeamSignUpsAdmin(admin.ModelAdmin):
    list_display = ['your_summoner_name', 'team_name', 'op_gg_link','time_created']
    ordering = ['your_summoner_name']

    def op_gg_link(self,obj):
       return format_html("<a href='{url}' target='_blank' rel='noopener noreferrer'>OP.GG</a>", url=obj.getOPGGLink())
    
    op_gg_link.short_description = "na.op.gg"

class SoloSignUpsAdmin(admin.ModelAdmin):
    list_display = ['your_summoner_name', 'primary_role', 'secondary_role', 'op_gg_link', 'time_created']
    ordering = ['primary_role']

    def op_gg_link(self,obj):
       return format_html("<a href='{url}' target='_blank' rel='noopener noreferrer'>OP.GG</a>", url=obj.getOPGGLink())
   
    op_gg_link.short_description = "na.op.gg"



admin.site.site_header = "Ascension Esports Database"
admin.site.site_title = "It's alright"
admin.site.index_title = "Ascension Esports Backend"

admin.site.register(Dragon_League, LeagueAdmin)
admin.site.register(Elder_League, LeagueAdmin)
admin.site.register(Baron_League, LeagueAdmin)

admin.site.register(Dragon_Post)
admin.site.register(Elder_Post)
admin.site.register(Baron_Post)

admin.site.register(Dragon_Standings, StandingsAdmin)
admin.site.register(Elder_Standings, StandingsAdmin)
admin.site.register(Baron_Standings, StandingsAdmin)

admin.site.register(Dragon_Solo_Sign_Ups, SoloSignUpsAdmin)
admin.site.register(Elder_Solo_Sign_Ups, SoloSignUpsAdmin)
admin.site.register(Elder_Team_Sign_Ups, TeamSignUpsAdmin)
admin.site.register(Baron_Team_Sign_Ups, TeamSignUpsAdmin)