"""dfs_site_data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from data.views import DfsSiteViewSet, SportViewSet, LeagueViewSet, TeamViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'sites', DfsSiteViewSet, base_name='sites')
router.register(r'sports', SportViewSet, base_name='sites')
router.register(r'leagues', LeagueViewSet, base_name='leagues')
router.register(r'teams', TeamViewSet, base_name='teams')


urlpatterns = [
    url(r'^', include(router.urls)),
]