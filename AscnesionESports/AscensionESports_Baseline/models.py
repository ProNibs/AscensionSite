"""
Definition of models.
"""

from django.db import models

Positions = (('Top', 'Top'),('Jungle', 'Jungle'),('Mid', 'Mid'),('ADC', 'ADC'),('Support','Support'),('Substitute','Substitute'),
             ('Pending-Top','Pending-Top'), ('Pending-Jgl','Pending-Jgl'), ('Pending-Mid','Pending-Mid'),
             ('Pending-ADC','Pending-ADC'),('Pending-Sup','Pending-Sup'))

Roles = (('Top', 'Top'),('Jungle', 'Jungle'),('Mid', 'Mid'),('ADC', 'ADC'),('Support','Support'),('Fill','Fill'))

Leagues = (('Dragon', 'Dragon'),('Elder', 'Elder'),('Baron','Baron'))

Side_Choices = (('Blue','Blue'),('Red','Red'))
# Create your models here.

class A_Player(models.Model):
    # This gives overall stats of a specific player
    summoner_name = models.CharField(max_length=32, unique=True)
    team_name = models.CharField(max_length=20)
    position = models.CharField(max_length=20, choices=Roles)

    # Stats on times played
    games_played = models.PositiveIntegerField(default=0)
    mins_played = models.PositiveIntegerField(default=0)
    first_blood = models.PositiveIntegerField(default=0)
    
    # In Game stats
    kills = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    creep_score = models.PositiveIntegerField(default=0)
    gold = models.PositiveIntegerField(default=0)
    gold_share = models.FloatField(default=0)
    damage_done = models.PositiveIntegerField(default=0)
    vision_score = models.PositiveIntegerField(default=0)
    crowd_control_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.summoner_name

    def get_absolute_url(self):
        return reverse('model-detail-view', arg_str=[str(self.id)])

    def get_KDA(self):
        return (self.kills+ self.assists) / float(self.deaths)

    # Avg / Game
    def get_average_kills(self):
        return (self.kills / self.games_played)
    def get_average_deaths(self):
        return (self.deaths / self.games_played)
    def get_average_assists(self):
        return (self.assists / self.games_played)
    def get_average_creep_score(self):
        return (self.creep_score / self.games_played)
    def get_average_gold(self):
        return (self.gold / self.games_played)
    def get_average_gold_share(self):
        return (self.gold_share / self.games_played)
    def get_average_damage_done(self):
        return (self.damage_done / self.games_played)
    def get_average_vision_score(self):
        return (self.vision_score / self.games_played)
    def get_average_crowd_control_score(self):
        return (self.crowd_control_score / self.games_played)


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

class A_Match(models.Model):
    blue_team = models.CharField(max_length=20)
    red_team = models.CharField(max_length=20)
    mins_played = models.PositiveIntegerField()


class A_Team_Stats(models.Model):
    team_side = models.CharField(max_length=4, choices=Side_Choices)

class A_Position_Stats(models.Model):
    # This gives overall stats of a specific player
    summoner_name = models.CharField(max_length=32, unique=True)

    # Stats on times played
    first_blood = models.BooleanField(default=False)
    largest_mult_kill = models.PositiveIntegerField(default=0)
    
    # In Game stats
    kills = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    creep_score = models.PositiveIntegerField(default=0)
    gold = models.PositiveIntegerField(default=0)
    damage_done = models.PositiveIntegerField(default=0)
    vision_score = models.PositiveIntegerField(default=0)
    crowd_control_score = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "A Single Roles Stats"
        abstract = True

    
class A_League(models.Model):
    acronym = models.CharField(max_length=4)
    team_name = models.CharField(max_length=20)
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
    def get_absolute_url(self):
        return reverse('model-detail-view', arg_str=[str(self.id)])
    def getOPGGLink(self):
        multi_query = str(self.top_laner)+'%2C'+str(self.jungler)+'%2C'+str(self.mid_laner)+'%2C'+str(self.ad_carry)+'%2C'+str(self.support)
        final_query = 'http://na.op.gg/multi/query=' + multi_query
        return final_query
    class Meta:
        db_table="League_Table_Template"
        abstract = True

class A_Team(models.Model):
    team_name = models.CharField(max_length=30)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.team_name
    def get_absolute_url(self):
        return reverse('model-detail-view', arg_str=[str(self.id)])
    class Meta:
        db_table = "Team_Template"
        abstract = True

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

class Dragon_League(A_League):
    class Meta:
        db_table="Dragon League"
        verbose_name_plural = "Dragon League"

class Dragon_Standings(A_Team):
    class Meta:
        db_table="Dragon League Standing"
        verbose_name_plural = "Dragon League Standings"

class Dragon_Solo_Sign_Ups(Generic_Solo_Sign_Up):
    class Meta:
        db_table = "Dragon Solo Sign Up"
        verbose_name_plural = "Dragon Solo Sign Ups"

class Elder_League(A_League):
    class Meta:
        db_table="Elder League"
        verbose_name_plural = "Elder League"

class Elder_Standings(A_Team):
    class Meta:
        db_table="Elder League Standing"
        verbose_name_plural = "Elder League Standings"

class Elder_Team_Sign_Ups(Generic_Team_Sign_Up):
    class Meta:
        db_table = "Elder Team Sign Up"
        verbose_name_plural = "Elder Team Sign Ups"

class Elder_Solo_Sign_Ups(Generic_Solo_Sign_Up):
    class Meta:
        db_table = "Elder Solo Sign Up"
        verbose_name_plural = "Elder Solo Sign Ups"

class Baron_League(A_League):
    class Meta:
        db_table="Baron League"
        verbose_name_plural = "Baron League"

class Baron_Standings(A_Team):
    class Meta:
        db_table="Baron League Standing"
        verbose_name_plural = "Baron League Standings"

class Baron_Team_Sign_Ups(Generic_Team_Sign_Up):
    class Meta:
        db_table = "Baron League Sign Up"
        verbose_name_plural = "Baron Sign Ups"

 
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