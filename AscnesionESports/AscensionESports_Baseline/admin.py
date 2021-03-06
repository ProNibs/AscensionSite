from django.contrib import admin
from django.utils.html import format_html

from .models import Dragon_Post, Elder_Post, Baron_Post
from .models import Dragon_League_Rosters, Elder_League_Rosters, Baron_League_Rosters
#from .models import Dragon_Standings, Elder_Standings, Baron_Standings
from .models import Baron_Players
from .models import Baron_Match_Report
from .models import Dragon_Solo_Sign_Ups, Dragon_Team_Sign_Ups, Elder_Team_Sign_Ups, Elder_Solo_Sign_Ups, Baron_Team_Sign_Ups
from .models import Start_League
from .models import BadAccounts

def resetLeague(modeladmin, request, queryset):
    queryset.update(acronym='TBD')
    queryset.update(team_name='Unnamed Team')
    #queryset.update(top_laner='Top Laner')
    #queryset.update(jungler='Jungler')
    #queryset.update(mid_laner='Mid Laner')
    #queryset.update(ad_carry='AD Carry')
    #queryset.update(support='Support')
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
    queryset.update(tie_breaker=0)

class LeagueAdmin(admin.ModelAdmin):
    list_display = ['acronym', 'team_name', 'wins', 'losses', 'top_laner', 'jungler','mid_laner','ad_carry','support']
    ordering = ['-wins','team_name']
    actions = [resetLeague]

class StandingsAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'wins', 'tie_breaker']
    ordering = ['wins', 'tie_breaker']
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

class LeaguePlayersAdmin(admin.ModelAdmin):
    list_display = ['summoner_name', 'games_played', 'KDA']
    list_filter = ('primary_role','secondary_role')
    fieldsets = (
        ('Player Info', {
            'fields':('summoner_name','primary_role','secondary_role')
        }),
        ("Previous Name and Alt Accounts listing", {
            'fields': ('previous_ign', 'alt_names')    
        }),
        ("Global Team Stats -- Don't edit unless we fucked up the stats", {
            'fields':(('games_played','mins_played'),
                      ('first_bloods','first_tower','largest_multi_kill')
                      )         
        }),
        ("Player Stats -- Don't edit unless we fucked up the stats", {
            'fields':(('kills','deaths','assists'),
                      ('creep_score','csd_at_ten','gold','gold_share'),
                      ('damage_done','damage_share'),
                      ('vision_score','crowd_control_score')
                     )         
        }),
        ("Calculated Avg. Game Stats -- Don't edit ever (editing above will change these values)", {
            'fields':(('KDA','avg_kills','avg_deaths','avg_assists'),
                      ('avg_creep_score','avg_csd_at_ten','avg_gold','avg_gold_share'),
                      ('avg_damage_done','avg_damage_share'),
                      ('avg_vision_score','avg_crowd_control_score')
                     )         
        }),
        ("Calculated Per Minute Stats -- Don't edit ever (editing above will change these values)", {
            'fields':(('creep_score_per_minute','gold_per_minute','damage_done_per_minute'),
                      ('vision_score_per_minute','crowd_control_score_per_minute')
                     )         
        })
        )

class MatchReportAdmin(admin.ModelAdmin):
    list_display = ['match_time', 'game_number', 'blue_team', 'red_team']
    ordering = ['-match_time','game_number']
    fields = [('match_id','week_number','game_number','match_time'),
              ('did_blue_win'),
              ('blue_team','red_team'),
              ('blue_top_laner','red_top_laner'),
              ('blue_jungler','red_jungler'),
              ('blue_mid_laner','red_mid_laner'),
              ('blue_ad_carry','red_ad_carry'),
              ('blue_support','red_support')]


class BadAccountsAdmin(admin.ModelAdmin):
    list_display = ['summoner_name','discord_name','who_added_person','reason_for_ban','time_added']
    list_filter = [('reason_for_ban')]
    ordering = ['time_added']
    fields = [ ('summoner_name','discord_name','summoner_id'),
               ('who_added_person','reason_for_ban'),
               ('supporting_documentation')
              ]



admin.site.site_header = "Ascension Esports Database"
admin.site.site_title = "It's alright"
admin.site.index_title = "Ascension Esports Backend"

admin.site.register(Baron_Players,LeaguePlayersAdmin)
admin.site.register(Baron_Match_Report,MatchReportAdmin)

admin.site.register(Dragon_League_Rosters, LeagueAdmin)
admin.site.register(Elder_League_Rosters, LeagueAdmin)
admin.site.register(Baron_League_Rosters, LeagueAdmin)

admin.site.register(Start_League)

admin.site.register(Dragon_Solo_Sign_Ups, SoloSignUpsAdmin)
admin.site.register(Dragon_Team_Sign_Ups, TeamSignUpsAdmin)
admin.site.register(Elder_Solo_Sign_Ups, SoloSignUpsAdmin)
admin.site.register(Elder_Team_Sign_Ups, TeamSignUpsAdmin)
admin.site.register(Baron_Team_Sign_Ups, TeamSignUpsAdmin)

admin.site.register(Dragon_Post)
admin.site.register(Elder_Post)
admin.site.register(Baron_Post)

admin.site.register(BadAccounts, BadAccountsAdmin)