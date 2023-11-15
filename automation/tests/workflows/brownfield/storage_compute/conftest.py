import logging
import time

import pytest

from automation.conftest import ExistingUserAcctDevices
from automation.local_libs.activate_orders.activate_orders_utils import ActivateOrdersHelper
from automation.local_libs.login.web_ui_login import LoginHelper
from automation.local_libs.ui_doorway.ui_doorway_devices_by_api import UiDoorwayDevices
from automation.tests.workflows.brownfield.networking.existing_acct_new_devices.brnf_network_existing_acct_new_devices import \
    WfExistingAcctNewDevices
from automation.tests.workflows.brownfield.storage_compute.brnf_str_com_existing_acct_devices import (
    WfScExistingAcctDevices,
)
from hpe_glcp_automation_lib.libs.adi.app_api.adi_app_api import ActivateInventory
from hpe_glcp_automation_lib.libs.sm.helpers.sm_create_orders_helper import NewSubsOrder
from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway

log = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def order_sc_storage_legacy_devices():
    create_test = WfScExistingAcctDevices()
    device_test = "STORAGE"
    for i in range(2):
        mfr_storage_dev = create_test.existing_acct_sc_create_device_fn(device_test)
        if mfr_storage_dev:
            return mfr_storage_dev
        else:
            time.sleep(3)
    return False


@pytest.fixture(scope="session")
def order_sc_dhci_storage_legacy_devices():
    create_test = WfScExistingAcctDevices()
    device_test = "DHCI_STORAGE"
    return create_test.existing_acct_sc_create_device_fn(device_test)


@pytest.fixture(scope="class")
def order_sc_compute_devices():
    create_test = WfScExistingAcctDevices()
    device_test = "COMPUTE"
    return create_test.existing_acct_sc_create_device_fn(device_test)


@pytest.fixture(scope="class")
def order_sc_gw_devices():
    create_test = WfScExistingAcctDevices()
    device_test = "GATEWAY"
    return create_test.existing_acct_sc_create_device_fn(device_test)


@pytest.fixture(scope="session")
# @measure_time
def brnf_sa_sc_user_login_load_account():
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data["brnf_sc_username"]
    password = ExistingUserAcctDevices.test_data["brnf_sc_password"]
    pcid = ExistingUserAcctDevices.test_data["brnf_sc_pcid"]
    url = hostname.split("//")[1]
    for i in range(2):
        ui_doorway_session = UIDoorway(url, username, password, pcid)
        if ui_doorway_session:
            return ui_doorway_session
        else:
            time.sleep(3)
    return False


@pytest.fixture(scope="class")
def brnf_sa_sc_manual_claim_storage_device(
        order_sc_storage_legacy_devices, brnf_sa_sc_user_login_load_account
):
    device_type = "STORAGE"
    for i in range(2):
        claim_device = UiDoorwayDevices.claim_app_assignment(device_type,
                                                             order_sc_storage_legacy_devices,
                                                             brnf_sa_sc_user_login_load_account)
        if claim_device:
            return claim_device
        else:
            time.sleep(3)
    return False


@pytest.fixture(scope="session")
def brnf_sa_sc_manual_claim_dhci_storage_device(
        order_sc_dhci_storage_legacy_devices, brnf_sa_sc_user_login_load_account
):
    device_type = "DHCI_STORAGE"
    for i in range(2):
        claim_device = UiDoorwayDevices.claim_app_assignment(device_type,
                                                             order_sc_dhci_storage_legacy_devices,
                                                             brnf_sa_sc_user_login_load_account)
        if claim_device:
            return claim_device
        else:
            time.sleep(3)
    return False


# @pytest.fixture(scope="class")
# def brnf_sa_sc_manual_claim_compute_device(
#         order_sc_compute_devices, brnf_sa_sc_user_login_load_account
# ):
#     device_type = "COMPUTE"
#     return UiDoorwayDevices.claim_app_assignment(
#         device_type, order_sc_compute_devices, brnf_sa_sc_user_login_load_account
#     )
#

@pytest.fixture(scope="class")
def brnf_sa_sc_manual_claim_gw_device(
        order_sc_gw_devices, brnf_sa_sc_user_login_load_account
):
    device_type = "GATEWAY"
    return UiDoorwayDevices.claim_app_assignment(
        device_type, order_sc_gw_devices, brnf_sa_sc_user_login_load_account
    )


@pytest.fixture()
def brnf_sa_sc_storage_prov(order_sc_storage_legacy_devices):
    device_type = "STORAGE"
    create_test = WfScExistingAcctDevices()
    for i in range(1, 3):
        add_device_call = create_test.brnf_sa_sc_prov(
            device_type, order_sc_storage_legacy_devices
        )
        if add_device_call:
            return add_device_call
        else:
            time.sleep(3)
    return False


@pytest.fixture()
def brnf_sa_sc_compute_prov(order_sc_compute_devices):
    device_type = "COMPUTE"
    create_test = WfScExistingAcctDevices()
    add_device_call = create_test.brnf_sa_sc_prov(device_type, order_sc_compute_devices)
    log.info(add_device_call)
    return add_device_call


@pytest.fixture()
def brnf_sa_sc_dhci_storage_prov(order_sc_dhci_storage_legacy_devices):
    device_type = "DHCI_STORAGE"
    create_test = WfScExistingAcctDevices()
    add_device_call = create_test.brnf_sa_sc_prov(
        device_type, order_sc_dhci_storage_legacy_devices
    )
    return add_device_call


@pytest.fixture(scope="function")
def brnf_idev_ldev_compute_prov(serial, part, certs):
    device_type = "COMPUTE"
    create_test = WfScExistingAcctDevices()
    add_device_call = create_test.brnf_idev_ldev_compute_prov(device_type, serial, part, certs)
    return add_device_call


@pytest.fixture(scope="class")
def brnf_assign_comp_devices_to_app(brnf_sa_sc_user_login_load_account):
    create_test = WfScExistingAcctDevices()
    device_type = "COMPUTE"
    device_data = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_comp_sn']
    part_number = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_comp_part']
    appid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_comp_appid"]
    app_instance_id = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_comp_instance_id"]
    return create_test.wf_existing_device_app_assignment(device_type,
                                                         part_number,
                                                         device_data,
                                                         brnf_sa_sc_user_login_load_account,
                                                         appid,
                                                         app_instance_id)


@pytest.fixture(scope="class")
def brnf_unassign_comp_devices_to_app(brnf_sa_sc_user_login_load_account):
    create_test = WfScExistingAcctDevices()
    device_type = "COMPUTE"
    device_data = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_comp_sn']
    part_number = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_comp_part']
    appid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_comp_appid"]
    app_instance_id = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_comp_instance_id"]
    return create_test.wf_existing_device_app_unassignment(device_type,
                                                           part_number,
                                                           device_data,
                                                           brnf_sa_sc_user_login_load_account,
                                                           appid,
                                                           app_instance_id)


@pytest.fixture(scope="class")
def brnf_sa_new_brim_subs_compute_iaas(brnf_sa_sc_user_login_load_account):
    app_api_host = ExistingUserAcctDevices.app_api_hostname
    sso_host = ExistingUserAcctDevices.sso_hostname
    end_username = ExistingUserAcctDevices.test_data['brnf_sc_username']
    aop_client_id = ExistingUserAcctDevices.test_data['brnf_sc_api_client_id']
    aop_client_secret = ExistingUserAcctDevices.test_data['brnf_sc_api_client_secret']

    # create a new subscription for AP and add to account
    new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
    try:
        license_key, lic_quote = new_order.create_compute_subs_order()
        if not lic_quote:
            return False
    except Exception as e:
        log.error(f"Could not create new compute iaas subscription dynamically. Error: {e}")
        return False

    return license_key, lic_quote


@pytest.fixture(scope="class")
def brnf_sa_new_brim_subs_storage_baas(brnf_sa_sc_user_login_load_account):
    app_api_host = ExistingUserAcctDevices.app_api_hostname
    sso_host = ExistingUserAcctDevices.sso_hostname
    end_username = ExistingUserAcctDevices.test_data['brnf_sc_username']
    aop_client_id = ExistingUserAcctDevices.test_data['brnf_sc_api_client_id']
    aop_client_secret = ExistingUserAcctDevices.test_data['brnf_sc_api_client_secret']

    # create a new subscription for AP and add to account
    new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
    try:
        license_key, lic_quote = new_order.create_storage_baas_order()
        if not lic_quote:
            return False
    except Exception as e:
        log.error(f"Could not create new storage baas subscription dynamically. Error: {e}")
        return False

    return license_key, lic_quote


@pytest.fixture(scope="class")
def brnf_sa_new_brim_subs_compute_gecko(brnf_sa_sc_user_login_load_account):
    app_api_host = ExistingUserAcctDevices.app_api_hostname
    sso_host = ExistingUserAcctDevices.sso_hostname
    end_username = ExistingUserAcctDevices.test_data['brnf_sc_username']
    aop_client_id = ExistingUserAcctDevices.test_data['brnf_sc_api_client_id']
    aop_client_secret = ExistingUserAcctDevices.test_data['brnf_sc_api_client_secret']

    # create a new subscription for Gecko
    new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
    try:
        license_key, lic_quote, lic_devices = new_order.create_compute_gecko_subs_order("PROLIANT")
        if not lic_quote:
            return False
    except Exception as e:
        log.error(f"Could not create new gecko compute iaas subscription dynamically. Error: {e}")
        return False

    return license_key, lic_quote, lic_devices


@pytest.fixture(scope="class")
def brnf_sa_new_brim_subs_hciaas_baas(brnf_sa_sc_user_login_load_account):
    app_api_host = ExistingUserAcctDevices.app_api_hostname
    sso_host = ExistingUserAcctDevices.sso_hostname
    end_username = ExistingUserAcctDevices.test_data['brnf_sc_username']
    aop_client_id = ExistingUserAcctDevices.test_data['brnf_sc_api_client_id']
    aop_client_secret = ExistingUserAcctDevices.test_data['brnf_sc_api_client_secret']

    # create a new subscription for AP and add to account
    new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
    try:
        license_key, lic_quote, lic_devices = new_order.create_storage_hciaas_order(order_type="HCIAAS")
        if not lic_quote:
            return False
    except Exception as e:
        log.error(f"Could not create new storage baas subscription dynamically. Error: {e}")
        return False

    return license_key, lic_quote, lic_devices

@pytest.fixture(scope="class")
def brnf_sa_new_brim_subs_hciaas_baas_two(brnf_sa_sc_user_login_load_account):
    app_api_host = ExistingUserAcctDevices.app_api_hostname
    sso_host = ExistingUserAcctDevices.sso_hostname
    end_username = ExistingUserAcctDevices.test_data['brnf_sc_username']
    aop_client_id = ExistingUserAcctDevices.test_data['brnf_sc_api_client_id']
    aop_client_secret = ExistingUserAcctDevices.test_data['brnf_sc_api_client_secret']

    # create a new subscription for AP and add to account
    new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
    try:
        license_key, lic_quote, lic_devices = new_order.create_storage_hciaas_order(order_type="HCIAAS")
        if not lic_quote:
            return False
    except Exception as e:
        log.error(f"Could not create new storage baas subscription dynamically. Error: {e}")
        return False

    return license_key, lic_quote, lic_devices


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


@pytest.fixture(scope="session")
def logged_in_storage_state(brnf_sa_sc_user_login_load_account, browser_instance):
    pcid_name = ExistingUserAcctDevices.test_data["brnf_sc_pcid_name"]
    yield LoginHelper.wf_webui_login(brnf_sa_sc_user_login_load_account,
                                     browser_instance,
                                     "brnf_sc_logged_in_state.json",
                                     pcid_name)


@pytest.fixture(scope="class")
def get_device_csv(order_sc_compute_devices):
    devices = [*order_sc_compute_devices.values()]
    yield ActivateOrdersHelper.generate_device_csv(devices, filename="compute_device.csv")


@pytest.fixture(scope="class")
def brnf_sa_order_iap_devices():
    """
    Create an IAP device
    :return: IAP device
    """
    create_test = WfExistingAcctNewDevices()
    device_type = "IAP"
    return create_test.existing_acct_create_device_of_type(device_type)
