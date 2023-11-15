from automation_svc_ui.conftest import ExistingUserAcctDevices
from hpe_glcp_automation_lib.libs.commons.utils.humio.humio_utils import HumioClass
import logging
import time
import re
import json

log = logging.getLogger(__name__)

class HumioLogLocalHelper:

    def __init__(self):
        humio_base_url = ExistingUserAcctDevices.humio_url
        humio_repository = "ccsportal"
        humio_user_token = ExistingUserAcctDevices.test_data["humio_user_token"]
        humio_session = HumioClass(base_url=humio_base_url, repository=humio_repository, user_token=humio_user_token)
        self.humio_session = humio_session

    def get_subs_mgmt_event_transaction_id(self,
                                      search_query,
                                      search_duration_in_ms=3600000,
                                      timeout=10000):
        """
        search humio logs for event name and returns transactionId
        :param: search_query (example: serial_number AND kafka-producer-network-thread AND DEVICE_PROVISION_INTERNAL_EVENT)
        :param: search_duration_in_ms
        :param: timeout for the method
        :return: transaction_id
        """
        epoch_time = int(time.time() * 1000.0)
        current_time = int(time.time() * 1000.0)
        timeout_time = current_time + timeout
        try:
            while current_time < timeout_time:
                result = self.humio_session.create_queryjob(
                    search_query,
                    start=epoch_time - search_duration_in_ms,
                    end=epoch_time,
                    is_live=False)
                json_log = json.loads(result[0]['log'])
                log.info("logs found for search query {} : as:  {}".format(search_query, json_log))
                msg = json_log['message']
                log.info("msg found for search query {}".format(msg))
                match_id = re.search('(?<=transaction=)([^,]*)', msg)
                transaction_id = match_id.group(1)[:-1]
                if transaction_id:
                    log.info(f"Found logs in humio with transaction_id: '{transaction_id}'")
                    return transaction_id
                time.sleep(1)
                current_time = int(time.time() * 1000.0)
        except Exception as e:
            log.error("Not able to search for transaction id, error {}".format(e))
            return False

    def humio_query_logs(self,
                         search_string,
                         search_duration_in_ms=600000):
        """
        humio query logs for searching all logs for a string in given duration
        :param: search_string
        :search_duration_in_ms: time to search_string in past logs
        :return: boolean (True or False)
        """

        try:
            epoch_time = int(time.time() * 1000.0)
            result = self.humio_session.create_queryjob(
                search_string,
                start=epoch_time - search_duration_in_ms,
                end=epoch_time,
                is_live=False)
            log.info(result)
            return True
        except Exception as e:
            log.error("Not able to search for search the string, error {}".format(e))
            return False
