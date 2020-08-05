import os
import subprocess
import logging

logger = logging.getLogger(__name__)

envs_which_should_pass_value = [
        'ALIYUN_ACCESSKEYID', 'ALIYUN_ACCESSSECRET', 'ALIYUN_REGIONID',
        'INSTANCE_NAME', 'SUBDOMAIN', 'MAINDOMAIN',
        'SSH_USER']

# ('<accessKeyId>', '<accessSecret>', '<region-Id>')
ALIYUN_ACCESSKEYID = os.environ.get('ALIYUN_ACCESSKEYID')
ALIYUN_ACCESSSECRET = os.environ.get('ALIYUN_ACCESSSECRET')
ALIYUN_REGIONID = os.environ.get('ALIYUN_REGIONID')

# INSTANCE NAME
INSTANCE_NAME = os.environ.get('INSTANCE_NAME')


# DOMAIN
SUBDOMAIN = os.environ.get('SUBDOMAIN')
MAINDOMAIN = os.environ.get('MAINDOMAIN')


# max idle time
MAX_IDLE_TIME = int(os.environ.get('MAX_IDLE_TIME', '3600'))


# ssh related
SSH_USER = os.environ.get('SSH_USER')
SSH_IDENTITY = os.environ.get('SSH_IDENTITY', '/root/.ssh/id_rsa')
SSH_HOST = os.environ.get('SSH_HOST')


def config_init():
    all_passes = 1;
    for env_name in envs_which_should_pass_value:
        if os.environ.get(env_name) is None:
            all_passes = 0
            logger.error(f"env({env_name}) doesn't pass value, please check that.")

    if not (os.path.exists(SSH_IDENTITY) and os.path.isfile(SSH_IDENTITY)
            and os.access(SSH_IDENTITY, os.R_OK)):
        all_passes = 0
        logger.error(f"file({SSH_IDENTITY}) doesn't exit or is not a regular readable file.")

    if MAX_IDLE_TIME < 60 or MAX_IDLE_TIME > 86400:
        all_passes = 0
        logger.error(f"MAX_IDLE_TIME({MAX_IDLE_TIME}) should be a value in [60,86400]")

    global SSH_HOST
    if SSH_HOST is None:
        SSH_HOST = subprocess.check_output(
                'ip route show | awk \'/default/ {print $3}\'', shell=True, text=True).strip()
        logger.info(f"Got SSH_HOST({SSH_HOST})")


    return all_passes

