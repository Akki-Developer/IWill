"""iWill_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from psybot import views
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('chatBot_darkmode', views.chatBot_darkmode, name='chatBot_darkmode'),
    path('chatBot_lightmode', views.chatBot_lightmode, name='chatBot_lightmode'),
    # path('create_django_user', views.User.as_view(), name='user'),
    path('bot_api', views.botAPI.as_view(), name='botAPI'),
    path('chat_history', views.chathistory.as_view(), name='bothistory'),
    path('check_status', views.check_status.as_view(), name='check_status'),
    # path('recomd_exercise', views.recomd_exercise.as_view(), name='recomd_exercise'),
    # path('bot_restart', views.botrestart.as_view(), name='botrestart'),


    # url(r'^$', views.home, name='home'),
]
