import logging
import os
import time

import allure
import pytest
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.choose_account_page import ChooseAccount
from hpe_glcp_automation_lib.libs.adi.ui.dev_inventory_page import DevicesInventory
from hpe_glcp_automation_lib.libs.commons.ui.manage_account_page import ManageAccount
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import (
    browser_page,
    browser_stop,
)

from automation.conftest import ExistingUserAcctDevices
from automation.local_libs.activate_inventory.activate_inventory_ui_utils import DeviceInventoryHelper
from automation.local_libs.activate_inventory.adi_test_helper import AdiTestHelper
from automation.local_libs.activate_orders.activate_orders_utils import ActivateOrdersHelper
from automation.local_libs.audit_logs.audit_logs_ui_utils import AuditLogsVerifier, LogsEventType
from automation.local_libs.login.app_api_login import AppApiSession
from automation.local_libs.login.user_api_login import UserApiLogin
from automation.local_libs.login.web_ui_login import LoginHelper
from automation.local_libs.subscription_mgmt.sm_assignments_by_api import SMAssignments
from automation.local_libs.subscription_mgmt.sm_ui_utils import SmVerifier

log = logging.getLogger(__name__)
devices_details = []
device_details = {}
device_details["device_IAP0"] = {}

class InitTestExistingDevicesUnassignDevicesAppApi:
    def __init__(self):
        self.cluster = ExistingUserAcctDevices.login_page_url
        self.username = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_dynamic_devices"]["username"]
        self.password = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_dynamic_devices"]["password"]
        self.pcid1 = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_dynamic_devices"]["pcid1"]
        self.pcid1_name = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_dynamic_devices"]["pcid1_name"]
        self.acid1 = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_dynamic_devices"]["acid1_network"]
        self.pcid2 = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_dynamic_devices"]["pcid2"]
        self.pcid2_name = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_dynamic_devices"]["pcid2_name"]
        self.acid2 = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_dynamic_devices"]["acid2_network"]
        self.api_key = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_dynamic_devices"]["api_client_id_network"]
        self.api_secret = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_dynamic_devices"]["api_client_secret_network"]

@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices")
@allure.sub_suite("Existing account - Existing dynamic list of network devices")
@pytest.mark.skipif("mira" not in ExistingUserAcctDevices.login_page_url, reason="Run during MC Test on Mira env")
class TestExistingDevicesUnassignDevicesAppApi:
    init_data = InitTestExistingDevicesUnassignDevicesAppApi()
    @pytest.mark.order(1)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220639)
    def test_move_devices_between_pcid_unassign_app_c1220639(self):
        """
        ===== Move the device from pcid1 to pcid2 for Unassign a device from Application ======
        1.  cleanup_stage: get device by acid from pcid2,
            if device exists make sure it is unassigned from the application in pcid2
            claim the device to pcid1
        2. unassign a device from the pcid1
        3. verify the device is unassign successfully
        """
        init_data = InitTestExistingDevicesUnassignDevicesAppApi()
        app_api_session = AppApiSession.adi_app_session(init_data.api_key, init_data.api_secret)
        adi_app_helper_session = AppApiSession.adi_app_helper_session(init_data.api_key, init_data.api_secret)
        try:
            pcid2_devices = app_api_session.get_devices_by_pcid(platform_customer_id=init_data.pcid2)
            devices = pcid2_devices.json()["devices"]
            if len(devices) == 1:
                # unassign device from application
                for device in devices:
                    if device["device_type"] == "AP":
                        unassign_response = app_api_session.unprovision_device_from_application(device)
                        time.sleep(5)
                        # verify device should successfully unprovisioned
                        verify_response = adi_app_helper_session.is_device_provisioned_to_pcid \
                            (platform_customer_id=init_data.pcid2,
                             serial_number=device["serial_number"])
                        device_details["device_IAP0"]["device_type"] = "IAP"
                        device_details["device_IAP0"]["serial_no"] = device["serial_number"]
                        device_details["device_IAP0"]["mac"] = device["mac_address"]
                        devices_details.append(device_details)
                AdiTestHelper.device_claim_with_app_api(init_data.pcid1,
                                                        init_data.username,
                                                        device_details["device_IAP0"]["device_type"],
                                                        devices_details[0],
                                                        app_api_session)
        except:
            log.info("device is already in pcid1, cleanup is not required")
            pass

        # get devices from list of assigned devices
        acid_devices = app_api_session.get_devices_by_acid(application_customer_id=init_data.acid1)
        devices = acid_devices.json()["devices"]
        # unassign device from application
        for device in devices:
            if device["device_type"] == "AP":
                unassign_response = app_api_session.unprovision_device_from_application(device)
                if unassign_response.status_code == 200:
                    time.sleep(5)
                    # verify device should successfully unprovisioned
                    verify_response = adi_app_helper_session.is_device_provisioned_to_pcid\
                        (platform_customer_id=init_data.pcid1,
                         serial_number=device["serial_number"])
                    device_details["device_IAP0"]["device_type"] = "IAP"
                    device_details["device_IAP0"]["serial_no"] = device["serial_number"]
                    device_details["device_IAP0"]["mac"] = device["mac_address"]
                    devices_details.append(device_details)
                    assert verify_response == False
                else:
                    assert False
        AdiTestHelper.device_claim_with_app_api(init_data.pcid2,
                                                init_data.username,
                                                device_details["device_IAP0"]["device_type"],
                                                devices_details[0],
                                                app_api_session)
        time.sleep(7)
        unassign_response = app_api_session.unprovision_device_from_application(device)
        time.sleep(7)
        verify_response = adi_app_helper_session.is_device_provisioned_to_pcid \
            (platform_customer_id=init_data.pcid1,
             serial_number=device["serial_number"])
        assert verify_response == False

    @pytest.mark.testrail(id=1220622)
    @pytest.mark.order(2)
    @pytest.mark.Plv
    @pytest.mark.Regression
    def test_brnf_manual_ui_claim_iap_c1220622(self, browser_instance,
                                               ):
        """
        ===== login and add device from device inventory page ======
        1.  login to ui
        2.  Go to device inventory page and add the device.
        3.  Verify the device is added correctly
        """
        init_data = InitTestExistingDevicesUnassignDevicesAppApi()
        user_api_login_load_account = UserApiLogin.user_api_login_load_account(init_data.username,
                                                                               init_data.password,
                                                                               init_data.pcid1)
        logged_in_storage_state = LoginHelper.wf_webui_login(user_api_login_load_account,
                                                             browser_instance,
                                                             "brnf_logged_in_state_4.json",
                                                             init_data.pcid1_name)
        context, page = browser_page(browser_instance, logged_in_storage_state)

        try:
            ChooseAccount(page, init_data.cluster).open() \
                .go_to_account_by_name(init_data.pcid1_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_devices()
            devices_inventory = DevicesInventory(page, init_data.cluster).wait_for_loaded_state()

            # Get details of first device of each type in devices_details dictionaries
            device_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)

            DeviceInventoryHelper.claim_ordered_network_devices(devices_inventory, device_details)
            assert True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            assert False

    @pytest.mark.testrail(id=1220622)
    @pytest.mark.Plv
    @pytest.mark.Regression
    @pytest.mark.order(3)
    def test_audit_log_iap_device_claim_c1220622(self,
                                                 browser_instance):
        """
        ===== login and device related audit logs from the UI ======
        1.  login to ui
        2.  Go to audit trail page and search for the device using serial number.
        3.  Verify the device related audit logs are showing correctly
        """
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        init_data = InitTestExistingDevicesUnassignDevicesAppApi()
        user_api_login_load_account = UserApiLogin.user_api_login_load_account(init_data.username,
                                                                               init_data.password,
                                                                               init_data.pcid1)
        logged_in_storage_state = LoginHelper.wf_webui_login(user_api_login_load_account,
                                                             browser_instance,
                                                             "brnf_logged_in_state_4.json",
                                                             init_data.pcid1_name)
        context, page = browser_page(browser_instance, logged_in_storage_state)

        try:
            ChooseAccount(page, init_data.cluster).open() \
                .go_to_account_by_name(init_data.pcid1_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_manage()
            audit_logs = ManageAccount(page, init_data.cluster).open_audit_logs().wait_for_loaded_table()

            # Get details of first device of each type in devices_details dictionaries
            device = devices_details[0]["device_IAP0"]
            AuditLogsVerifier.check_device_events(audit_logs, [LogsEventType.CLAIM], device)
            assert True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            assert False

        finally:
            browser_stop(context, page, test_name)

    @pytest.mark.testrail(id=1220622)
    @pytest.mark.Plv
    @pytest.mark.Regression
    @pytest.mark.order(4)
    def test_assign_sm_eval_license(self):
        """
        ===== Using api assign license key to device ======
        """
        try:
            device_type = devices_details[0]["device_IAP0"]["device_type"]
            serial = devices_details[0]["device_IAP0"]["serial_no"]
            init_data = InitTestExistingDevicesUnassignDevicesAppApi()
            user_api_login_load_account = UserApiLogin.user_api_login_load_account(init_data.username,
                                                                                   init_data.password,
                                                                                   init_data.pcid1)

            subs_assignment_resp = SMAssignments.wf_assign_subs_eval(device_type, serial, user_api_login_load_account)
            assert True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            assert False

    @pytest.mark.testrail(id=1220635)
    @pytest.mark.order(5)
    @pytest.mark.Regression
    @pytest.mark.xfail
    def test_get_audit_log_sm_details_c1220635(self, browser_instance):
        """
        ===== login and subscriptions related audit logs from the UI ======
        1.  login to ui
        2.  Go to audit trail page and search for the subscriptions using serial number.
        3.  Verify the device related audit logs are showing correctly
        """
        log.info(f"Playwright: verifying subscription at Device Subscriptions page.")

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        init_data = InitTestExistingDevicesUnassignDevicesAppApi()
        user_api_login_load_account = UserApiLogin.user_api_login_load_account(init_data.username,
                                                                               init_data.password,
                                                                               init_data.pcid1)
        storage_state_path = LoginHelper.wf_webui_login(user_api_login_load_account,
                                                             browser_instance,
                                                             "brnf_logged_in_state_4.json",
                                                             init_data.pcid1_name)
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, init_data.cluster).open() \
                .go_to_account_by_name(init_data.pcid1_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_manage()
            device_subscriptions = ManageAccount(page, init_data.cluster).open_subscriptions().wait_for_loaded_table()

            # Get details of first device of each type in devices_details dictionaries
            resp = user_api_login_load_account.get_devices_Licensed()
            device_details = resp["devices"][0]

            sm_audit_check = SmVerifier.check_device_subscription(device_subscriptions, device_details)

            assert True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            assert False

        finally:
            browser_stop(context, page, test_name)


