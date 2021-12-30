from fabric.api import *
from fabvenv import virtualenv
from os import path

env.user = 'ubuntu'
env.hosts = 'ijust.ir'
env.key_filename = '~/aminhp.pem'
home = '/var/www/ie/'
p2p = path.join(home, 'p2p_videochat/')
game = path.join(home, 'webSocket/')
p2p_venv = path.join(p2p, 'venv')
game_venv = path.join(game, 'venv')
logl = path.join(home, 'log/')


def pull(dest='game'):
    if dest == 'game':
        with cd(game):
            sudo('git pull origin master')
    else:
        with cd(p2p):
            sudo('git pull origin master')


def server_down(dest='game'):
    if dest == 'game':
        with cd(game, warn_only=True):
            with virtualenv(game_venv):
                sudo('screen -XS game quit')
    else:
        with cd(p2p, warn_only=True):
            with virtualenv(p2p_venv):
                sudo('screen -XS p2p quit')


def server_up(dest='game'):
    if dest == 'game':
        with cd(game):
            with virtualenv(game_venv):
                sudo('screen -RdmLS game python server.py')
    else:
        with cd(p2p):
            with virtualenv(p2p_venv):
                sudo('screen -dmLS p2p python server.py')


def deploy(dest='game'):
    pull(dest)
    try:
        server_down(dest)
    except Exception as err:
        pass
    server_up(dest)
