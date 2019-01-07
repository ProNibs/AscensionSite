"""
Definition of models.
"""

from django.db import models
from django.urls import reverse

Positions = (('Top', 'Top'),('Jungle', 'Jungle'),('Mid', 'Mid'),('ADC', 'ADC'),('Support','Support'),('Substitute','Substitute'),
             ('Pending-Top','Pending-Top'), ('Pending-Jgl','Pending-Jgl'), ('Pending-Mid','Pending-Mid'),
             ('Pending-ADC','Pending-ADC'),('Pending-Sup','Pending-Sup'))

Roles = (('Top', 'Top'),('Jungle', 'Jungle'),('Mid', 'Mid'),('ADC', 'ADC'),('Support','Support'),('Fill','Fill'))

Leagues = (('Dragon', 'Dragon'),('Elder', 'Elder'),('Baron','Baron'))

Side_Choices = (('Blue','Blue'),('Red','Red'))



# Create your models here.

class A_League(models.Model):
    acronym = models.CharField(max_length=4)
    team_name = models.CharField(max_length=20)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    tie_breaker = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="This will change to false whenever the League is over.")

    top_laner = models.CharField(max_length=32)
    jungler = models.CharField(max_length=32)
    mid_laner = models.CharField(max_length=32)
    ad_carry = models.CharField(max_length=32)
    support = models.CharField(max_length=32)
    substitute1 = models.CharField(max_length=32, blank=True)
    sub1_role = models.CharField(max_length=20, choices=Roles, default='N/A', blank=True)
    substitute2 = models.CharField(max_length=32, blank=True)
    sub2_role = models.CharField(max_length=20, choices=Roles, default='N/A', blank=True)
    substitute3 = models.CharField(max_length=32, blank=True)
    sub3_role = models.CharField(max_length=20, choices=Roles, default='N/A', blank=True)
    coach = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.team_name
    def getTeamName(self):
        return self.team_name
    #def get_absolute_url(self):
    #   return reverse('baron', args=[str(self.team_name)])
    def getOPGGLink(self):
        multi_query = str(self.top_laner)+'%2C'+str(self.jungler)+'%2C'+str(self.mid_laner)+'%2C'+str(self.ad_carry)+'%2C'+str(self.support)
        final_query = 'http://na.op.gg/multi/query=' + multi_query
        return final_query
    class Meta:
        db_table="League_Table_Template"
        abstract = True

'''
General Design Pattern and Database Flow

Each League has a Players Table.
Teams are made from the Players Table.
There is a global League table that tracks which leagues are active and when started.

There is a match report backend that simply requires Blue Team, Red Team, and Riot MatchID.
It will use the Riot API to get stats on the match and assign those stats to each of the players.
It will update the avg/per_game stats for the players once numbers are assigned.
It will update the team score and the standings as well.

'''

# Players
#region Players
class A_Player(models.Model):
    def __init__(self, *args, **kwargs):
        super(A_Player, self).__init__(*args, **kwargs)
        self.old_largest_multi_kill = self.largest_multi_kill

    # This gives overall stats of a specific player
    summoner_name = models.CharField(max_length=32, unique=True)
    primary_role = models.CharField(max_length=20, choices=Roles)
    secondary_role = models.CharField(max_length=20, choices=Roles)

    # Stats on times played
    games_played = models.PositiveIntegerField(default=0)
    mins_played = models.PositiveIntegerField(default=0)
    first_bloods = models.PositiveIntegerField(default=0)
    largest_multi_kill = models.PositiveIntegerField(default=0)
    first_tower = models.PositiveIntegerField(default=0)

    # In Game stats
    kills = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    creep_score = models.PositiveIntegerField(default=0)
    gold = models.PositiveIntegerField(default=0)
    gold_share = models.FloatField(default=0)
    damage_done = models.PositiveIntegerField(default=0)
    damage_share = models.FloatField(default=0)
    vision_score = models.PositiveIntegerField(default=0)
    crowd_control_score = models.PositiveIntegerField(default=0)
    csd_at_ten = models.FloatField(default=0)

    # Calculated stats
    KDA = models.FloatField(default=0)
    avg_kills = models.FloatField(default=0)
    avg_deaths = models.FloatField(default=0)
    avg_assists = models.FloatField(default=0)
    avg_creep_score = models.FloatField(default=0)
    avg_gold = models.FloatField(default=0)
    avg_gold_share = models.FloatField(default=0)
    avg_damage_done = models.FloatField(default=0)
    avg_damage_share = models.FloatField(default=0)
    avg_vision_score = models.FloatField(default=0)
    avg_crowd_control_score = models.FloatField(default=0)
    avg_csd_at_ten = models.FloatField(default=0)

    creep_score_per_minute = models.FloatField(default=0)
    gold_per_minute = models.FloatField(default=0)
    damage_done_per_minute = models.FloatField(default=0)
    vision_score_per_minute = models.FloatField(default=0)
    crowd_control_score_per_minute = models.FloatField(default=0)


    def __str__(self):
        return self.summoner_name

    def save(self, *args, **kwargs): 
        if (self.games_played is not 0) and (self.mins_played is not 0):
            self.update_stats()
        super(A_Player, self).save(*args, **kwargs)
        
    def check_multi_kills(self):    #Check if old value greater than new
        if (self.largest_multi_kill < self.old_largest_multi_kill):
            self.largest_multi_kill = self.old_largest_multi_kill
        
    class Meta:
        db_table = "A Single Players Stats"
        abstract = True

    def update_stats(self):
        self.check_multi_kills()
        self.KDA = self.get_KDA()
        self.avg_kills = self.get_average_kills()
        self.avg_deaths = self.get_average_deaths()
        self.avg_assists = self.get_average_assists()
        self.avg_creep_score = self.get_average_creep_score()
        self.avg_gold = self.get_average_gold()
        self.avg_gold_share = self.get_average_gold_share()
        self.avg_damage_done = self.get_average_damage_done()
        self.avg_damage_share = self.get_average_damage_share()
        self.avg_vision_score = self.get_average_vision_score()
        self.avg_crowd_control_score = self.get_average_crowd_control_score()
        self.avg_csd_at_ten = self.get_average_csd_at_ten()
        
        self.creep_score_per_minute = self.get_creep_score_per_minute()
        self.gold_per_minute = self.get_gold_per_minute()
        self.damage_done_per_minute = self.get_damage_done_per_minute()
        self.vision_score_per_minute = self.get_vision_score_per_minute()
        self.crowd_control_score_per_minute = self.get_crowd_control_score_per_minute()
        

    def get_KDA(self):
        return (self.kills+ self.assists) / float(self.deaths)
    

    # Avg / Game
    def get_average_kills(self):
        return (self.kills / self.games_played)
    def get_average_deaths(self):
        return (self.deaths / self.games_played)
    def get_average_assists(self):
        return (self.assists // self.games_played)
    def get_average_creep_score(self):
        return (self.creep_score // self.games_played)
    def get_average_gold(self):
        return (self.gold // self.games_played)
    def get_average_gold_share(self):
        return (self.gold_share // self.games_played)
    def get_average_damage_done(self):
        return (self.damage_done // self.games_played)
    def get_average_damage_share(self):
        return (self.damage_share // self.games_played)    
    def get_average_vision_score(self):
        return (self.vision_score // self.games_played)
    def get_average_crowd_control_score(self):
        return (self.crowd_control_score // self.games_played)
    def get_average_csd_at_ten(self):
        return (self.csd_at_ten // self.games_played)

    # Avg / Mins.
    def get_creep_score_per_minute(self):
        return (self.creep_score / self.mins_played)
    def get_gold_per_minute(self):
        return (self.gold / self.mins_played)
    def get_damage_done_per_minute(self):
        return (self.damage_done / self.mins_played)
    def get_vision_score_per_minute(self):
        return (self.vision_score / self.mins_played)
    def get_crowd_control_score_per_minute(self):
        return (self.crowd_control_score / self.mins_played)

class Baron_Players(A_Player):
    def get_absolute_url(self):
        return reverse('baron_stats', args=(self.summoner_name,))

    class Meta:
        db_table="Baron Players"
        verbose_name_plural = "Baron Players"

#endregion

# Team Rosters
#region Teams
class Baron_League_Rosters(A_League):
    top_laner = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="top_laner"
        )
    jungler = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="jungler"
        )
    mid_laner = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="mid_laner"
        )
    ad_carry = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="ad_carry"
        )
    support = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="support"
        )
    substitute1 = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="substitute1",
        blank=True, null=True
        )
    substitute2 = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="substitute2",
        blank=True, null=True
        )
    substitute3 = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="substitute3",
        blank=True, null=True 
        )

    class Meta:
        db_table = "Baron Rosters"
        verbose_name_plural = "Baron Rosters"

#endregion

# Match Report
#region
class Report_Match(models.Model):
    blue_team = models.CharField(max_length=20)
    red_team = models.CharField(max_length=20)
    match_id = models.PositiveIntegerField()
    did_blue_win = models.BooleanField(default=True, help_text="DOUBLE CHECK THIS")
    week_number = models.PositiveIntegerField(default=1)
    game_number = models.PositiveIntegerField(help_text="In BoX series, it's game number. Otherwise, game number for a given week")
    
    blue_top_laner = models.CharField(max_length=32)
    blue_jungler = models.CharField(max_length=32)
    blue_mid_laner = models.CharField(max_length=32)
    blue_ad_carry = models.CharField(max_length=32)
    blue_support = models.CharField(max_length=32)

    red_top_laner = models.CharField(max_length=32)
    red_jungler = models.CharField(max_length=32)
    red_mid_laner = models.CharField(max_length=32)
    red_ad_carry = models.CharField(max_length=32)
    red_support = models.CharField(max_length=32)

    def __str__(self):
        return str(self.match_id)

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    class Meta:
        db_table = "A Single Match"
        abstract = True

class Baron_Match_Report(Report_Match):
    # Team+Player Fields
    #region
    blue_team = models.ForeignKey(
        Baron_League_Rosters,
        on_delete=models.CASCADE,
        related_name="blue_team"
        )
    red_team = models.ForeignKey(
        Baron_League_Rosters,
        on_delete=models.CASCADE,
        related_name="red_team"
        )

    blue_top_laner = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="blue_top_laner"
        )
    blue_jungler = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="blue_jungler"
        )
    blue_mid_laner = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="blue_mid_laner"
        )
    blue_ad_carry = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="blue_ad_carry"
        )
    blue_support = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="blue_support"
        )


    red_top_laner = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="red_top_laner"
        )
    red_jungler = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="red_jungler"
        )
    red_mid_laner = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="red_mid_laner"
        )
    red_ad_carry = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="red_ad_carry"
        )
    red_support = models.OneToOneField(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="red_support"
        )
    #endregion

    def save(self, *args, **kwargs):    # Get team stats here
        super(Baron_Match_Report, self).save(*args, **kwargs)
        if self.did_blue_win:
            self.blue_team.wins += 1
            self.red_team.losses += 1
        else:
            self.blue_team.losses += 1
            self.red_team.wins += 1

        self.blue_team.save(*args, **kwargs)
        self.red_team.save(*args, **kwargs)
        

    class Meta:
        db_table = "Baron Match Report"
        verbose_name_plural = "Baron Match Report"

#endregion

# Global League Tracking Table
# Once created, will create matches that link back to this creation.
# Will pull all active rosters in a League
common_weeks = ((5,5),(9,9))
series_choices = ((1,'Bo1'),(2,'Bo2'),(3,'Bo3'))

class League_Track(models.Model):
    league_name = models.CharField(max_length=50, default='Dragon League X')
    league = models.CharField(max_length=50, choices=Leagues)
    start_date = models.DateField(auto_now_add=True)
    week_length = models.PositiveIntegerField(default=9, choices=common_weeks)
    regular_season_schedule = models.PositiveIntegerField(default=1, choices=series_choices)
    number_of_teams = models.PositiveIntegerField(default=10, help_text='This is always assumed to be 10')
    pools = models.PositiveIntegerField(default=1, help_text='In case we got multiple Elder Leagues again')
    
    def __str__(self):
        return self.league_name

    def get_League(self):
        self.temp_value = None
        self.team = None
        if self.league == 'Dragon':
            self.temp_value = Dragon_League
        elif self.league == 'Elder':
            self.temp_value = Elder_League
        elif self.league == 'Baron':
            self.temp_value = Baron_League_Rosters
        self.team = models.ForeignKey(self.temp_value, on_delete=models.CASCADE, related_name='rosters', limit_choices_to={'is_active': True})
        print(self.team.team_name.all())

    def create_league(self):
        if self.week_length is 9: # 9-week schedule
            if self.regular_season_schedule is 1:   #Bo1, double round robin
                return 0
            else:   # 9-week schedule with Bo2/Bo3 is single round robin
                return 0
        elif self.week_length is 5: # Shortened 5-week schedule, single round robin
            return 0

    def save(self, *args, **kwargs):
        self.get_League()
        super(League_Track, self).save(*args, **kwargs)

    class Meta:
        db_table = "League Tracker"
        verbose_name_plural = "League Tracker"

class Dragon_League(A_League):
    class Meta:
        db_table="Dragon League"
        verbose_name_plural = "Dragon League"


class Elder_League(A_League):
    class Meta:
        db_table="Elder League"
        verbose_name_plural = "Elder League"

class Baron_League(A_League):
    class Meta:
        db_table="Baron League"
        verbose_name_plural = "Baron League"





# Sign Ups
#region
class Generic_Team_Sign_Up(A_League):
    your_summoner_name = models.CharField(max_length=28)
    discord_name = models.CharField(max_length=30)
    email_address = models.EmailField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Team Sign Up Form Template"
        abstract = True

class Generic_Solo_Sign_Up(models.Model):
    your_summoner_name = models.CharField(max_length=28)
    primary_role = models.CharField(max_length=20, choices=Roles)
    secondary_role = models.CharField(max_length=20, choices=Roles)
    discord_name = models.CharField(max_length=30)
    email_address = models.EmailField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    
    def getOPGGLink(self):
        final_query = 'http://na.op.gg/summoner/userName=' + str(self.your_summoner_name)
        return final_query

    class Meta:
        db_table = "Solo Sign Up Form Template"
        abstract = True


class Dragon_Solo_Sign_Ups(Generic_Solo_Sign_Up):
    class Meta:
        db_table = "Dragon Solo Sign Up"
        verbose_name_plural = "Dragon Solo Sign Ups"

class Elder_Team_Sign_Ups(Generic_Team_Sign_Up):
    class Meta:
        db_table = "Elder Team Sign Up"
        verbose_name_plural = "Elder Team Sign Ups"

class Elder_Solo_Sign_Ups(Generic_Solo_Sign_Up):
    duo_partner = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = "Elder Solo Sign Up"
        verbose_name_plural = "Elder Solo Sign Ups"

class Baron_Team_Sign_Ups(Generic_Team_Sign_Up):
    class Meta:
        db_table = "Baron League Sign Up"
        verbose_name_plural = "Baron Sign Ups"
#endregion


# Posts
#region
class Post(models.Model):
    title = models.CharField(max_length=64)
    date = models.DateTimeField()
    author = models.CharField(max_length=64)
    body = models.TextField()
 
    def __str__(self):
        return "%s (%s)" % (self.title, self.author)
    class Meta:
        abstract = True

class Dragon_Post(Post):
    class Meta:
        db_table = "Dragon News"
        verbose_name_plural = "Dragon News"

class Elder_Post(Post):
    class Meta:
        db_table = "Elder News"
        verbose_name_plural = "Elder News"

class Baron_Post(Post):
    class Meta:
        db_table = "Baron News"
        verbose_name_plural = "Baron News"
#endregion
