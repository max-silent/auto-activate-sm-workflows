import json
import logging
import time
from typing import Union

import pytest
from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.local_libs.login.web_ui_login import LoginHelper
from automation_svc_ui.tests.workflows.greenfield.wf_session_new_user_acct_first_order_auto_claim import (
    WfNewDeviceNewUserSignupCreateAcct,
)

log = logging.getLogger(__name__)
create_test = WfNewDeviceNewUserSignupCreateAcct()


@pytest.fixture(scope="session")
def order_iap_devices():
    device_type = "IAP"
    return create_test.new_nw_device_fn(device_type)


@pytest.fixture(scope="session")
def order_sw_devices():
    device_type = "SWITCH"
    return create_test.new_nw_device_fn(device_type)


@pytest.fixture(scope="session")
def order_gw_devices():
    device_type = "GATEWAY"
    return create_test.new_nw_device_fn(device_type)


@pytest.fixture()
def order_storage_legacy_devices():
    device_type = "STORAGE"
    return create_test.new_nw_device_fn(device_type)


@pytest.fixture()
def order_compute_devices():
    device_type = "COMPUTE"
    return create_test.new_nw_device_fn(device_type)


@pytest.fixture(scope="session")
def create_user_create_account(browser_instance):
    """test_new_user_signup_create_acct, create devices, provision app_api, add devices, assign sm"""
    result: Union[bool, str] = False
    retries = 2
    for count in range(retries):
        if count > 0:
            time.sleep(5)
            log.warning("Retrying to customer signup again")
        try:
            customer_details = (
                create_test.wf_new_user_acct_fn(browser_instance)
            )
            if customer_details:
                log.info("customer details: {}".format(customer_details))
                result = customer_details
                break
        except Exception as ex:
            log.error(f"Not able to setup a new user and account:\n{ex}")
    return result


@pytest.fixture(scope="session")
def new_user_login_load_account(create_user_create_account):
    if create_user_create_account:
        new_setup_info = json.loads(create_user_create_account)
        log.info(new_setup_info)
    else:
        raise ValueError("User/account was not created")
    url = new_setup_info["url"].split("//")[1]
    return UIDoorway(
        url, new_setup_info["user"], new_setup_info["password"], new_setup_info["pcid"]
    )


@pytest.fixture(scope="session")
def tac_user_login_load_account():
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data["tac_admin_username"]
    password = ExistingUserAcctDevices.test_data["tac_admin_password"]
    pcid = ExistingUserAcctDevices.test_data["tac_admin_pcid1"]
    url = hostname.split("//")[1]
    return UIDoorway(url, username, password, pcid)


@pytest.fixture(scope="session")
def new_provision_app():
    return create_test.wf_prov_app_fn(new_user_login_load_account)


@pytest.fixture()
def brnf_sa_new_iap_prov(order_iap_devices):
    device_type = "IAP"
    add_device_call = create_test.grnf_sa_nw_new_device_prov(
        order_iap_devices, device_type
    )
    return add_device_call


@pytest.fixture()
def brnf_sa_new_sw_prov(order_sw_devices):
    device_type = "SWITCH"
    add_device_call = create_test.grnf_sa_nw_new_device_prov(
        order_sw_devices, device_type
    )
    return add_device_call


@pytest.fixture()
def brnf_sa_new_gw_prov(order_gw_devices):
    device_type = "GATEWAY"
    add_device_call = create_test.grnf_sa_nw_new_device_prov(
        order_gw_devices, device_type
    )
    return add_device_call


@pytest.fixture(scope="session")
def logged_in_storage_state(new_user_login_load_account, browser_instance):
    yield LoginHelper.wf_webui_login(new_user_login_load_account, browser_instance, "gf_logged_in_state.json")


@pytest.fixture(scope="class")
def login_second_user_create_account(browser_instance):
    """Create account for test_remove_alias_from_one_and_add_to_another"""
    result: Union[bool, str] = False
    retries = 2
    test = WfNewDeviceNewUserSignupCreateAcct()
    for count in range(retries):
        if count > 0:
            time.sleep(5)
            log.warning("Retrying to customer signup again")
        try:
            customer_details = (
                test.wf_new_user_acct_fn(browser_instance)
            )
            if customer_details:
                log.info("customer details: {}".format(customer_details))
                result = customer_details
                break
        except Exception as ex:
            log.error(f"Not able to setup a new user and account:\n{ex}")
    if result:
        new_setup_info = json.loads(result)
        url = new_setup_info["url"].split("//")[1]
        return UIDoorway(url, new_setup_info["user"], new_setup_info["password"], new_setup_info["pcid"])
    else:
        raise ValueError("User/account was not created")
