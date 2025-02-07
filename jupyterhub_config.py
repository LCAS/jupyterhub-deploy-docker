# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()


# eanble sharing https://jupyterhub.readthedocs.io/en/latest/reference/sharing.html#sharing-reference
c.JupyterHub.load_roles = [
    {
        "name": "user",
        "scopes": ["self", "shares!user", "read:users:name", "read:groups:name"],
    },
]


# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
c.DockerSpawner.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })

# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir, 'jupyterhub-shared': '/shared' }
# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# c.DockerSpawner.extra_create_kwargs.update({ 'runtime': 'nvidia' })
import docker

c.DockerSpawner.extra_host_config = {
    "device_requests": [
        docker.types.DeviceRequest(
            count=-1,
            capabilities=[["gpu"]],
        ),
    ],
}

c.DockerSpawner.mem_limit = '8G'
c.DockerSpawner.cpu_limit = 2

c.DockerSpawner.environment = {
    'GRANT_SUDO': '1',
}

# Remove containers once they are stopped
c.DockerSpawner.remove = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8080

c.JupyterHub.authenticator_class = "generic-oauth"

# Fill these in with your values
c.GenericOAuthenticator.oauth_callback_url = "https://jupyter.zrok.lcas.group/hub/oauth_callback"
c.GenericOAuthenticator.client_id = os.getenv("OAUTH_CLIENT_ID")
c.GenericOAuthenticator.client_secret = os.getenv("OAUTH_CLIENT_SECRET")


c.GenericOAuthenticator.login_service = "UoL" # Text of login button
c.GenericOAuthenticator.authorize_url = "https://lcas.lincoln.ac.uk/auth/realms/lcas/protocol/openid-connect/auth"
c.GenericOAuthenticator.token_url = "https://lcas.lincoln.ac.uk/auth/realms/lcas/protocol/openid-connect/token"
c.GenericOAuthenticator.scope = ["openid"]
c.GenericOAuthenticator.userdata_url = "https://lcas.lincoln.ac.uk/auth/realms/lcas/protocol/openid-connect/userinfo"
c.GenericOAuthenticator.username_claim = "preferred_username"
c.GenericOAuthenticator.allow_all = False
c.GenericOAuthenticator.allow_existing_users = True
c.GenericOAuthenticator.admin_users = {"mhanheide"}

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

c.JupyterHub.admin_access = True
