"""
Definition of views.
"""
from datetime import datetime

from django.conf import settings
from django import forms
from django.apps import apps

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

#from AscensionESports_Baseline.models import Dragon_League, Elder_League, Baron_League
from AscensionESports_Baseline.models import Dragon_Post, Elder_Post, Baron_Post
from AscensionESports_Baseline.models import Dragon_Players, Dragon_League_Rosters
from AscensionESports_Baseline.models import Elder_Players, Elder_League_Rosters
from AscensionESports_Baseline.models import Baron_Players, Baron_League_Rosters, Baron_Match_Report
from AscensionESports_Baseline.models import BadAccounts, Start_League

import json
from django.core.serializers.json import DjangoJSONEncoder

from .forms import (
    Dragon_League_Signup_Form, Elder_League_Solo_Signup_Form, Elder_League_Team_Signup_Form, Baron_League_Signup_Form
    )

from datetime import datetime

def Dragon_League_Request(request):
    league_sheet = Dragon_League_Rosters.objects.filter(is_active=True)
    return league_sheet

def Elder_League_Request(request):
    league_sheet = Elder_League_Rosters.objects.filter(is_active=True)
    return league_sheet

def Baron_League_Request(request):
    league_sheet = Baron_League_Rosters.objects.filter(is_active=True)
    return league_sheet

def Baron_Players_Request(request):
    players = Baron_Players.objects.all()
    return players

def Baron_Match_Report_Request(request):    # Need to give schedule html only the latest schedule, not everything
    start_league = Start_League.objects.filter(league='Baron')
    date = None
    for start_league_object in start_league:    # Assumption: A League won't overlap itself
        if (date == None) or (start_league_object.start_date >= date):
            date = start_league_object.start_date
    if date == None:    # In the case a League has never been started
        date = datetime.now()
    schedule = Baron_Match_Report.objects.filter(match_time__gte=date)
    return schedule

def Bad_Players_Request(request):
    names = BadAccounts.objects.all().values_list('summoner_name')
    return json.dumps(list(names), ensure_ascii=False, cls=DjangoJSONEncoder)


def getSiteBackground():
    return 'steelblue'

def getSiteColor():
    return 'white'

def getDragonBackground():
    return '#268B4C'

def getDragonColor():
    return 'white'

def getElderBackground():
    return '#A0410F'

def getElderColor():
    return 'white'

def getBaronBackground():
    return '#9370DB'

def getBaronColor():
    return 'white'

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'AscensionESports_Baseline/index.html',
        {
            'background': getSiteBackground(),
            'color': getSiteColor(),
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'AscensionESports_Baseline/contact.html',
        {
            'background': getSiteBackground(),
            'color': getSiteColor(),
            'title':'Contact Us',
            'message':'Feel free to contact us via any of the following platforms!',
            'year':datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'AscensionESports_Baseline/about.html',
        {
            'background': getSiteBackground(),
            'color': getSiteColor(),
            'title':'About Us',
            'year': datetime.now().year,
        }
    )

# News
#region
def dragon_news(request):
    all_posts = Dragon_Post.objects.all().order_by('-date')

    return render(
        request,
        'AscensionESports_Baseline/news.html', 
        {
            'background': getDragonBackground(),
            'color': getBaronColor(),
            'title': 'Dragon League News',
            'posts': all_posts,
            'year': datetime.now().year,
        }
    )

def elder_news(request):
    all_posts = Elder_Post.objects.all().order_by('-date')

    return render(
        request,
        'AscensionESports_Baseline/news.html', 
        {
            'background': getElderBackground(),
            'color': getElderColor(),
            'title': 'Elder League News',
            'posts': all_posts,
            'year': datetime.now().year,
        }
    )


def baron_news(request):
    all_posts = Baron_Post.objects.all().order_by('-date')

    return render(
        request,
        'AscensionESports_Baseline/news.html', 
        {
            'background': getBaronBackground(),
            'color': getBaronColor(),
            'title': 'Baron League News',
            'posts': all_posts,
            'year': datetime.now().year,
        }
    )
#endregion

def dragon(request):
    """Renders the Dragon League Roster page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'AscensionESports_Baseline/league_layout.html',
        {
            'background': getDragonBackground(),
            'color': getDragonColor(),
            'title':'Dragon League Rosters',
            'query_results': Dragon_League_Request(request),
            'year': datetime.now().year,
        }
    )

def elder(request):
    """Renders the Elder League Roster page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'AscensionESports_Baseline/league_layout.html',
        {
            'background': getElderBackground(),
            'color': getElderColor(),
            'title':'Elder League Rosters',
            'query_results': Elder_League_Request(request),
            'year': datetime.now().year,
        }
    )

def baron(request):
    """Renders the Baron League Roster page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'AscensionESports_Baseline/league_layout.html',
        {
            'background': getBaronBackground(),
            'color': getBaronColor(),
            'title':'Baron League Rosters',
            'query_results': Baron_League_Request(request),
            'year': datetime.now().year,
        }
    )

def baron_stats(request, name):
    """Renders the Player Stats page."""
    assert isinstance(request, HttpRequest)
    query = Baron_Players.objects.filter(summoner_name=name)
    
    return render(
        request,
        'AscensionESports_Baseline/player_stats.html',
        {
            'background': getBaronBackground(),
            'color': getBaronColor(),
            'title':'Baron League Stats',
            'query_results': query,
            'year': datetime.now().year,
        }
    )

def baron_schedule(request):
    """Renders the Baron League Roster page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'AscensionESports_Baseline/schedule.html',
        {
            'background': getBaronBackground(),
            'color': getBaronColor(),
            'title':'Baron League Schedule',
            'query_results': Baron_Match_Report_Request(request),
            'year': datetime.now().year,
        }
    )

# Sign Ups
#region
def dragon_league_sign_ups(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Dragon_League_Signup_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/Thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Dragon_League_Signup_Form()

    return render(
        request, 
        'AscensionESports_Baseline/sign_ups.html', 
        {
            'background': getDragonBackground(),
            'color': getDragonColor(),
            'title': 'Dragon League Sign Ups!',
            'form': form,
            'year': datetime.now().year,
        })

def elder_league_solo_sign_ups(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Elder_League_Solo_Signup_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/Thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Elder_League_Solo_Signup_Form()

    return render(
        request, 
        'AscensionESports_Baseline/sign_ups.html', 
        {
            'background': getElderBackground(),
            'color': getElderColor(),
            'title': 'Elder League Solo Sign Ups!',
            'form': form,
            'year': datetime.now().year,
        })
def elder_league_team_sign_ups(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Elder_League_Team_Signup_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/Thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Elder_League_Team_Signup_Form()

    return render(
        request, 
        'AscensionESports_Baseline/sign_ups.html', 
        {
            'background': getElderBackground(),
            'color': getElderColor(),
            'title': 'Elder League Team Sign Ups!',
            'form': form,
            'year': datetime.now().year,
        })
def baron_league_sign_ups(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Baron_League_Signup_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/Thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Baron_League_Signup_Form()

    return render(
        request, 
        'AscensionESports_Baseline/sign_ups.html', 
        {
            'background': getBaronBackground(),
            'color': getBaronColor(),
            'title': 'Baron League Sign Ups!',
            'form': form,
            'year': datetime.now().year,
        })

def thanks(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'AscensionESports_Baseline/Thanks.html',
        {
            'background': getSiteBackground(),
            'color': getSiteColor(),
            'title':"You are now signed up!",
            'year': datetime.now().year,
        }
    )

def league_sign_ups(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'AscensionESports_Baseline/central_league_sign_ups.html',
        {
            'background': getSiteBackground(),
            'color': getSiteColor(),
            'title':'How to Sign Up',
            'year': datetime.now().year,
        }
    )
#endregion

@login_required
def check_for_bad_accounts(request):
    """Renders the check for bad accounts page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'AscensionESports_Baseline/check_for_bad_accounts.html',
        {
            'background': getSiteBackground(),
            'color': getSiteColor(),
            'title':'Check for Bad Accounts',
            'query_results' : Bad_Players_Request(request), 
            'year': datetime.now().year,
        }
    )
