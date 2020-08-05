import time
import os
import logging
import ali_dns
import ali_instance
import config

logger = logging.getLogger(__name__)

def update_domain_A_record():
    public_ips = ali_instance.get_instance_public_ips(config.INSTANCE_NAME)
    if public_ips is  None or not public_ips:
        logger.error("failed to get instance({config.INSTANCE_NAME}) public IP.")
        return None

    if len(public_ips) > 1:
        logger.warn(f"too many A record found for instance({config.INSTANCE_NAME})."
                f"We will use the first one:({public_ips[0]})")

    result = ali_dns.update_doamin_record_byname(config.SUBDOMAIN, config.MAINDOMAIN, 'A', public_ips[0])
    if result is None or not result:
        logger.error(f"something error encountered when trying to update "
                f"domain({config.SUBDOMAIN}.{config.MAINDOMAIN}) A recore value ({public_ips[0]})")
        return None

    logger.info(f"successfully update domain({config.SUBDOMAIN}.{config.MAINDOMAIN}) A recore value ({public_ips[0]})")

    return True


def get_current_login_user():
    current_users = 0
    with os.popen(f"ssh -i {config.SSH_IDENTITY} -l {config.SSH_USER} -o ConnectTimeout=30 -o StrictHostKeyChecking=no {config.SSH_HOST} last | grep 'still logged in'") as f:
        while True:
            u = f.readline()
            if u:
                logger.info(f"current user: {u}")
                current_users += 1
            else:
                break

    if current_users:
        logger.info(f"there are {current_users} alive")
    else:
        logger.info(f"no user alive now!")

    return current_users


def main():
    logging.basicConfig(level=logging.INFO,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a %d %b %Y %H:%M:%S')

    if not config.config_init():
        logger.fatal("config init failed , please check above log and rerun again")
        time.sleep(10)
        return -1

    while True:
        try:
            result = update_domain_A_record()
            if result:
                break
            else:
                time.sleep(10)
        except Exception as ex:
            logger.fatal(ex)
            time.sleep(10)

    user_alive_time = time.time()
    str_user_alive_time = time.asctime()
    while True:
        try:
            cnt = get_current_login_user()
            if cnt is None or cnt > 0:
                user_alive_time = time.time()
                str_user_alive_time = time.asctime()

            if user_alive_time + config.MAX_IDLE_TIME < time.time():
                logger.info(f"idle time({config.MAX_IDLE_TIME}) reached since last user login time is "
                        f"({str_user_alive_time}).We'll close the instance by name ({config.INSTANCE_NAME})")
                ali_instance.stop_instance_by_name(config.INSTANCE_NAME)
                break
            else:
                time.sleep(60)
        except Exception as ex:
            logger.fatal(ex)
            time.sleep(60)

    while True:
        logger.info("waiting server to die...")
        time.sleep(60)

if __name__ == '__main__':
    main()
