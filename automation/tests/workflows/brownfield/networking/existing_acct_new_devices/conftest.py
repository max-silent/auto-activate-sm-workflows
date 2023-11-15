import logging
import time
from datetime import datetime

import pytest
from hpe_glcp_automation_lib.libs.adi.app_api.adi_app_api import ActivateInventory
from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway

from automation.conftest import ExistingUserAcctDevices
from automation.conftest import get_add_device_expected_responses
from automation.local_libs.activate_orders.activate_orders_utils import ActivateOrdersHelper
from automation.local_libs.login.web_ui_login import LoginHelper
from automation.local_libs.ui_doorway.ui_doorway_devices_by_api import UiDoorwayDevices
from automation.tests.workflows.brownfield.networking.existing_acct_new_devices.brnf_network_existing_acct_new_devices \
    import WfExistingAcctNewDevices

expected_response_data = get_add_device_expected_responses()

log = logging.getLogger(__name__)

create_test = WfExistingAcctNewDevices()


@pytest.fixture(scope="class")
def end_username_msp_alias(tac_user_login_load_account):
    yield create_test.end_username
    msp_pcid = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid"]
    UiDoorwayDevices.delete_alias(create_test.end_username, tac_user_login_load_account, msp_pcid)


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
def brnf_autoclaim_order_iap_devices():
    """
    Create an IAP device
    :return: IAP device
    """
    device_type = "IAP"
    return create_test.existing_acct_create_device_of_type(device_type, end_username=create_test.pcid_name)


@pytest.fixture(scope="class")
def brnf_msp_sa_order_iap_devices(end_username_msp_alias):
    """
    Create an IAP device
    :return: IAP device
    """
    device_type = "IAP"
    return create_test.existing_acct_create_device_of_type(device_type, end_username=end_username_msp_alias)


@pytest.fixture(scope="class")
def brnf_msp_sa_order_switch_devices(end_username_msp_alias):
    """
    Create an SWITCH device
    :return: SWITCH device
    """
    device_type = "SWITCH"
    return create_test.existing_acct_create_device_of_type(device_type, end_username=end_username_msp_alias)


@pytest.fixture(scope="class")
def brnf_msp_sa_order_cntrl_devices(end_username_msp_alias):
    """
    Create an CONTROLLER device
    :return: CONTROLLER device
    """
    device_type = "CONTROLLER"
    return create_test.existing_acct_create_device_of_type(device_type, end_username=end_username_msp_alias)


@pytest.fixture(scope="class")
def brnf_sa_order_sw_devices():
    device_type = "SWITCH"
    return create_test.existing_acct_create_device_of_type(device_type)


@pytest.fixture(scope="class")
def brnf_sa_order_gw_devices():
    device_type = "GATEWAY"
    return create_test.existing_acct_create_device_of_type(device_type)


@pytest.fixture(scope="class")
def brnf_sa_order_cntrl_devices():
    device_type = "CONTROLLER"
    return create_test.existing_acct_create_device_of_type(device_type)


@pytest.fixture(scope="class")
def brnf_sa_iap_subscription(tac_user_login_load_account, brnf_sa_user_login_load_account):
    subscr_key = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_iap_lic_key"]
    subscr_details = {"tier": "Advanced AP",
                      "key": subscr_key}
    yield subscr_details

    subscr_current_expiration = \
        tac_user_login_load_account.get_cm_customer_subscriptions(subscription_key_pattern=subscr_key)[0][
            "appointments"]["subscription_end"] // 1000
    subscr_target_expiration = int(datetime.today().timestamp()) + 2592000  # timestamp of month after today
    end_date_increment = subscr_target_expiration - subscr_current_expiration
    pcid = brnf_sa_user_login_load_account.pcid
    tac_user_login_load_account.update_cm_eval_subscription(pcid, subscr_key, end_date_incremental=end_date_increment)


@pytest.fixture(scope="class")
def brnf_sa_sw_subscription(tac_user_login_load_account, brnf_sa_user_login_load_account):
    subscr_key = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_sw_lic_key"]
    subscr_details = {"tier": "Advanced-Switch-62xx/29xx",
                      "key": subscr_key}
    yield subscr_details

    subscr_current_expiration = \
        tac_user_login_load_account.get_cm_customer_subscriptions(subscription_key_pattern=subscr_key)[0][
            "appointments"]["subscription_end"] // 1000
    subscr_target_expiration = int(datetime.today().timestamp()) + 2592000  # timestamp of month after today
    end_date_increment = subscr_target_expiration - subscr_current_expiration
    pcid = brnf_sa_user_login_load_account.pcid
    tac_user_login_load_account.update_cm_eval_subscription(pcid, subscr_key, end_date_incremental=end_date_increment)


@pytest.fixture(scope="class")
def brnf_sa_gw_subscription(tac_user_login_load_account, brnf_sa_user_login_load_account):
    subscr_key = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_gw_lic_key"]
    subscr_details = {"tier": "Advanced-70xx/90xx",
                      "key": subscr_key}
    yield subscr_details

    subscr_current_expiration = \
        tac_user_login_load_account.get_cm_customer_subscriptions(subscription_key_pattern=subscr_key)[0][
            "appointments"]["subscription_end"] // 1000
    subscr_target_expiration = int(datetime.today().timestamp()) + 2592000  # timestamp of month after today
    end_date_increment = subscr_target_expiration - subscr_current_expiration
    pcid = brnf_sa_user_login_load_account.pcid
    tac_user_login_load_account.update_cm_eval_subscription(pcid, subscr_key, end_date_incremental=end_date_increment)


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


@pytest.fixture(scope="session")
def brnf_app_api_session():
    """
    ===== Creates an Authorization bearer token ======
    """
    app_api_session = ActivateInventory(
        host=ExistingUserAcctDevices.app_api_hostname,
        sso_host=ExistingUserAcctDevices.sso_hostname,
        client_id=ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_id"],
        client_secret=ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_secret"],
    )
    return app_api_session


@pytest.fixture(scope="class")
def brnf_sa_manual_claim_iap_device_app_api(brnf_sa_order_iap_devices, brnf_app_api_session):
    """
    Claim an IAP device using an app api into an existing customer account
    :param brnf_sa_order_iap_devices: IAP device
    :param brnf_app_api_session: Authorization bearer token
    :return: True is status is 200, else false
    """
    device_type = "IAP"
    return create_test.wf_existing_device_claim_with_app_api(
        device_type, brnf_sa_order_iap_devices, brnf_app_api_session
    )


@pytest.fixture(scope="class")
def brnf_sa_manual_claim_sw_device(
        brnf_sa_order_sw_devices, brnf_sa_user_login_load_account
):
    device_type = "SWITCH"
    return create_test.wf_existing_device_claim_app_assignment(
        device_type, brnf_sa_order_sw_devices, brnf_sa_user_login_load_account
    )


@pytest.fixture(scope="class")
def brnf_sa_manual_claim_gw_device(
        brnf_sa_order_gw_devices, brnf_sa_user_login_load_account
):
    device_type = "GATEWAY"
    return create_test.wf_existing_device_claim_app_assignment(
        device_type, brnf_sa_order_gw_devices, brnf_sa_user_login_load_account
    )


@pytest.fixture(scope="class")
def brnf_sa_manual_claim_contrl_device(
        brnf_sa_order_cntrl_devices, brnf_app_api_session, brnf_sa_user_login_load_account
):
    device_type = "CONTROLLER"
    if create_test.wf_existing_device_claim_with_app_api(
            device_type, brnf_sa_order_cntrl_devices, brnf_app_api_session
    ):
        return create_test.wf_new_device_app_assignment(device_type, [brnf_sa_order_cntrl_devices],
                                                        brnf_sa_user_login_load_account)
    return False


@pytest.fixture()
def brnf_sa_iap_firmware(brnf_sa_order_iap_devices, endpoint, x_type, fw_version):
    """
     Device firmware call for firmware checks, upgrade, base firmware version for IAP device
        :param brnf_sa_order_iap_devices: Newly created IAP device detiles
        :param endpoint: firmware endpoint for IAP device
        :param x_type: firmware request for firmware checks, upgrade, base firmware version for IAP device
        :param fw_version: firmware version for IAP device
        :return firmware response for IAP formware call
    """
    device_type = "IAP"
    for i in range(2):
        add_device_call = create_test.brnf_sa_nw_device_firmware(
            brnf_sa_order_iap_devices, device_type, endpoint, x_type, fw_version
        )
        if add_device_call:
            return add_device_call
        else:
            time.sleep(3)
    return False


@pytest.fixture()
def brnf_sa_iap_prov(brnf_sa_order_iap_devices):
    device_type = "IAP"
    for i in range(1, 3):
        add_device_call = create_test.brnf_sa_nw_device_prov(
            brnf_sa_order_iap_devices, device_type
        )
        if add_device_call:
            return add_device_call
        else:
            time.sleep(3)
    return False


@pytest.fixture()
def brnf_sa_iap_prov_msp(brnf_msp_sa_order_iap_devices):
    device_type = "IAP"
    add_device_call = create_test.brnf_sa_nw_device_prov(
        brnf_msp_sa_order_iap_devices, device_type
    )
    return add_device_call


@pytest.fixture()
def brnf_sa_sw_prov(brnf_sa_order_sw_devices, api_path, x_type):
    device_type = "SWITCH"
    for i in range(1, 3):
        add_device_call = create_test.brnf_sa_switch_device_prov(
            brnf_sa_order_sw_devices, device_type, api_path, x_type
        )
        if add_device_call.status_code == expected_response_data['switch_provision_no_rule']['response_code']:
            return add_device_call
        else:
            time.sleep(3)
    return False


@pytest.fixture()
def brnf_sa_sw_prov_msp(brnf_msp_sa_order_switch_devices, api_path, x_type):
    device_type = "SWITCH"
    add_device_call = create_test.brnf_sa_switch_device_prov(
        brnf_msp_sa_order_switch_devices, device_type, api_path, x_type
    )
    return add_device_call


@pytest.fixture()
def brnf_sa_gw_prov(brnf_sa_order_gw_devices):
    device_type = "GATEWAY"
    add_device_call = create_test.brnf_sa_nw_device_prov(
        brnf_sa_order_gw_devices, device_type
    )
    return add_device_call


@pytest.fixture()
def brnf_sa_cntrl_prov_msp(brnf_msp_sa_order_cntrl_devices):
    device_type = "CONTROLLER"
    add_device_call = create_test.brnf_sa_nw_device_prov(
        brnf_msp_sa_order_cntrl_devices, device_type
    )
    return add_device_call


@pytest.fixture()
def brnf_sa_cntrl_prov(brnf_sa_order_cntrl_devices):
    device_type = "CONTROLLER"
    add_device_call = create_test.brnf_sa_nw_device_prov(
        brnf_sa_order_cntrl_devices, device_type
    )
    return add_device_call


@pytest.fixture()
def brnf_sa_contrl_firmware(brnf_sa_order_cntrl_devices, endpoint, x_type, fw_version):
    """
     Device firmware call for firmware base version iap and gateway for controller device
        :param endpoint: firmware endpoint for controller device
        :param x_type: firmware request for firmware base version iap and gateway for controller device
        :param fw_version: firmware version for controller device
        :return firmware response for controller firmware call
    """
    device_type = "CONTROLLER"
    add_device_call = create_test.brnf_sa_nw_device_firmware(
        brnf_sa_order_cntrl_devices, device_type, endpoint, x_type, fw_version
    )
    return add_device_call


@pytest.fixture(scope="session")
def logged_in_storage_state(brnf_sa_user_login_load_account, browser_instance):
    pcid_name = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1_name"]
    yield LoginHelper.wf_webui_login(brnf_sa_user_login_load_account,
                                     browser_instance,
                                     "brnf_logged_in_state.json",
                                     pcid_name)


@pytest.fixture(scope="session")
def msp_logged_in_storage_state(brnf_msp_user_login_load_account, browser_instance):
    pcid_name = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid_name"]
    yield LoginHelper.wf_webui_login(brnf_msp_user_login_load_account,
                                     browser_instance,
                                     "brnf_msp_logged_in_state.json",
                                     pcid_name=pcid_name)


@pytest.fixture(scope="session")
def tac_logged_in_storage_state(tac_user_login_load_account, browser_instance):
    create_test = WfExistingAcctNewDevices()
    yield create_test.tac_webui_login(tac_user_login_load_account, browser_instance)


@pytest.fixture(scope="class")
def get_device_csv(brnf_sa_order_gw_devices, brnf_sa_order_sw_devices):
    devices = [*brnf_sa_order_gw_devices.values(), *brnf_sa_order_sw_devices.values()]
    yield ActivateOrdersHelper.generate_device_csv(devices)
