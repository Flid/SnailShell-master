from fabric.api import sudo, run

from snailshell_cp.management.cluster_control.utils import reset_docker
from .base import cp_task, copy_configs
from time import sleep
import logging
from django.conf import settings
from snailshell_cp.clients.portainer import PortainerClient

logger = logging.getLogger(__name__)


@cp_task
def provision_master_node():
    """
    Run on a main node once to set up all the services needed.
    WARNING: it wipes out everything, all unsaved data will be lost.
    """
    reset_docker()

    sudo('rm -rf /opt/portainer/')

    sudo(  # start Portainer
        f'docker run -d '
        f'-p {settings.PORTAINER_PORT}:9000 --restart always '
        f'-v /var/run/docker.sock:/var/run/docker.sock '
        f'-v /opt/portainer:/data '
        f'--name {settings.PORTAINER_DOCKER_CONTAINER_NAME} '
        f'{settings.PORTAINER_IMAGE_NAME}:{settings.PORTAINER_IMAGE_TAG}'
    )

    sleep(2)  # TODO

    logger.info('Initializing ')
    portainer_client = PortainerClient(settings.PORTAINER_EXTERNAL_URL)
    portainer_client.init_admin(
        settings.PORTAINER_ADMIN_USER,
        settings.PORTAINER_ADMIN_PASSWORD,
    )
    portainer_client.authenticate(
        settings.PORTAINER_ADMIN_USER,
        settings.PORTAINER_ADMIN_PASSWORD,
    )
    portainer_client.add_endpoint(
        settings.PORTAINER_LOCAL_ENDPOINT_NAME,
        settings.DOCKER_LOCAL_SOCKET_PATH,
    )

    # Postgres
    logger.info('Setting up Postgres...')
    portainer_client.create_image(
        settings.PORTAINER_LOCAL_ENDPOINT_ID,
        settings.POSTGRES_IMAGE_NAME,
        settings.POSTGRES_IMAGE_TAG,
    )
    portainer_client.create_container(
        settings.PORTAINER_LOCAL_ENDPOINT_ID,
        settings.POSTGRES_IMAGE_NAME,
        settings.POSTGRES_IMAGE_TAG,
        name=settings.POSTGRES_CONTAINER_NAME,
        request_data={
            'Env': copy_configs({
                'POSTGRES_USER': 'POSTGRES_USER',
                'POSTGRES_PASSWORD': 'POSTGRES_PASSWORD',
                'POSTGRES_DB': 'POSTGRES_DBNAME_CONTROL_PANEL',
            }),
            'PortBindings': {
                '5432/tcp': [{'HostPort': str(settings.POSTGRES_PORT)}],
            },
            'RestartPolicy': {'Name': 'unless-stopped'},
        }
    )
    portainer_client.start_container(
        settings.PORTAINER_LOCAL_ENDPOINT_ID,
        settings.POSTGRES_CONTAINER_NAME,
    )

    # RabbitMQ
    logger.info('Setting up RabbitMQ...')
    portainer_client.create_image(
        settings.PORTAINER_LOCAL_ENDPOINT_ID,
        settings.RABBITMQ_IMAGE_NAME,
        settings.RABBITMQ_IMAGE_TAG,
    )
    portainer_client.create_container(
        settings.PORTAINER_LOCAL_ENDPOINT_ID,
        settings.RABBITMQ_IMAGE_NAME,
        settings.RABBITMQ_IMAGE_TAG,
        name=settings.RABBITMQ_CONTAINER_NAME,
        request_data={
            'Env': copy_configs({
                'RABBITMQ_DEFAULT_USER': 'RABBITMQ_USER',
                'RABBITMQ_DEFAULT_PASS': 'RABBITMQ_PASSWORD',
            }),
            'PortBindings': {
                '5672/tcp': [{'HostPort': str(settings.RABBITMQ_PORT)}],
                '15672/tcp': [{'HostPort': str(settings.RABBITMQ_MANAGEMENT_PORT)}],
            },
            'RestartPolicy': {'Name': 'unless-stopped'},
        }
    )
    portainer_client.start_container(
        settings.PORTAINER_LOCAL_ENDPOINT_ID,
        settings.RABBITMQ_CONTAINER_NAME,
    )

    # Control panel
    # homedir = str(run('echo $HOME'))
    # sshdir = os.path.join(homedir, '.ssh')

    portainer_client.create_image(
        settings.PORTAINER_LOCAL_ENDPOINT_ID,
        settings.CONTROL_PANEL_IMAGE_NAME,
        settings.CONTROL_PANEL_IMAGE_TAG,
    )
    portainer_client.create_container(
        settings.PORTAINER_LOCAL_ENDPOINT_ID,
        settings.CONTROL_PANEL_IMAGE_NAME,
        settings.CONTROL_PANEL_IMAGE_TAG,
        name=settings.CONTROL_PANEL_CONTAINER_NAME,
        request_data={
            'Env': copy_configs({
                'POSTGRES_USER': 'POSTGRES_USER',
                'POSTGRES_PASSWORD': 'POSTGRES_PASSWORD',
                'POSTGRES_PORT': 'POSTGRES_PORT',
                'POSTGRES_DB': 'POSTGRES_DBNAME_CONTROL_PANEL',
                'RABBITMQ_USER': 'RABBITMQ_USER',
                'RABBITMQ_PASSWORD': 'RABBITMQ_PASSWORD',
                'RABBITMQ_PORT': 'RABBITMQ_PORT',
                'PORTAINER_ADMIN_USER': 'PORTAINER_ADMIN_USER',
                'PORTAINER_ADMIN_PASSWORD': 'PORTAINER_ADMIN_PASSWORD',
                'PORTAINER_EXTERNAL_URL': 'PORTAINER_EXTERNAL_URL',
                'PORTAINER_INTERNAL_URL': 'PORTAINER_INTERNAL_URL',
                'LOG_LEVEL': 'LOG_LEVEL',
                'SECRET_KEY': 'SECRET_KEY',
                'DEBUG': 'DEBUG',
                'MASTER_HOST': 'MASTER_HOST',
                'DOCKERD_API_PORT': 'DOCKERD_API_PORT',
                'CONTROL_PANEL_ADMIN_USER': 'CONTROL_PANEL_ADMIN_USER',
                'CONTROL_PANEL_ADMIN_PASSWORD': 'CONTROL_PANEL_ADMIN_PASSWORD',
                'CONTROL_PANEL_PORT': 'CONTROL_PANEL_PORT',
                'PORTAINER_LOCAL_ENDPOINT_NAME': 'PORTAINER_LOCAL_ENDPOINT_NAME',
                'PORTAINER_LOCAL_ENDPOINT_ID': 'PORTAINER_LOCAL_ENDPOINT_ID',
            }),
            'PortBindings': {
                f'8000/tcp': [{'HostPort': str(settings.CONTROL_PANEL_PORT)}],
            },
            # TODO In future we might want to share host ssh key
            # 'Volumes': {'/ssh-conf/': {}},
            # 'HostConfig': {
            #     'Binds': [
            #         f'{sshdir}:/ssh-conf/',
            #     ],
            # },
            'RestartPolicy': {'Name': 'unless-stopped'},
            'User': settings.CONTROL_PANEL_LINUX_USER,
        }
    )

    portainer_client.start_container(
        settings.PORTAINER_LOCAL_ENDPOINT_ID,
        settings.CONTROL_PANEL_CONTAINER_NAME,
    )
