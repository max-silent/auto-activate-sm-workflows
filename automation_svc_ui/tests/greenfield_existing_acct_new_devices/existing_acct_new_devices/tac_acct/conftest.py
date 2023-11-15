import logging
import time
from datetime import datetime

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
def brnf_sa_order_iap_devices():
    """
    Create an IAP device
    :return: IAP device
    """
    device_type = "IAP"
    for i in range(2):
        create_test = WfExistingAcctNewDevices()
        aop_device_call = create_test.existing_acct_create_device_of_type(device_type)
        if aop_device_call:
            return aop_device_call
        else:
            time.sleep(3)
    return False


@pytest.fixture(scope="class")
def brnf_sa_order_sw_devices():
    device_type = "SWITCH"
    for i in range(2):
        create_test = WfExistingAcctNewDevices()
        aop_device_call = \
            create_test.existing_acct_create_device_of_type(device_type)
        if aop_device_call:
            return aop_device_call
        else:
            time.sleep(3)
    return False


@pytest.fixture(scope="class")
def brnf_sa_order_gw_devices():
    device_type = "GATEWAY"
    for i in range(2):
        create_test = WfExistingAcctNewDevices()
        aop_device_call = \
            create_test.existing_acct_create_device_of_type(device_type)
        if aop_device_call:
            return aop_device_call
        else:
            time.sleep(3)
    return False


@pytest.fixture(scope="class")
def brnf_sa_iap_subscription(tac_user_login_load_account, brnf_sa_user_login_load_account):
    subscr_key = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_iap_lic_key"]
    subscr_details = {"tier": "Advanced AP",
                      "key": subscr_key}
    yield subscr_details

    for i in range(1, 3):
        try:
            subscr_current_expiration = \
                tac_user_login_load_account.get_cm_customer_subscriptions(subscription_key_pattern=subscr_key)[0][
                    "appointments"]["subscription_end"] // 1000
            subscr_target_expiration = int(datetime.today().timestamp()) + 2592000  # timestamp of month after today
            end_date_increment = subscr_target_expiration - subscr_current_expiration
            pcid = brnf_sa_user_login_load_account.pcid
            tac_user_login_load_account.update_cm_eval_subscription(pcid,
                                                                    subscr_key,
                                                                    end_date_incremental=end_date_increment)
            break
        except Exception as ex:
            log.error(f"Error '{type(ex)}' at teardown attempt '{i}' of 'brnf_sa_iap_subscription()' fixture: '{ex}'.")
            if i > 1:
                raise
            time.sleep(3)


@pytest.fixture(scope="class")
def brnf_sa_sw_subscription(tac_user_login_load_account, brnf_sa_user_login_load_account):
    subscr_key = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_sw_lic_key"]
    subscr_details = {"tier": "Advanced-Switch-62xx/29xx",
                      "key": subscr_key}
    yield subscr_details

    for i in range(1, 3):
        try:
            subscr_current_expiration = \
                tac_user_login_load_account.get_cm_customer_subscriptions(subscription_key_pattern=subscr_key)[0][
                    "appointments"]["subscription_end"] // 1000
            subscr_target_expiration = int(datetime.today().timestamp()) + 2592000  # timestamp of month after today
            end_date_increment = subscr_target_expiration - subscr_current_expiration
            pcid = brnf_sa_user_login_load_account.pcid
            tac_user_login_load_account.update_cm_eval_subscription(pcid,
                                                                    subscr_key,
                                                                    end_date_incremental=end_date_increment)
            break
        except Exception as ex:
            log.error(f"Error '{type(ex)}' at teardown attempt '{i}' of 'brnf_sa_sw_subscription()' fixture: '{ex}'.")
            if i > 1:
                raise
            time.sleep(3)


@pytest.fixture(scope="class")
def brnf_sa_gw_subscription(tac_user_login_load_account, brnf_sa_user_login_load_account):
    subscr_key = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_gw_lic_key"]
    subscr_details = {"tier": "Advanced-70xx/90xx",
                      "key": subscr_key}
    yield subscr_details

    for i in range(1, 3):
        try:
            subscr_current_expiration = \
                tac_user_login_load_account.get_cm_customer_subscriptions(subscription_key_pattern=subscr_key)[0][
                    "appointments"]["subscription_end"] // 1000
            subscr_target_expiration = int(datetime.today().timestamp()) + 2592000  # timestamp of month after today
            end_date_increment = subscr_target_expiration - subscr_current_expiration
            pcid = brnf_sa_user_login_load_account.pcid
            tac_user_login_load_account.update_cm_eval_subscription(pcid,
                                                                    subscr_key,
                                                                    end_date_incremental=end_date_increment)
            break
        except Exception as ex:
            log.error(f"Error '{type(ex)}' at teardown attempt '{i}' of 'brnf_sa_gw_subscription()' fixture: '{ex}'.")
            if i > 1:
                raise
            time.sleep(3)


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
def tac_user_login_load_account():
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data["tac_admin_username"]
    password = ExistingUserAcctDevices.test_data["tac_admin_password"]
    pcid = ExistingUserAcctDevices.test_data["tac_admin_pcid1"]
    url = hostname.split("//")[1]
    return UIDoorway(url, username, password, pcid)


@pytest.fixture(scope="session")
def logged_in_storage_state(brnf_sa_user_login_load_account, browser_instance):
    pcid_name = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1_name"]
    yield LoginHelper.wf_webui_login(brnf_sa_user_login_load_account,
                                     browser_instance,
                                     "brnf_logged_in_state.json",
                                     pcid_name)


@pytest.fixture(scope="session")
def tac_logged_in_storage_state(tac_user_login_load_account, browser_instance):
    create_test = WfExistingAcctNewDevices()
    yield create_test.tac_webui_login(tac_user_login_load_account, browser_instance)
