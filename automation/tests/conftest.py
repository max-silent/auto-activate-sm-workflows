import logging
import pytest
from hpe_glcp_automation_lib.libs.adi.app_api.adi_app_api import ActivateInventory
from hpe_glcp_automation_lib.libs.adi.app_api.app_api_helper import AdiAppApiHelper
from automation.local_libs.activate_inventory.verify_by_api import VerifyByApi

from automation.conftest import ExistingUserAcctDevices

log = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def adi_app_api_session():
    """
    Creating App API session for ADI
    """
    adi_app_api = ActivateInventory(
        host=ExistingUserAcctDevices.app_api_hostname,
        sso_host=ExistingUserAcctDevices.sso_hostname,
        client_id=ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_client_id"],
        client_secret=ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_client_secret"],
    )
    return adi_app_api

@pytest.fixture(scope="class")
def archive_network_device(adi_app_api_session, request) -> dict:
    """
    - Get network devices from list of devices.
    - pick one device.
    - Archive it.
    """
    pcid = request.param
    devices = VerifyByApi.get_all_network_devices_by_pcid(adi_app_api_session, pcid)
    device = devices[0]
    log.info(device)
    device["archive"] = True
    payload = {}
    payload["devices"] = [device]
    archive_response = adi_app_api_session.update_archive_status(pcid = pcid, devices = payload)
    log.info(archive_response)
    archive_devices_list = VerifyByApi.get_all_network_devices_by_pcid(adi_app_api_session, pcid, archived_only = "ARCHIVED_ONLY")
    for dev in archive_devices_list:
            if dev["serial_number"] == device["serial_number"]:
                log.info("Device found in list of archived devices.........")
                log.info(device)
                return device

    return {}


@pytest.fixture(scope="class")
def adi_app_api_helper():
    adi_app_api_helper = AdiAppApiHelper(
        host=ExistingUserAcctDevices.app_api_hostname,
        sso_host=ExistingUserAcctDevices.sso_hostname,
        client_id=ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_client_id"],
        client_secret=ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_client_secret"],
    )
    return adi_app_api_helper
