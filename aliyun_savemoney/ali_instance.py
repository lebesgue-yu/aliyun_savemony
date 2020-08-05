import logging

from aliyunsdkecs.request.v20140526.StopInstanceRequest import StopInstanceRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

from ali_sendrequest import sendrequest

logger = logging.getLogger(__name__)

def get_instance_by_name(name):
    request_describe_instances = DescribeInstancesRequest()
    request_describe_instances.set_InstanceName(name)
    request_describe_instances.set_PageSize(100)

    response = sendrequest(request_describe_instances)
    if response is None:
        logger.error(f"Failed to get ECS by name({name}), please check above log")
        return None

    logger.info(f"Successfully get {response.get('TotalCount')} ECS(s) by name({name}).")

    #[{"ResourceGroupId":"","Memory":2048,"InstanceChargeType":"PostPaid","Cpu":2,"OSName":"CentOS  7.8 64位","InstanceNetworkType":"vpc","InnerIpAddress":{"IpAddress":[]},"ExpiredTime":"2099-12-31T15:59Z","ImageId":"centos_7_8_x64_20G_alibase_20200622.vhd","EipAddress":{"AllocationId":"","IpAddress":"","InternetChargeType":""},"HostName":"main","VlanId":"","Status":"Running","MetadataOptions":{"HttpTokens":"","HttpEndpoint":""},"InstanceId":"i-uf6ddw7sm2rjqzk6kt5a","StoppedMode":"Not-applicable","CpuOptions":{"ThreadsPerCore":2,"Numa":"ON","CoreCount":1},"StartTime":"2020-07-31T17:26Z","DeletionProtection":false,"SecurityGroupIds":{"SecurityGroupId":["sg-uf6isrfirr1cm5t11h81"]},"VpcAttributes":{"PrivateIpAddress":{"IpAddress":["192.168.7.1"]},"VpcId":"vpc-uf6o8756puxsi6yrtukv5","VSwitchId":"vsw-uf6eb8cjpyi92lzkx4il0","NatIpAddress":""},"InternetChargeType":"PayByBandwidth","InstanceName":"main","DeploymentSetId":"","InternetMaxBandwidthOut":1,"SerialNumber":"abe536e8-5d76-47ba-9f77-7ae1fc999660","OSType":"linux","CreationTime":"2020-07-13T05:45Z","AutoReleaseTime":"","Description":"","InstanceTypeFamily":"ecs.t6","DedicatedInstanceAttribute":{"Tenancy":"","Affinity":""},"PublicIpAddress":{"IpAddress":["106.14.188.212"]},"GPUSpec":"","NetworkInterfaces":{"NetworkInterface":[{"PrimaryIpAddress":"192.168.7.1","NetworkInterfaceId":"eni-uf6i39kqgewm4ud72b9g","MacAddress":"00:16:3e:10:9d:df"}]},"SpotPriceLimit":0.0,"DeviceAvailable":true,"SaleCycle":"","InstanceType":"ecs.t6-c1m1.large","OSNameEn":"CentOS  7.8 64 bit","SpotStrategy":"NoSpot","IoOptimized":true,"ZoneId":"cn-shanghai-g","ClusterId":"","EcsCapacityReservationAttr":{"CapacityReservationPreference":"","CapacityReservationId":""},"DedicatedHostAttribute":{"DedicatedHostId":"","DedicatedHostName":""},"GPUAmount":0,"OperationLocks":{"LockReason":[]},"InternetMaxBandwidthIn":80,"Recyclable":false,"RegionId":"cn-shanghai","CreditSpecification":"Standard"}]
    return response.get('Instances').get('Instance')

def stop_instance_by_name(name,DryRun=False):
    instance_list = get_instance_by_name(name)
    if instance_list is None:
        logger.error(f"failed to get instances list by name{name} when tring to stop them, please check that")
        return None

    for instance in instance_list:
        logger.info(f"Get instance: {instance}, trying to stop it.")
        stop_intance_result = stop_instance_by_id(instance.get('InstanceId'), DryRun)
        if stop_intance_result is None:
            logger.error(f"Failed to stop ECS by instanceid({instance.get('InstanceId')}), please check above log")
        else:
            logger.info(f"Stop ECS by instanceid({instance.get('InstanceId')}) successfully")

def stop_instance_by_id(instanceid, DryRun=False):
    request_stop_instance = StopInstanceRequest()
    request_stop_instance.set_InstanceId(instanceid)
    request_stop_instance.set_StoppedMode('StopCharging')
    request_stop_instance.set_ConfirmStop(False)
    request_stop_instance.set_ForceStop(False)
    request_stop_instance.set_DryRun(DryRun)
    return sendrequest(request_stop_instance)


def get_instance_public_ips(name):
    instance_list = get_instance_by_name(name)
    if instance_list is None:
        logger.error(f"failed to get instances list by name{name} when tring to get public ip, please check that")
        return None

    result = []
    for instance in instance_list:
        logger.info(f"Get instance: {instance}, trying to get its public ips")
        #PublicIpAddress = result['Instances']['Instance'][0]['PublicIpAddress']['IpAddress'][0]
        result.extend(instance.get('PublicIpAddress').get('IpAddress'))

    return result

