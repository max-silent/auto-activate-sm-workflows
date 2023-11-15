import logging

import pytest
from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.conftest import get_add_device_expected_responses
from automation_svc_ui.local_libs.login.web_ui_login import LoginHelper
from automation_svc_ui.local_libs.ui_doorway.ui_doorway_devices_by_api import UiDoorwayDevices
from automation_svc_ui.local_libs.utils.decorators import retry_on_false, retry_until_condition
from automation_svc_ui.tests.greenfield_existing_acct_new_devices.existing_acct_new_devices \
    .brnf_network_existing_acct_new_devices import WfExistingAcctNewDevices

expected_response_data = get_add_device_expected_responses()

log = logging.getLogger(__name__)

create_test = WfExistingAcctNewDevices()


@pytest.fixture(scope="class")
def end_username_msp_alias(tac_user_login_load_account):
    yield create_test.end_username
    msp_pcid = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid"]
    UiDoorwayDevices.delete_alias(create_test.end_username, tac_user_login_load_account, msp_pcid)


@pytest.fixture(scope="class")
@retry_on_false()
def brnf_sa_order_iap_devices():
    """
    Create an IAP device
    :return: IAP device
    """
    device_type = "IAP"
    create_test = WfExistingAcctNewDevices()
    return create_test.existing_acct_create_device_of_type(device_type)


@pytest.fixture(scope="function")
def msp_iap_subscription(brnf_msp_user_login_load_account):
    subscriptions = brnf_msp_user_login_load_account.get_licenses()["subscriptions"]
    ap_subscriptions = list(filter(lambda subscr: "AP" in subscr["supported_device_types"], subscriptions))

    subscr_details = {}
    for subscr in ap_subscriptions:
        if subscr["available_quantity"] > 1:
            subscr_details["tier"] = subscr["subscription_tier_description"]
            subscr_details["key"] = subscr["subscription_key"]
            break
    else:
        log.error("There is lack of available AP Advanced subscriptions.")
    yield subscr_details


@pytest.fixture(scope="class")
@retry_on_false()
def brnf_msp_sa_order_iap_devices(end_username_msp_alias):
    """
    Create an IAP device
    :return: IAP device
    """
    device_type = "IAP"
    create_test = WfExistingAcctNewDevices()
    return create_test.existing_acct_create_device_of_type(device_type,
                                                           end_username=end_username_msp_alias)


@pytest.fixture(scope="class")
@retry_on_false()
def brnf_msp_sa_order_switch_devices(end_username_msp_alias):
    """
    Create an SWITCH device
    :return: SWITCH device
    """
    device_type = "SWITCH"
    create_test = WfExistingAcctNewDevices()
    return create_test.existing_acct_create_device_of_type(device_type,
                                                           end_username=end_username_msp_alias)


@pytest.fixture(scope="class")
@retry_on_false()
def brnf_msp_sa_order_cntrl_devices(end_username_msp_alias):
    """
    Create an CONTROLLER device
    :return: CONTROLLER device
    """
    device_type = "CONTROLLER"
    create_test = WfExistingAcctNewDevices()
    return create_test.existing_acct_create_device_of_type(device_type,
                                                           end_username=end_username_msp_alias)


@pytest.fixture(scope="class")
@retry_on_false()
def brnf_sa_order_sw_devices():
    device_type = "SWITCH"
    create_test = WfExistingAcctNewDevices()
    return create_test.existing_acct_create_device_of_type(device_type)


@pytest.fixture(scope="class")
@retry_on_false()
def brnf_sa_order_gw_devices():
    device_type = "GATEWAY"
    create_test = WfExistingAcctNewDevices()
    return create_test.existing_acct_create_device_of_type(device_type)


@pytest.fixture(scope="session")
def brnf_sa_user_login_load_account():
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_username"]
    password = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_password"]
    pcid = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1"]
    url = hostname.split("//")[1]
    return UIDoorway(url, username, password, pcid)


@pytest.fixture(scope="session")
def brnf_msp_user_login_load_account():
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["username"]
    password = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["password"]
    pcid = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid"]
    url = hostname.split("//")[1]
    return UIDoorway(url, username, password, pcid)


@pytest.fixture(scope="session")
def tac_user_login_load_account():
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data["tac_admin_username"]
    password = ExistingUserAcctDevices.test_data["tac_admin_password"]
    pcid = ExistingUserAcctDevices.test_data["tac_admin_pcid1"]
    url = hostname.split("//")[1]
    return UIDoorway(url, username, password, pcid)


@pytest.fixture()
@retry_until_condition(lambda resp: resp.status_code < 500)
def brnf_sa_iap_prov_msp(brnf_msp_sa_order_iap_devices):
    device_type = "IAP"
    return create_test.brnf_sa_nw_device_prov(brnf_msp_sa_order_iap_devices, device_type)


@pytest.fixture()
@retry_until_condition(lambda resp: resp.status_code < 500)
def brnf_sa_sw_prov_msp(brnf_msp_sa_order_switch_devices, api_path, x_type):
    device_type = "SWITCH"
    return create_test.brnf_sa_switch_device_prov(brnf_msp_sa_order_switch_devices,
                                                  device_type,
                                                  api_path,
                                                  x_type)


@pytest.fixture()
@retry_until_condition(lambda resp: resp.status_code < 500)
def brnf_sa_cntrl_prov_msp(brnf_msp_sa_order_cntrl_devices):
    device_type = "CONTROLLER"
    return create_test.brnf_sa_nw_device_prov(brnf_msp_sa_order_cntrl_devices,
                                              device_type)


@pytest.fixture(scope="session")
def msp_logged_in_storage_state(brnf_msp_user_login_load_account, browser_instance):
    pcid_name = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid_name"]
    yield LoginHelper.wf_webui_login(brnf_msp_user_login_load_account,
                                     browser_instance,
                                     "brnf_msp_logged_in_state.json",
                                     pcid_name=pcid_name)
