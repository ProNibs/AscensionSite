"""
Definition of urls for AscnesionESports.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import AscensionESports_Baseline.forms
import AscensionESports_Baseline.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', AscensionESports_Baseline.views.home, name='home'),
    url(r'^Contact$', AscensionESports_Baseline.views.contact, name='contact'),
    url(r'^About$', AscensionESports_Baseline.views.about, name='about'),
    url(r'^Dragon League$', AscensionESports_Baseline.views.dragon, name='dragon'),
    url(r'^Elder League$', AscensionESports_Baseline.views.elder, name='elder'),
    url(r'^Baron League$', AscensionESports_Baseline.views.baron, name='baron'),
    url(r'^Dragon/News$', AscensionESports_Baseline.views.dragon_news, name='dragon_news'),
    url(r'^Elder/News$', AscensionESports_Baseline.views.elder_news, name='elder_news'),
    url(r'^Baron/News$', AscensionESports_Baseline.views.baron_news, name='baron_news'),
    url(r'^Sign-Ups/Dragon/$', AscensionESports_Baseline.views.dragon_league_sign_ups, name='dragon_league_sign_ups'),
    url(r'^Sign-Ups/Elder/Solo/$', AscensionESports_Baseline.views.elder_league_solo_sign_ups, name='elder_solo_league_sign_ups'),
    url(r'^Sign-Ups/Elder/Team/$', AscensionESports_Baseline.views.elder_league_team_sign_ups, name='elder_team_league_sign_ups'),
    url(r'^Sign-Ups/Baron$', AscensionESports_Baseline.views.baron_league_sign_ups, name='baron_league_sign_ups'),
    url(r'^Sign-Ups$', AscensionESports_Baseline.views.league_sign_ups, name='league_sign_ups'),
    url(r'^Thanks$', AscensionESports_Baseline.views.thanks, name='thanks'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'AscensionESports_Baseline/login.html',
            'authentication_form': AscensionESports_Baseline.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'template_name': 'AscensionESports_Baseline/logoff.html',
            #'next_page': '/',
        },
        name='logout'),


    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^AEadmin/', include(admin.site.urls)),
]

