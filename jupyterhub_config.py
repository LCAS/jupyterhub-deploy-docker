# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

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
c.DockerSpawner.volumes = { 'k8s-jupyterhub-user-{username}': notebook_dir, 'k8s-jupyterhub-shared': /shared }
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

c.DockerSpawner.environment = {
    'GRANT_SUDO': '1',
}

# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'k8s-hub'
c.JupyterHub.hub_port = 8080

# TLS config
c.JupyterHub.port = 443
c.JupyterHub.ssl_key = os.environ['SSL_KEY']
c.JupyterHub.ssl_cert = os.environ['SSL_CERT']


# from oauthenticator.generic import LocalGenericOAuthenticator
# c.JupyterHub.authenticator_class = LocalGenericOAuthenticator
# c.OAuthenticator.client_id = os.environ['OPENIDC_CLIENT_ID']
# c.OAuthenticator.client_secret = os.environ['OPENIDC_CLIENT_SECRET']
# c.LocalGenericOAuthenticator.token_url = os.environ['OAUTH2_TOKEN_URL']
# c.LocalGenericOAuthenticator.userdata_url = os.environ['OAUTH2_USERDATA_URL']
# c.LocalGenericOAuthenticator.userdata_method = 'GET'
# c.LocalGenericOAuthenticator.userdata_params = {"state": "state"}
# c.LocalGenericOAuthenticator.username_key = "preferred_username"
# c.LocalAuthenticator.create_system_users = True


#################

# Enable the authenticator
c.JupyterHub.authenticator_class = 'keycloakauthenticator.KeyCloakAuthenticator'
c.KeyCloakAuthenticator.username_key = 'preferred_username'
c.KeyCloakAuthenticator.logout_redirect_uri = 'https://lcas.lincoln.ac.uk'
c.KeyCloakAuthenticator.oauth_callback_url = 'https://jupyterhub.lar.lincoln.ac.uk/hub/oauth_callback'

# Specify the issuer url, to get all the endpoints automatically from .well-known/openid-configuration
c.KeyCloakAuthenticator.oidc_issuer = 'https://sso.lar.lincoln.ac.uk/auth/realms/lar'

# If you need to set a different scope, like adding the offline option for longer lived refresh token
c.KeyCloakAuthenticator.scope = ['openid']
# Only allow users with this specific roles (none, to allow all)
c.KeyCloakAuthenticator.allowed_roles = ['socs-role', 'liat-role']
# Specify the role to set a user as admin
c.KeyCloakAuthenticator.admin_role = 'admin'

# If you have the roles in a non default place inside the user token, you can retrieve them
# This must return a set
def claim_roles_key(env, token):
    return set(token.get('roles', []))
c.KeyCloakAuthenticator.claim_roles_key = claim_roles_key

# Request access tokens for other services by passing their id's (this uses the token exchange mechanism)
#c.KeyCloakAuthenticator.exchange_tokens = ['eos-service', 'cernbox-service']

# If your authenticator needs extra configurations, set them in the pre-spawn hook
# def pre_spawn_hook(authenticator, spawner, auth_state):
#     spawner.environment['ACCESS_TOKEN'] = auth_state['exchanged_tokens']['eos-service']
#     spawner.environment['OAUTH_INSPECTION_ENDPOINT'] = authenticator.userdata_url.replace('https://', '')
#     spawner.user_roles = authenticator.get_roles_for_token(auth_state['access_token'])
#     spawner.user_uid = auth_state['oauth_user']['cern_uid']
# c.KeyCloakAuthenticator.pre_spawn_hook = pre_spawn_hook

#Configure token signature verification
c.KeyCloakAuthenticator.check_signature=True
c.KeyCloakAuthenticator.jwt_signing_algorithms = ["HS256", "RS256"]


c.LocalAuthenticator.create_system_users = True


#####################




# Authenticate users with GitHub OAuth
#c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
#c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB'],
)

# Whitlelist users and admins
#c.Authenticator.whitelist = whitelist = set()
#c.Authenticator.admin_users = admin = set()
c.JupyterHub.admin_access = True
# pwd = os.path.dirname(__file__)
# with open(os.path.join(pwd, 'userlist')) as f:
#     for line in f:
#         if not line:
#             continue
#         parts = line.split()
#         # in case of newline at the end of userlist file
#         if len(parts) >= 1:
#             name = parts[0]
#             whitelist.add(name)
#             if len(parts) > 1 and parts[1] == 'admin':
#                 admin.add(name)
