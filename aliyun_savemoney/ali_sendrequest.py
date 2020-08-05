#  coding=utf-8
# if the python sdk is not install using 'sudo pip install aliyun-python-sdk-ecs'
# if the python sdk is install using 'sudo pip install --upgrade aliyun-python-sdk-ecs'
# make sure the sdk version is greater than 2.1.2, you can use command 'pip show aliyun-python-sdk-ecs' to check
import json
import logging
from aliyunsdkcore.client import AcsClient
import config

logger = logging.getLogger(__name__)

# send open api request
def sendrequest(request):
    #('<accessKeyId>', '<accessSecret>', '<region-Id>')
    client = AcsClient(
       config.ALIYUN_ACCESSKEYID,
       config.ALIYUN_ACCESSSECRET,
       config.ALIYUN_REGIONID
       )

    request.set_accept_format('json')
    try:
        response_str = client.do_action_with_exception(request)
        logger.info(response_str)
        response_detail = json.loads(str(response_str, encoding='utf-8'))
        return response_detail
    except Exception as e:
        logger.error(e)
        return None

