#!/usr/bin/env python
from fabric.api import *
from fabric.decorators import runs_once

import os

fabfile_dir = os.path.dirname(__file__)


# Fill out USER and HOSTS configuration before running
env.user = ''
env.hosts = ['']

env.code_dir = '/home/%s/GitHub/ex2' % (env.user)
env.virtualenv = '/home/%s/GitHub' % (env.user)



def update_theme():
    theme_dir = os.path.join(fabfile_dir, 'readthedocs', 'templates', 'sphinx')
    if not os.path.exists('/tmp/sphinx_rtd_theme'):
        local('git clone https://github.com/snide/sphinx_rtd_theme.git /tmp/sphinx_rtd_theme')
    with lcd('/tmp/sphinx_rtd_theme'):
        local('git remote update')
        local('git reset --hard origin/master ')
        local('cp -r /tmp/sphinx_rtd_theme/sphinx_rtd_theme %s' % theme_dir)
        local('cp -r /tmp/sphinx_rtd_theme/sphinx_rtd_theme/static/fonts/ %s' % os.path.join(fabfile_dir, 'media', 'font'))
        local('cp /tmp/sphinx_rtd_theme/sphinx_rtd_theme/static/css/badge_only.css %s' % os.path.join(fabfile_dir, 'media', 'css'))
        local('cp /tmp/sphinx_rtd_theme/sphinx_rtd_theme/static/css/theme.css %s' %
              os.path.join(fabfile_dir, 'media', 'css', 'sphinx_rtd_theme.css'))


def i18n():
    with lcd('readthedocs'):
        local('rm -rf rtd_tests/tests/builds/')
        local('tx pull')
        local('./manage.py makemessages --all')
        #local('tx push -s')
        local('./manage.py compilemessages')


def i18n_docs():
    with lcd('docs'):
        # Update our tanslations
        local('tx pull -a')
        local('sphinx-intl build')
        # Push new ones
        local('make gettext')
        local('tx push -s')


@runs_once
def spider():
    local('patu.py -d1 readthedocs.org')



#--------------------------------------------------------------#
#Ab hier selbst geschriebene F'n

#Beispiel "Hello World/Name!"
#Ausgabe mit fab hello oder fab hello:name
def hello(name="world"):
    print('Hello %s!' % name)

#uptime
def uptime():
  local('uptime')

#push
def push():
    "Push new code, but don't restart/reload."
    local('git push ex2')
    with cd(env.code_dir):
        run('git pull ex2')
    

