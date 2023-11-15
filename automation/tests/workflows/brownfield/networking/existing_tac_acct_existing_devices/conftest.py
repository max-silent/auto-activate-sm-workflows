import logging

import pytest

from automation.conftest import ExistingUserAcctDevices
from automation.local_libs.ui_doorway.ui_doorway_devices_by_api import UiDoorwayDevices
from automation.tests.workflows.brownfield.networking.existing_tac_acct_existing_devices.brnf_network_existing_tac_acct_devices \
    import WfExistingTacExistingDevices
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils
from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway

log = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def device_folder_name(brnf_sa_user_login_load_account):
    create_test = WfExistingTacExistingDevices()
    rand_string = RandomGenUtils.random_string_of_chars(uppercase=True, digits=True)
    folder_name = f"Auto_tac_{rand_string}"
    yield folder_name
    UiDoorwayDevices.delete_folder(folder_name, brnf_sa_user_login_load_account, create_test.pcid)


@pytest.fixture(scope="function")
def movable_device_sn_iap(brnf_sa_user_login_load_account):
    device_sn = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_iap_sn"]
    device_part_no = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_iap_part_no"]
    device_mac = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_iap_mac"]
    yield device_sn
    # Move device back to "default" folder as a teardown action.
    device_details = [{"serial_number": device_sn,
                       "part_number": device_part_no,
                       "mac_address": device_mac,
                       "device_type": "IAP"
                       }]
    pcid = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1"]
    brnf_sa_user_login_load_account.move_devices_to_folder(device_details, "default", pcid)


@pytest.fixture(scope="function")
def movable_device_sn_gw(brnf_sa_user_login_load_account):
    device_sn = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_gw_sn"]
    device_part_no = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_gw_part_no"]
    device_mac = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_gw_mac"]
    yield device_sn
    # Move device back to "default" folder as a teardown action.
    device_details = [{"serial_number": device_sn,
                       "part_number": device_part_no,
                       "mac_address": device_mac,
                       "device_type": "GATEWAY"
                       }]
    pcid = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1"]
    brnf_sa_user_login_load_account.move_devices_to_folder(device_details, "default", pcid)


@pytest.fixture(scope="function")
def movable_device_sn_sw(brnf_sa_user_login_load_account):
    device_sn = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_sw_sn"]
    device_part_no = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_sw_part_no"]
    device_mac = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_sw_mac"]
    yield device_sn
    # Move device back to "default" folder as a teardown action.
    device_details = [{"serial_number": device_sn,
                       "part_number": device_part_no,
                       "mac_address": device_mac,
                       "device_type": "SWITCH"
                       }]
    pcid = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1"]
    brnf_sa_user_login_load_account.move_devices_to_folder(device_details, "default", pcid)


@pytest.fixture(scope="function")
def inter_customers_movable_devices(brnf_sa_user_login_load_account):
    devices_details = ExistingUserAcctDevices.test_data["brnf_existing_acct_devices_list"]
    yield devices_details
    # Move devices back to original owner customer
    devices_ids = [device_details["serial_number"] for device_details in devices_details]
    devices_owner_pcid = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1"]
    brnf_sa_user_login_load_account.move_devices_to_customer(devices_ids, devices_owner_pcid, "default")


@pytest.fixture(scope="function")
def athena_f_devices(brnf_sa_user_login_load_account):
    devices_details = ExistingUserAcctDevices.test_data["brnf_existing_acct_athena_f_devices_list"]
    yield devices_details
    # Move devices back to original owner customer
    devices_ids = [device_details["serial_number"] for device_details in devices_details]
    devices_owner_pcid = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1"]
    athena_f_folder = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1_athena_f_folder"]
    brnf_sa_user_login_load_account.move_devices_to_customer(devices_ids, devices_owner_pcid, athena_f_folder)


@pytest.fixture(scope="session")
def brnf_sa_user_login_load_account():
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data["tac_admin_username"]
    password = ExistingUserAcctDevices.test_data["tac_admin_password"]
    pcid = ExistingUserAcctDevices.test_data["tac_admin_pcid1"]
    url = hostname.split("//")[1]
    yield UIDoorway(url, username, password, pcid)


@pytest.fixture(scope="session")
def logged_in_storage_state(brnf_sa_user_login_load_account, browser_instance):
    create_test = WfExistingTacExistingDevices()
    yield create_test.wf_webui_login(brnf_sa_user_login_load_account, browser_instance)


@pytest.fixture(scope="module")
def eval_subscription(brnf_sa_user_login_load_account):
    create_test = WfExistingTacExistingDevices()
    yield create_test.wf_generate_eval_subscription(brnf_sa_user_login_load_account)


@pytest.fixture(scope="module")
def sw_brim_subscription(brnf_sa_user_login_load_account):
    subs_key = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_sw_brim_subs_key"]
    subs_before = brnf_sa_user_login_load_account.get_cm_customer_subscriptions(subscription_key_pattern=subs_key)[0]
    source_pcid = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1"]
    yield subs_before
    subscription = brnf_sa_user_login_load_account.get_cm_customer_subscriptions(subscription_key_pattern=subs_key)[0]
    if subscription.get("platform_customer_id") != source_pcid:
        brnf_sa_user_login_load_account.transfer_cm_eval_subscription(source_pcid, subs_key)


@pytest.fixture(scope="module")
def service_brim_subscription(brnf_sa_user_login_load_account):
    subs_key = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_service_brim_subs_key"]
    subs_before = brnf_sa_user_login_load_account.get_cm_customer_subscriptions(subscription_key_pattern=subs_key)[0]
    source_pcid = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1"]
    yield subs_before
    subscription = brnf_sa_user_login_load_account.get_cm_customer_subscriptions(subscription_key_pattern=subs_key)[0]
    if subscription.get("platform_customer_id") != source_pcid:
        brnf_sa_user_login_load_account.transfer_cm_eval_subscription(source_pcid, subs_key)


@pytest.fixture(scope="module")
def customer_alias_name(brnf_sa_user_login_load_account, device_folder_name):
    create_test = WfExistingTacExistingDevices()
    yield device_folder_name
    UiDoorwayDevices.delete_alias(device_folder_name, brnf_sa_user_login_load_account, create_test.pcid)
