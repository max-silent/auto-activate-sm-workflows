import logging
import time

import pytest
from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.conftest import get_add_device_expected_responses
from automation_svc_ui.local_libs.login.web_ui_login import LoginHelper
from automation_svc_ui.tests.greenfield_existing_acct_new_devices.existing_acct_new_devices \
    .brnf_network_existing_acct_new_devices import WfExistingAcctNewDevices

expected_response_data = get_add_device_expected_responses()

log = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def brnf_autoclaim_order_iap_devices():
    """
    Create an IAP device
    :return: IAP device
    """
    device_type = "IAP"
    for i in range(2):
        create_test = WfExistingAcctNewDevices()
        aop_device_call = \
            create_test.existing_acct_create_device_of_type(device_type, end_username=create_test.pcid_name)
        if aop_device_call:
            return aop_device_call
        else:
            time.sleep(3)
    return False


@pytest.fixture(scope="session")
def brnf_sa_user_login_load_account():
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_username"]
    password = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_password"]
    pcid = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1"]
    url = hostname.split("//")[1]
    for i in range(2):
        try:
            ui_doorway_session = UIDoorway(url, username, password, pcid)
            if ui_doorway_session:
                return ui_doorway_session
        except Exception as ex:
            log.warning(f"Error appeared: '{ex}'")
        time.sleep(3)
    return False


@pytest.fixture(scope="session")
def logged_in_storage_state(brnf_sa_user_login_load_account, browser_instance):
    pcid_name = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1_name"]
    yield LoginHelper.wf_webui_login(brnf_sa_user_login_load_account,
                                     browser_instance,
                                     "brnf_logged_in_state.json",
                                     pcid_name)
