import logging

import pytest
from hpe_glcp_automation_lib.libs.add.device_calls.add_payload_constant import ADDDeviceConstants
from hpe_glcp_automation_lib.libs.commons.utils.humio.humio_utils import HumioClass
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils
from hpe_glcp_automation_lib.libs.sm.app_api.sm_app_api import SubscriptionManagementApp
from hpe_glcp_automation_lib.libs.sm.helpers.sm_create_orders_helper import NewSubsOrder
from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.conftest import SkipTest
from automation_svc_ui.local_libs.login.web_ui_login import LoginHelper
from automation_svc_ui.local_libs.subscription_mgmt.sm_assignments_by_api import SMAssignments
from automation_svc_ui.local_libs.ui_doorway.ui_doorway_devices_by_api import UiDoorwayDevices
from automation_svc_ui.tests.brownfield_existing_acct_existing_devices.network_device_flows \
    .brnf_network_existing_acct_existing_devices import WfExistingAcctExistingDevices

log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def humio_session():
    humio_base_url = ExistingUserAcctDevices.humio_url
    humio_repository = "ccsportal"
    humio_user_token = ExistingUserAcctDevices.test_data["humio_user_token"]

    humioSession = HumioClass(base_url=humio_base_url, repository=humio_repository, user_token=humio_user_token)
    return humioSession


@pytest.fixture(scope="module")
def device_folder_name(brnf_sa_user_login_load_account):
    rand_string = RandomGenUtils.random_string_of_chars(uppercase=True, digits=True)
    folder_name = f"Auto_{rand_string}"
    yield folder_name
    UiDoorwayDevices.delete_folder(folder_name, brnf_sa_user_login_load_account)


@pytest.fixture(scope="session")
def brnf_sa_user_login_load_account():
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
    password = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_password']
    pcid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_pcid']
    url = hostname.split('//')[1]
    return UIDoorway(url, username, password, pcid)


@pytest.fixture(scope="class")
def brnf_second_user_login_load_account():
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_username"]
    password = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_password"]
    pcid = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1"]
    url = hostname.split("//")[1]
    return UIDoorway(url, username, password, pcid)


@pytest.fixture(scope="session")
def brnf_assign_iap_devices_to_app(brnf_sa_user_login_load_account):
    create_test = WfExistingAcctExistingDevices()
    device_type = "IAP"
    device_data = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_sn']
    appid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_appid"]
    app_instance_id = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_instance_id"]
    return create_test.wf_existing_device_app_assignment(device_type,
                                                         device_data,
                                                         brnf_sa_user_login_load_account,
                                                         appid,
                                                         app_instance_id)


@pytest.fixture(scope="session")
def brnf_assign_sw_devices_to_app(brnf_sa_user_login_load_account):
    create_test = WfExistingAcctExistingDevices()
    device_type = "SWITCH"
    device_data = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_sw_sn']
    appid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_appid"]
    app_instance_id = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_instance_id"]
    return create_test.wf_existing_device_app_assignment(device_type,
                                                         device_data,
                                                         brnf_sa_user_login_load_account,
                                                         appid,
                                                         app_instance_id)


@pytest.fixture(scope="session")
def brnf_assign_gw_devices_to_app(brnf_sa_user_login_load_account):
    create_test = WfExistingAcctExistingDevices()
    device_type = "GATEWAY"
    device_data = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_gw_sn']
    appid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_appid"]
    app_instance_id = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_instance_id"]
    return create_test.wf_existing_device_app_assignment(device_type,
                                                         device_data,
                                                         brnf_sa_user_login_load_account,
                                                         appid,
                                                         app_instance_id)


@pytest.fixture(scope="session")
def brnf_sa_manual_evals_subs_iap(brnf_sa_user_login_load_account):
    serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_sn']
    device_type = "IAP"
    return SMAssignments().wf_assign_subs_eval(device_type,
                                               serial,
                                               brnf_sa_user_login_load_account)


@pytest.fixture(scope="session")
def brnf_sa_manual_evals_subs_sw(brnf_sa_user_login_load_account):
    serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_sw_sn']
    device_type = "SWITCH"
    return SMAssignments().wf_assign_subs_eval(device_type,
                                               serial,
                                               brnf_sa_user_login_load_account)


@pytest.fixture(scope="session")
def brnf_sa_manual_evals_subs_gw(brnf_sa_user_login_load_account):
    serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_gw_sn']
    device_type = "GATEWAY"
    return SMAssignments().wf_assign_subs_eval(device_type,
                                               serial,
                                               brnf_sa_user_login_load_account)


@pytest.fixture()
def existint_acct_existing_dev_brnf_sa_iap_prov():
    device_type = "IAP"
    serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_sn']
    mac_address = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_mac']
    create_test = WfExistingAcctExistingDevices()
    add_device_call = create_test.brnf_sa_nw_device_prov(serial,
                                                         mac_address,
                                                         device_type, )
    return add_device_call


@pytest.fixture()
def existint_acct_existing_dev_brnf_sa_sw_prov():
    device_type = "SWITCH"
    serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_sw_sn']
    mac_address = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_sw_mac']
    create_test = WfExistingAcctExistingDevices()
    add_device_call = create_test.brnf_sa_nw_device_prov(serial,
                                                         mac_address,
                                                         device_type, )
    return add_device_call


@pytest.fixture()
def existing_acct_existing_dev_brnf_sa_sw_firmware(api_path, x_type):
    device_type = "SWITCH"
    serial_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_serial_no']
    part_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_part_no']
    mac_address = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_mac']
    create_test = WfExistingAcctExistingDevices()
    add_device_call = create_test.brnf_sa_switch_device_prov(device_type, serial_no, mac_address, part_no, api_path,
                                                             x_type)
    return add_device_call


@pytest.fixture()
def existint_acct_existing_dev_brnf_sa_gw_prov():
    device_type = "GATEWAY"
    serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_gw_sn']
    mac_address = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_gw_mac']
    create_test = WfExistingAcctExistingDevices()
    add_device_call = create_test.brnf_sa_nw_device_prov(serial,
                                                         mac_address,
                                                         device_type, )
    return add_device_call


@pytest.fixture()
def brnf_sa_vgw_est_prov():
    device_type = "GATEWAY"
    serial_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_vgw_serial_no']
    mac_address = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_vgw_mac']
    part_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_vgw_part_no']
    create_test = WfExistingAcctExistingDevices()
    add_device_call = create_test.brnf_sa_device_est_prov(device_type, serial_no, mac_address, part_no)
    return add_device_call


@pytest.fixture()
def brnf_sa_vgw_verify_est():
    device_type = "GATEWAY"
    serial_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_vgw_serial_no']
    mac_address = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_vgw_mac']
    part_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_vgw_part_no']
    create_test = WfExistingAcctExistingDevices()
    username = f"{serial_no},{mac_address},{part_no},VGW"
    vgw_payload_data = ADDDeviceConstants.vgw_device_data()['vgw_payload_data']
    verify_est_call = create_test.brnf_sa_verify_est(device_type, serial_no, mac_address, part_no,
                                                     username, vgw_payload_data)
    return verify_est_call


@pytest.fixture()
def brnf_sa_nontpm_est_prov():
    device_type = "SWITCH"
    serial_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_serial_no']
    part_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_part_no']
    mac_address = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_mac']
    create_test = WfExistingAcctExistingDevices()
    add_device_call = create_test.brnf_sa_device_est_prov(device_type, serial_no, mac_address, part_no)
    return add_device_call


@pytest.fixture()
def brnf_sa_nontpm_verify_est():
    device_type = "SWITCH"
    serial_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_serial_no']
    part_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_part_no']
    mac_address = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_mac']
    create_test = WfExistingAcctExistingDevices()
    username = f"{serial_no}, {mac_address}, {part_no}, NONTPM"
    nontpm_payload_data = ADDDeviceConstants.nontpm_device_data()['nontpm_payload_data']
    verify_est_call = create_test.brnf_sa_verify_est(device_type, serial_no, mac_address, part_no,
                                                     username, nontpm_payload_data)
    return verify_est_call


@pytest.fixture()
def brnf_sa_nontpm_prov():
    device_type = "SWITCH"
    serial_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_serial_no']
    part_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_part_no']
    mac_address = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_mac']
    create_test = WfExistingAcctExistingDevices()
    add_device_call = create_test.brnf_sa_switch_device_prov(device_type, serial_no, mac_address, part_no, "hpe-nontpm",
                                                             "provision-update")
    return add_device_call


@pytest.fixture()
def brnf_sa_nontpm_prov_invalid_mac():
    device_type = "SWITCH"
    serial_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_serial_no']
    part_no = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_nontpm_part_no']
    mac_address = "00:9C:02:63:00:10"
    create_test = WfExistingAcctExistingDevices()
    add_device_call = create_test.brnf_sa_switch_device_prov(device_type, serial_no, mac_address, part_no, "hpe-nontpm",
                                                             "provision-update")
    return add_device_call


@pytest.fixture(scope="session")
def logged_in_storage_state(brnf_sa_user_login_load_account, browser_instance):
    pcid_name = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_acct1"]
    yield LoginHelper.wf_webui_login(brnf_sa_user_login_load_account,
                                     browser_instance,
                                     "brnf_logged_in_state_2.json",
                                     pcid_name)


@pytest.fixture(scope="session")
def second_acc_logged_in_storage_state(browser_instance):
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data['brnf_existing_acct_new_devices_username']
    password = ExistingUserAcctDevices.test_data['brnf_existing_acct_new_devices_password']
    pcid = ExistingUserAcctDevices.test_data['brnf_existing_acct_new_devices_pcid1']
    pcid_name = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1_name"]
    url = hostname.split('//')[1]
    user_info = UIDoorway(url, username, password, pcid)
    yield LoginHelper.wf_webui_login(user_info,
                                     browser_instance,
                                     "brnf_logged_in_state_3.json",
                                     pcid_name)


@pytest.fixture(scope="session")
def sm_app_api_session():
    SkipTest.skip_if_triton_lite()
    sm_app_api = SubscriptionManagementApp(
        host=ExistingUserAcctDevices.app_api_hostname,
        sso_host=ExistingUserAcctDevices.sso_hostname,
        client_id=ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_client_id"],
        client_secret=ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_client_secret"],
    )
    return sm_app_api


@pytest.fixture(scope="session")
def brnf_sa_new_brim_combined_subs_ap_sw_gw(brnf_sa_user_login_load_account):
    end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
    app_api_host = ExistingUserAcctDevices.app_api_hostname
    sso_host = ExistingUserAcctDevices.sso_hostname
    aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
    aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']

    # create a new subscription for AP and add to account
    new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
    try:
        ap_key, sw_key, gw_key, lic_quote = new_order.create_combined_ap_sw_gw_subs_order()
    except Exception as e:
        log.error(f"Could not create new, combined subscription dynamically. Error: {e}")
        return False

    return ap_key, sw_key, gw_key, lic_quote


@pytest.fixture(scope="session")
def brnf_sa_new_brim_subs_iap(brnf_sa_user_login_load_account):
    end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
    app_api_host = ExistingUserAcctDevices.app_api_hostname
    sso_host = ExistingUserAcctDevices.sso_hostname
    aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
    aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']

    # create a new subscription for AP and add to account
    new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
    try:
        license_key, lic_quote = new_order.create_ap_subs_order()
    except Exception as e:
        log.error(f"Could not create new subscription dynamically. Error: {e}")
        return False

    return license_key, lic_quote


@pytest.fixture(scope="session")
def brnf_sa_new_brim_subs_switch(brnf_sa_user_login_load_account):
    end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
    app_api_host = ExistingUserAcctDevices.app_api_hostname
    sso_host = ExistingUserAcctDevices.sso_hostname
    aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
    aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']

    # create a new subscription for AP and add to account
    new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
    try:
        license_key, lic_quote = new_order.create_sw_subs_order()
    except Exception as e:
        log.error(f"Could not create new subscription dynamically. Error: {e}")
        return False

    return license_key, lic_quote


@pytest.fixture(scope="session")
def brnf_sa_new_brim_subs_gw_70xx(brnf_sa_user_login_load_account):
    end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
    app_api_host = ExistingUserAcctDevices.app_api_hostname
    sso_host = ExistingUserAcctDevices.sso_hostname
    aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
    aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']

    # create a new subscription for AP and add to account
    new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
    try:
        license_key, lic_quote = new_order.create_gw_subs_order(order_type="70XX")
    except Exception as e:
        log.error(f"Could not create new subscription dynamically. Error: {e}")
        return False

    return license_key, lic_quote


@pytest.fixture(scope="session")
def brnf_sa_new_brim_subs_vgw(brnf_sa_user_login_load_account):
    end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
    app_api_host = ExistingUserAcctDevices.app_api_hostname
    sso_host = ExistingUserAcctDevices.sso_hostname
    aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
    aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']

    # create a new subscription for AP and add to account
    new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
    try:
        license_key, lic_quote = new_order.create_vgw_subs_order()
    except Exception as e:
        log.error(f"Could not create new subscription dynamically. Error: {e}")
        return False

    return license_key, lic_quote
