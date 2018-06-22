"""
Definition of views.
"""
import json
import urllib

from django.conf import settings
from django.contrib import messages
from django import forms

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from AscensionESports_Baseline.models import Dragon_League, Elder_League, Baron_League
from AscensionESports_Baseline.models import Dragon_Post, Elder_Post, Baron_Post

from django.http import HttpResponseRedirect

from .forms import (
    Dragon_League_Signup_Form, Elder_League_Solo_Signup_Form, Elder_League_Team_Signup_Form, Baron_League_Signup_Form
    )

from datetime import datetime

def Dragon_League_Request(request):
    league_sheet = Dragon_League.objects.all()
    return league_sheet

def Elder_League_Request(request):
    league_sheet = Elder_League.objects.all()
    return league_sheet

def Baron_League_Request(request):
    league_sheet = Baron_League.objects.all()
    return league_sheet



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
            return render(
                        request, 
                        'AscensionESports_Baseline/thanks.html', 
                        {
                            'background': getDragonBackground(),
                            'color': getDragonColor(),
                            'title': 'You have signed up for Dragon League!',
                            'year': datetime.now().year,
                        })

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
            return render(
                        request, 
                        'AscensionESports_Baseline/thanks.html', 
                        {
                            'background': getElderBackground(),
                            'color': getElderColor(),
                            'title': 'You have signed up alone for Elder League!',
                            'year': datetime.now().year,
                        })

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
            return render(
                        request, 
                        'AscensionESports_Baseline/thanks.html', 
                        {
                            'background': getElderBackground(),
                            'color': getElderColor(),
                            'title': 'You have signed your team up for Elder League!',
                            'year': datetime.now().year,
                        })

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
            return render(
                        request, 
                        'AscensionESports_Baseline/thanks.html', 
                        {
                            'background': getBaronBackground(),
                            'color': getBaronColor(),
                            'title': 'You have signed your team up for Baron League!',
                            'year': datetime.now().year,
                        })

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
        'AscensionESports_Baseline/thanks.html',
        {
            'background': getSiteBackground(),
            'color': getSiteColor(),
            'title':"Don't think you got here the correct way...",
            'year': datetime.now().year,
        }
    )