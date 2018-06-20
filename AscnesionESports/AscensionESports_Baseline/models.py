"""
Definition of models.
"""

from django.db import models

Positions = (('Top', 'Top'),('Jungle', 'Jungle'),('Mid', 'Mid'),('ADC', 'ADC'),('Support','Support'),('Substitute','Substitute'),
             ('Pending-Top','Pending-Top'), ('Pending-Jgl','Pending-Jgl'), ('Pending-Mid','Pending-Mid'),
             ('Pending-ADC','Pending-ADC'),('Pending-Sup','Pending-Sup'))

Roles = (('Top', 'Top'),('Jungle', 'Jungle'),('Mid', 'Mid'),('ADC', 'ADC'),('Support','Support'),('Fill','Fill'))

Leagues = (('Dragon', 'Dragon'),('Elder', 'Elder'),('Baron','Baron'))
# Create your models here.

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
    team_name = models.CharField(max_length=20)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)

    def __str__(self):
        return team_name
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
        verbose_name = "Dragon League"

class Dragon_Standings(A_Team):
    class Meta:
        db_table="Dragon League Standing"
        verbose_name = "Dragon League Standings"

class Dragon_Solo_Sign_Ups(Generic_Solo_Sign_Up):
    class Meta:
        db_table = "Dragon Solo Sign Up"
        verbose_name = "Dragon Solo Sign Ups"

class Elder_League(A_League):
    class Meta:
        db_table="Elder League"
        verbose_name = "Elder League"

class Elder_Standings(A_Team):
    class Meta:
        db_table="Elder League Standing"
        verbose_name = "Elder League Standings"

class Elder_Team_Sign_Ups(Generic_Team_Sign_Up):
    class Meta:
        db_table = "Elder Team Sign Up"
        verbose_name = "Elder Team Sign Ups"

class Elder_Solo_Sign_Ups(Generic_Solo_Sign_Up):
    class Meta:
        db_table = "Elder Solo Sign Up"
        verbose_name = "Elder Solo Sign Ups"

class Baron_League(A_League):
    class Meta:
        db_table="Baron League"
        verbose_name = "Baron League"

class Baron_Standings(A_Team):
    class Meta:
        db_table="Baron League Standing"
        verbose_name = "Baron League Standings"

class Baron_Team_Sign_Ups(Generic_Team_Sign_Up):
    class Meta:
        db_table = "Baron League Sign Up"
        verbose_name = "Baron Sign Ups"

 
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
        verbose_name = "Dragon News"

class Elder_Post(Post):
    class Meta:
        db_table = "Elder News"
        verbose_name = "Elder News"

class Baron_Post(Post):
    class Meta:
        db_table = "Baron News"
        verbose_name = "Baron News"