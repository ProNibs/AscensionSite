"""
Definition of models.
"""

from django.db import models
from django.urls import reverse
import datetime
import random

Positions = (('Top', 'Top'),('Jungle', 'Jungle'),('Mid', 'Mid'),('ADC', 'ADC'),('Support','Support'),('Substitute','Substitute'),
             ('Pending-Top','Pending-Top'), ('Pending-Jgl','Pending-Jgl'), ('Pending-Mid','Pending-Mid'),
             ('Pending-ADC','Pending-ADC'),('Pending-Sup','Pending-Sup'))

Roles = (('Top', 'Top'),('Jungle', 'Jungle'),('Mid', 'Mid'),('ADC', 'ADC'),('Support','Support'),('Fill','Fill'))

Leagues = (('Dragon', 'Dragon'),('Elder', 'Elder'),('Baron','Baron'))

Side_Choices = (('Blue','Blue'),('Red','Red'))



# Create your models here.
class A_League(models.Model):
    acronym = models.CharField(max_length=4)
    team_name = models.CharField(max_length=25)
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

class Dragon_Players(A_Player):
    def get_absolute_url(self):
        return reverse('dragon_stats', args=(self.summoner_name,))

    class Meta:
        db_table="Dragon Players"
        verbose_name_plural = "Dragon Players"

class Elder_Players(A_Player):
    def get_absolute_url(self):
        return reverse('elder_stats', args=(self.summoner_name,))

    class Meta:
        db_table="Elder Players"
        verbose_name_plural = "Elder Players"

class Baron_Players(A_Player):
    def get_absolute_url(self):
        return reverse('baron_stats', args=(self.summoner_name,))

    class Meta:
        db_table="Baron Players"
        verbose_name_plural = "Baron Players"

#endregion

# Team Rosters
#region Teams
class Dragon_League_Rosters(A_League):
    top_laner = models.OneToOneField(
        Dragon_Players,
        on_delete=models.CASCADE,
        related_name="top_laner"
        )
    jungler = models.OneToOneField(
        Dragon_Players,
        on_delete=models.CASCADE,
        related_name="jungler"
        )
    mid_laner = models.OneToOneField(
        Dragon_Players,
        on_delete=models.CASCADE,
        related_name="mid_laner"
        )
    ad_carry = models.OneToOneField(
        Dragon_Players,
        on_delete=models.CASCADE,
        related_name="ad_carry"
        )
    support = models.OneToOneField(
        Dragon_Players,
        on_delete=models.CASCADE,
        related_name="support"
        )
    substitute1 = models.OneToOneField(
        Dragon_Players,
        on_delete=models.CASCADE,
        related_name="substitute1",
        blank=True, null=True
        )
    substitute2 = models.OneToOneField(
        Dragon_Players,
        on_delete=models.CASCADE,
        related_name="substitute2",
        blank=True, null=True
        )
    substitute3 = models.OneToOneField(
        Dragon_Players,
        on_delete=models.CASCADE,
        related_name="substitute3",
        blank=True, null=True 
        )

    class Meta:
        db_table = "Dragon Rosters"
        verbose_name_plural = "Dragon Rosters"


class Elder_League_Rosters(A_League):
    top_laner = models.OneToOneField(
        Elder_Players,
        on_delete=models.CASCADE,
        related_name="top_laner"
        )
    jungler = models.OneToOneField(
        Elder_Players,
        on_delete=models.CASCADE,
        related_name="jungler"
        )
    mid_laner = models.OneToOneField(
        Elder_Players,
        on_delete=models.CASCADE,
        related_name="mid_laner"
        )
    ad_carry = models.OneToOneField(
        Elder_Players,
        on_delete=models.CASCADE,
        related_name="ad_carry"
        )
    support = models.OneToOneField(
        Elder_Players,
        on_delete=models.CASCADE,
        related_name="support"
        )
    substitute1 = models.OneToOneField(
        Elder_Players,
        on_delete=models.CASCADE,
        related_name="substitute1",
        blank=True, null=True
        )
    substitute2 = models.OneToOneField(
        Elder_Players,
        on_delete=models.CASCADE,
        related_name="substitute2",
        blank=True, null=True
        )
    substitute3 = models.OneToOneField(
        Elder_Players,
        on_delete=models.CASCADE,
        related_name="substitute3",
        blank=True, null=True 
        )

    class Meta:
        db_table = "Elder Rosters"
        verbose_name_plural = "Elder Rosters"


class Baron_League_Rosters(A_League):   # Foreign Key because Match Report references it too
    top_laner = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="top_laner"
        )
    jungler = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="jungler"
        )
    mid_laner = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="mid_laner"
        )
    ad_carry = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="ad_carry"
        )
    support = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="support"
        )
    substitute1 = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="substitute1",
        blank=True, null=True
        )
    substitute2 = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="substitute2",
        blank=True, null=True
        )
    substitute3 = models.ForeignKey(
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
    blue_team = models.CharField(max_length=25)
    red_team = models.CharField(max_length=25)
    match_id = models.PositiveIntegerField(default=0)
    did_blue_win = models.BooleanField(default=True, help_text="DOUBLE CHECK THIS")
    week_number = models.PositiveIntegerField(default=1)
    game_number = models.PositiveIntegerField(help_text="In BoX series, it's game number. Otherwise, game number for a given week")
    match_time = models.DateTimeField(help_text='Put in your timezone')
    
    blue_top_laner = models.CharField(max_length=32, blank=True, null=True)
    blue_jungler = models.CharField(max_length=32, blank=True, null=True)
    blue_mid_laner = models.CharField(max_length=32, blank=True, null=True)
    blue_ad_carry = models.CharField(max_length=32, blank=True, null=True)
    blue_support = models.CharField(max_length=32, blank=True, null=True)

    red_top_laner = models.CharField(max_length=32, blank=True, null=True)
    red_jungler = models.CharField(max_length=32, blank=True, null=True)
    red_mid_laner = models.CharField(max_length=32, blank=True, null=True)
    red_ad_carry = models.CharField(max_length=32, blank=True, null=True)
    red_support = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    class Meta:
        unique_together = ('blue_team','red_team','match_time')
        db_table = "A Single Match"
        abstract = True

class Baron_Match_Report(Report_Match):
    # Team+Player Fields
    #region
    blue_team = models.ForeignKey(
        Baron_League_Rosters,
        on_delete=models.CASCADE,
        related_name="blue_team",
        blank=True, null=True
        )
    red_team = models.ForeignKey(
        Baron_League_Rosters,
        on_delete=models.CASCADE,
        related_name="red_team",
        blank=True, null=True
        )
    
    blue_top_laner = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="blue_top_laner",
        blank=True, null=True
        )
    blue_jungler = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="blue_jungler",
        blank=True, null=True
        )
    blue_mid_laner = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="blue_mid_laner",
        blank=True, null=True
        )
    blue_ad_carry = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="blue_ad_carry",
        blank=True, null=True
        )
    blue_support = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="blue_support",
        blank=True, null=True
        )


    red_top_laner = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="red_top_laner",
        blank=True, null=True
        )
    red_jungler = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="red_jungler",
        blank=True, null=True
        )
    red_mid_laner = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="red_mid_laner",
        blank=True, null=True
        )
    red_ad_carry = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="red_ad_carry",
        blank=True, null=True
        )
    red_support = models.ForeignKey(
        Baron_Players,
        on_delete=models.CASCADE,
        related_name="red_support",
        blank=True, null=True
        )
    #endregion

    def save(self, *args, **kwargs):    # Get team stats here
        super(Baron_Match_Report, self).save(*args, **kwargs)
        '''         #THIS FUCKER RUINS FOREIGN KEY SHIT UGH
        if self.did_blue_win:
            self.blue_team.wins += 1
            self.red_team.losses += 1
        else:
            self.blue_team.losses += 1
            self.red_team.wins += 1

        self.blue_team.save(*args, **kwargs)
        self.red_team.save(*args, **kwargs)
        '''

    class Meta:
        unique_together = ('blue_team','red_team','match_time')
        db_table = "Baron Match Report"
        verbose_name_plural = "Baron Match Reports"

#endregion

# Global League Tracking Table
# Once created, will create matches that link back to this creation.
# Will pull all active rosters in a League
common_weeks = ((5,5),(9,9))
series_choices = ((1,'Bo1'),(2,'Bo2'),(3,'Bo3'))

class Start_League(models.Model):
    league_name = models.CharField(max_length=50, default='Dragon League X')
    league = models.CharField(max_length=50, choices=Leagues)
    start_date = models.DateTimeField()
    week_length = models.PositiveIntegerField(default=9, choices=common_weeks)
    regular_season_schedule = models.PositiveIntegerField(default=1, choices=series_choices)
    number_of_teams = models.PositiveIntegerField(default=10, help_text='This is always assumed to be 10')
    pools = models.PositiveIntegerField(default=1, help_text='In case we got multiple Elder Leagues again')
    
    # Constants used to create schedules
    teams = [0,1,2,3,4,5,6,7,8,9] 
    # ["Team 1","Team 2", "Team 3", "Team 4", "Team 5", "Team 6", "Team 7", "Team 8", "Team 9", "Team 10"]
    
    def __str__(self):
        return self.league_name

    def get_League(self):
        self.league_instance = None
        self.match_report_instance = None
        self.team = None
        if self.league == 'Dragon':
            pass
            #self.league_instance = Dragon_League
        elif self.league == 'Elder':
            pass
            #self.league_instance = Elder_League
        elif self.league == 'Baron':
            self.league_instance = Baron_League_Rosters.objects.filter(is_active=True)
            self.match_report_instance = Baron_Match_Report
        #self.team = models.ForeignKey(self.temp_value, on_delete=models.CASCADE, related_name='rosters', limit_choices_to={'is_active': True})
        #self.match_report = models.ForeignKey(self.temp_value, on_delete=models.CASCADE, related_name='match_report')
        print(self.start_date, type(self.start_date))

    def check_for_bye(self, list):  # Only need this for stand-alone testing
        if len(list) % 2 == 1:
            list += ['BYE']
        return list

    def create_round_robin(self, list):
        s = []

        new_list = list #self.check_for_bye(list)

        for i in range(len(new_list)-1):
            mid = int(len(new_list) / 2)
            l1 = new_list[:mid]
            l2 = new_list[mid:]
            l2.reverse()

            # Switch sides after each round
            week_list = []
            for j in range(mid):
                if(i % 2 == 1):
                    week_list += [(l1[j],l2[j])]
                else:
                    week_list += [(l2[j],l1[j])]
            # Conduct a pop
            tmp = new_list[len(new_list)-1]
            new_list =  new_list[:len(new_list)-1]
            # Conduct an insert
            new_list = [new_list[0]] + [tmp] + new_list[1:]
            #new_list.insert(1, new_list.pop())
            s += [week_list]
        return s

    def create_double_round_robin(self, round_robin_list):
        new_list = []
        for round in round_robin_list:
            week_list = []
            for match in round:
                week_list += [(match[1],match[0])]
            new_list += [week_list]
        return round_robin_list + new_list
    
    def check_league_for_teams(self):   # Check to ensure enough active rosters exist
        if len(self.league_instance) == number_of_teams:
            return True
        else:
            print('Wrong number of teams')
            raise Http404('Bad number of rosters already present')
            return False

    def create_league(self):
        self.team_list = self.league_instance
        round_robin_list = self.create_round_robin(self.team_list)
        double_round_robin = self.create_double_round_robin(round_robin_list)
        time_delta = datetime.timedelta(hours=1)
        game = 0
        week = 0
        first_game_tonight = False  # Check below will flip it back for first game
        if self.week_length is 9: # 9-week schedule
            if self.regular_season_schedule is 1:   #Bo1, round robin, two games a night
                for round in double_round_robin:
                    game = 1
                    if first_game_tonight:
                        first_game_tonight = False
                    else:
                        week += 1
                        first_game_tonight = True
                    print('------------')
                    for match in round:
                        #print('Match', match)
                        day_delta = datetime.timedelta(days=7*(week-1))
                        new_time = None
                        if first_game_tonight == False:
                            new_time = self.start_date + day_delta + time_delta
                        else:
                            new_time = self.start_date + day_delta
                        
                        self.match_report_instance.objects.create(
                            blue_team=match[0],
                            red_team=match[1], 
                            week_number=week,
                            game_number=game,
                            match_time=new_time
                            )
                        print('new self time',new_time)
                        print('old self time', self.start_date)
                return 0
            else:   # 9-week schedule with Bo2/Bo3 in single round robin
                for round in round_robin_list:
                    week += 1
                    for match in round:
                        game = 1
                        day_delta = datetime.timedelta(days=7*(week-1))
                        self.match_report_instance.objects.create(
                            blue_team=match[0],
                            red_team=match[1], 
                            week_number=week,
                            game_number=game,
                            match_time=(self.start_date + day_delta)
                            )

                        # Do second for 2nd game in Bo2
                        self.match_report_instance.objects.create(
                            blue_team=match[1],
                            red_team=match[0], 
                            week_number=week,
                            game_number=game+1,
                            match_time=(self.start_date + day_delta + time_delta)
                            )
                        if self.regular_season_schedule is 3:   # it's Bo3
                            # Blue/Red side evennness already done when creating the initial round-robin.
                            self.match_report_instance.objects.create(
                                blue_team=match[0],
                                red_team=match[1], 
                                week_number=week,
                                game_number=game+2,
                                match_time=(self.start_date + day_delta + time_delta*2)
                                )
                return 0
        elif self.week_length is 5: # Shortened 5-week schedule, single round robin
            return 0

    def save(self, *args, **kwargs):
        self.get_League()
        self.create_league()
        super(Start_League, self).save(*args, **kwargs)

    class Meta:
        db_table = "Start League"
        verbose_name_plural = "Start League"


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
