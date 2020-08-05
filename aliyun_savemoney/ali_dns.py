from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
import json
import sys
import logging
from ali_sendrequest import sendrequest

logger = logging.getLogger(__name__)

def get_domain_record_ids(subdomain, maindomain, querytype='A', searchmode='EXACT'):
    request_describeDomainRecord = DescribeDomainRecordsRequest()
    request_describeDomainRecord.set_DomainName(maindomain)
    request_describeDomainRecord.set_RRKeyWord(subdomain)
    request_describeDomainRecord.set_KeyWord(subdomain)
    request_describeDomainRecord.set_Type(querytype)
    request_describeDomainRecord.set_SearchMode(searchmode)

    logger.info(f"Trying to get {querytype} recored of domain: {subdomain}.{maindomain}, "
            f"with searchmode({searchmode})")
    response = sendrequest(request_describeDomainRecord)
    if response is None:
        logging.error(f"failed to get domain A record, see above log to check.")
        return None

    resultid =  []
    domainRecord_list = response.get('DomainRecords').get('Record')
    logger.info(f"Get domainRecordList successfully: ({domainRecord_list})")

    for domainRecord in domainRecord_list:
        resultid.append([domainRecord.get('RecordId'), domainRecord.get('Value')])
    return resultid

def update_domain_record_byid(subdomain, recordid, recordtype, recordvalue):
    request_updatednsaddr = UpdateDomainRecordRequest()
    request_updatednsaddr.set_RR(subdomain)
    request_updatednsaddr.set_RecordId(recordid)
    request_updatednsaddr.set_Type(recordtype)
    request_updatednsaddr.set_Value(recordvalue)

    logger.info(f"Trying to update subdomain({subdomain}) with type({recordtype}):value({recordvalue}) ")
    response = sendrequest(request_updatednsaddr)
    if response is None:
        logging.error(f"failed to update subdomain({subdomain}) with "
                f"type({recordtype}):value({recordvalue}). see above log to check.")
        return None

    logging.info(f"successfully update subdomain({subdomain}) with "
            f"type({recordtype}):value({recordvalue}).")
    return response

def update_doamin_record_byname(subdomain, maindomain, recordtype, recordvalue):
    recordid_list = get_domain_record_ids(subdomain, maindomain, recordtype, 'EXACT')
    if recordid_list is None:
        logging.error(f"failed to get recoredid in update_doamin_record_byname.")
        return None

    update_all_successful = True
    if recordvalue in [i[1] for i in recordid_list]:
        logging.info(f"value({recordvalue}) already exists int the value lists.")
        return update_all_successful 

    for rr_id, rr_value in recordid_list:
        update_single_result = update_domain_record_byid(subdomain, rr_id, recordtype, recordvalue)
        if update_single_result is None:
            update_all_successful = False

    return update_all_successful

