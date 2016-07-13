"""null URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
import app.storyboard.views

urlpatterns = [
    url(r'^$', app.storyboard.views.main),
    url(r'^insert/$', app.storyboard.views.insert_view),
    url(r'^insert/add/$', app.storyboard.views.insert),
    url(r'^novel/([^/]+)/$', app.storyboard.views.novel_view),
    url(r'^parallelstory/$', app.storyboard.views.get_parallel_story_json),
    url(r'^team/$', app.storyboard.views.team_view),
    url(r'^profile/([^/]+)/$', app.storyboard.views.profile_view),
    url(r'^test/$', app.storyboard.views.test_view),

]
