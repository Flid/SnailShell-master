import json
import logging
import os

from django.conf import settings
from fabric.api import local, sudo
from storm import Storm

from .base import cp_task

logger = logging.getLogger(__name__)
HOST_SSH_DIR = '/opt/snailshell_cp/.ssh'
HOST_PG_DIR = '/opt/snailshell_cp/pg'


def jdump(data):
    return json.dumps(data, indent=2)


@cp_task
def generate_local_ssh_key():
    os.makedirs(HOST_SSH_DIR, mode=0o660, exist_ok=True)
    local(f'chown 1000:1000 {HOST_SSH_DIR} -R')

    output_file = os.path.join(HOST_SSH_DIR, 'id_rsa')

    if os.path.exists(output_file):
        logger.info('Shh key already exists - skipping.')
        return

    local(f'ssh-keygen -t rsa -N "" -f {output_file}')


@cp_task
def add_ssh_host(*, name, host, port, login, password):
    storm_ = Storm()

    try:
        storm_.delete_entry(name)
    except ValueError:
        pass

    storm_.add_entry(
        name,
        host,
        login,
        port,
        id_file='',
        # With these options there will be no stupid interactive
        # questions on ssh key uploading.
        custom_options=[
            'StrictHostKeyChecking=no',
            'UserKnownHostsFile=/dev/null',
        ],
    )

    # TODO can be insecure. Copy the password to a local file
    # with 0600 permissions and use the file with `-f` option.
    local(f'sshpass -p {password} ssh-copy-id {name}')


def reset_docker(reinstall_docker=True, local_mode=False):
    executor = local if local_mode else sudo

    if reinstall_docker:
        executor(settings.ENV.CMD_UNINSTALL_DOCKER)
        executor(settings.ENV.CMD_INSTALL_DOCKER)

    if settings.ENV.DOCKERHUB_USER:
        executor(f'docker login -u {settings.ENV.DOCKERHUB_USER} -p {settings.ENV.DOCKERHUB_PASSWORD}')
    else:
        logger.info('Skipping dockerhub login, you need to manually do that')

    # Stop and remove all containers/images
    options = {'capture': True} if local_mode else {}
    containers_running = executor('docker ps -a -q', **options)

    if containers_running:
        containers_running = ' '.join(containers_running.split())
        executor(f'docker stop {containers_running}')
        executor(f'docker rm {containers_running}')

    executor('docker system prune -f')
