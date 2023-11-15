import json
import logging
import os
import time
from datetime import datetime, timedelta, date

from automation_svc_ui.configs.device_mappings.activate_inventory_device_mapping import ActivateInventoryPartMap
from automation_svc_ui.conftest import ExistingUserAcctDevices, SubscriptionData
from automation_svc_ui.constants import RECORD_DIR
from automation_svc_ui.local_libs.activate_devices.manufacture_order_utils import ManufactureDevicesHelper
from automation_svc_ui.local_libs.activate_inventory.activate_inventory_ui_utils import ActivateInventoryVerifier
from automation_svc_ui.local_libs.activate_inventory.activate_inventory_ui_utils import DeviceInventoryHelper
from automation_svc_ui.local_libs.activate_orders.activate_orders_utils import ActivateOrdersHelper
from automation_svc_ui.local_libs.audit_logs.audit_logs_ui_utils import AuditLogsVerifier, LogsEventType
from automation_svc_ui.local_libs.subscription_mgmt.sm_ui_utils import SmVerifier
from automation_svc_ui.local_libs.ui_doorway.ui_doorway_devices_by_api import UiDoorwayDevices
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.choose_account_page import ChooseAccount
from hpe_glcp_automation_lib.libs.add.device_calls.device_prov import (
    NetworkStorageComputeDeviceProvisionHelper,
)
from hpe_glcp_automation_lib.libs.adi.app_api.adi_app_api import ActivateInventory
from hpe_glcp_automation_lib.libs.adi.ui.dev_inventory_page import DevicesInventory
from hpe_glcp_automation_lib.libs.aop.helpers.aop_payload_constants import (
    AOPDeviceConstants,
)
from hpe_glcp_automation_lib.libs.app_prov.ui.my_applications_page import MyApplications
from hpe_glcp_automation_lib.libs.authn.ui.login_page import Login
from hpe_glcp_automation_lib.libs.authn.user_api.session.core.exceptions import SessionException
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_customers_page import TacCustomersPage
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_devices_page import TacDevicesPage
from hpe_glcp_automation_lib.libs.commons.ui.manage_account_page import ManageAccount
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import (
    browser_page,
    browser_stop,
)
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils
from hpe_glcp_automation_lib.libs.sm.app_api.sm_app_api import SubscriptionManagementApp
from hpe_glcp_automation_lib.libs.sm.ui.device_subscriptions import DeviceSubscriptions

log = logging.getLogger(__name__)


class WfExistingAcctNewDevices:
    def __init__(self):
        log.info("Initialize new_device_existing_user.")
        """Step #0: Create Test constants and variables like sn, mac, system under test, device_category, device_type"""
        self.end_username = RandomGenUtils.random_string_of_chars(7)
        self.cluster = ExistingUserAcctDevices.login_page_url
        self.email_IdRand = "hcloud203+" + str(self.end_username) + "@gmail.com"
        self.app_api_hostname = ExistingUserAcctDevices.app_api_hostname
        self.dev_constants = AOPDeviceConstants.generate_devices_details()
        self.admin_pcid_name = ExistingUserAcctDevices.test_data.get("tac_admin_pcid1_name")
        self.pcid_name = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1_name"]
        self.acc2_pcid_name = ExistingUserAcctDevices.test_data.get("brnf_existing_acct2_new_devices_pcid1_name")
        self.acc2_pcid = ExistingUserAcctDevices.test_data.get("brnf_existing_acct2_new_devices_pcid1")
        self.msp_pcid_name = \
            ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid_name"]
        self.expiring_subscriptions = \
            (ExistingUserAcctDevices.test_data.get("brnf_existing_acct_new_devices_iap_lic_key"),
             ExistingUserAcctDevices.test_data.get("brnf_existing_acct_new_devices_gw_lic_key"),
             ExistingUserAcctDevices.test_data.get("brnf_existing_acct_new_devices_sw_lic_key"))

    def existing_acct_create_device_of_type(self, device_type, devices_count=1, **kw):
        """Create a device of given type in the account
           :param device_type: type of device to be created (IAP, STORAGE, SWITCH, COMPUTE, GATEWAY)
           :param devices_count: count of devices to be added to returned dictionary.
        """
        aop_client = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_id"]
        aop_secret = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_secret"]
        return ManufactureDevicesHelper(aop_client, aop_secret, self.dev_constants) \
            .create_device_of_type(device_type, devices_count, **kw)

    def wf_ui_add_device(self, browser_instance, storage_state_path, devices_details) -> bool:
        """Step #5: Add device claim for device's serial number."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_devices()
            devices_inventory = DevicesInventory(page, self.cluster).wait_for_loaded_state()

            # Get details of first device of each type in devices_details dictionaries
            devices_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)

            DeviceInventoryHelper.claim_ordered_network_devices(devices_inventory, devices_details)

            for device_details in devices_details:
                serial_no = device_details["serial_no"]
                devices_inventory \
                    .search_for_text(serial_no) \
                    .should_have_row_with_text_in_column("Serial Number", serial_no)

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_ui_add_network_csv_device(self, browser_instance, storage_state_path, csv_file) -> bool:
        """Step #_: Add device claim for device's CSV file."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_devices()
            add_devices_page = DevicesInventory(page, self.cluster).click_add_devices() \
                .select_device_type("Networking Devices") \
                .click_next_button() \
                .pickup_upload_device_csv_file(csv_file) \
                .click_finish_button()
            add_devices_page.close_popup()

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    @staticmethod
    def verify_device_claimed(device_order, ui_doorway):
        claimed_device = None
        search_request = {
            "unassigned_only": False,
            "archive_visibility": "HIDE_ARCHIVED",
            "search_string": device_order.get("serial_no")
        }
        devices = []
        start_time = datetime.now()
        while not devices and datetime.now() < start_time + timedelta(seconds=15):
            time.sleep(2)
            devices = ui_doorway.filter_devices(payload=search_request).get("devices")
        for device in devices:
            if device.get("serial_number") == device_order.get("serial_no"):
                claimed_device = device
                break
        return claimed_device

    def wf_dev_claim_audit_log_info(self, browser_instance, storage_state_path, devices_details) -> bool:
        """Step #6: Check add device claim info for device's serial number."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_manage()
            audit_logs = ManageAccount(page, self.cluster).open_audit_logs().wait_for_loaded_table()

            # Get details of first device of each type in devices_details dictionaries
            devices = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)
            for device in devices:
                AuditLogsVerifier.check_device_events(audit_logs, [LogsEventType.CLAIM], device)

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_sm_audit_log_info(
            self, browser_instance, storage_state_path, devices_details, brnf_sa_user_login_load_account
    ) -> bool:
        """Step #15: Check subscription for device's serial number."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_manage()
            audit_logs = ManageAccount(page, self.cluster).open_audit_logs().wait_for_loaded_table()

            for device in ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details):
                device_type = device["device_type"]
                part_no = self.dev_constants["DEFAULT_PART_MAP"][device_type]
                subscr_key = UiDoorwayDevices.get_subscription_key(device_type, device["serial_no"], part_no,
                                                                   brnf_sa_user_login_load_account)
                AuditLogsVerifier.check_device_events(audit_logs, [LogsEventType.SUBSCRIPTION], device,
                                                      subscr_key=subscr_key)

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_users_page(self, browser_instance, storage_state_path) -> bool:
        """Step #18: Check user at Users page."""
        log.info(f"Playwright: verifying logged in user at Users page.")

        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_manage()
            users_page = ManageAccount(page, self.cluster).open_identity_and_access().open_users()
            users_page \
                .wait_for_loaded_table() \
                .should_contain_text_in_title(self.pcid_name) \
                .search_for_text(ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_username"]) \
                .should_have_rows_count(1) \
                .should_contain_text_in_table(ExistingUserAcctDevices.test_data[
                                                  "brnf_existing_acct_new_devices_username"]) \
                .should_have_row_with_text_in_column("Email",
                                                     ExistingUserAcctDevices.test_data[
                                                         "brnf_existing_acct_new_devices_username"])

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_roles_page(self, browser_instance, storage_state_path) -> bool:
        """Step #19: Check role at Roles page."""
        log.info(f"Playwright: verifying existing role at Roles page.")

        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_manage()
            roles_page = ManageAccount(page, self.cluster).open_identity_and_access().open_roles_and_permissions()

            roles_page \
                .wait_for_loaded_table() \
                .should_contain_text_in_title("Roles & Permissions") \
                .should_have_search_field() \
                .search_for_text("Account Administrator") \
                .should_have_rows_count(1) \
                .should_contain_text_in_table("Account Administrator Role") \
                .should_have_row_with_text_in_column("Description", "Account Administrator Role")

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_devices_page(self, browser_instance, storage_state_path, devices_details) -> bool:
        """Step #42: Check Devices page."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_devices()
            devices_inventory = DevicesInventory(page, self.cluster).wait_for_loaded_table()
            devices_inventory.should_have_search_field()

            # Get details of first device of each type in devices_details dictionaries
            device1, device2, device3 = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)
            ActivateInventoryVerifier.check_devices_inventory(devices_inventory, device1)
            ActivateInventoryVerifier.check_devices_inventory(devices_inventory, device2)
            ActivateInventoryVerifier.check_devices_inventory(devices_inventory, device3)

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_applications_page(self, browser_instance, storage_state_path) -> bool:
        """Step #43: Check Applications page title."""
        log.info(f"Playwright: verifying logged in user at Users page.")

        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_applications()
            applications_page = MyApplications(page, self.cluster).wait_for_loaded_list()
            applications_page.should_have_text_in_title("My Services")  # Service-centric UI change

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_subscriptions_page(self, browser_instance, storage_state_path, devices_details) -> bool:
        """Step #44: Check Device Subscription."""
        log.info(f"Playwright: verifying subscription at Device Subscriptions page.")

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_devices()
            DevicesInventory(page, self.cluster).side_menu.navigate_to_dev_subscriptions()
            device_subscriptions = DeviceSubscriptions(page, self.cluster).wait_for_loaded_table()

            # Get details of first device of each type in devices_details dictionaries
            device1, device2, device3 = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)
            SmVerifier.check_device_subscription(device_subscriptions, device1)
            SmVerifier.check_device_subscription(device_subscriptions, device2)
            SmVerifier.check_device_subscription(device_subscriptions, device3)

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def verify_reassign_to_expired_subscription(
            self, browser_instance, storage_state_path, devices_details, subscr_details) -> bool:
        """Step #8: Check that specified subscription is not present in list of available subscriptions
            of apply-subscription wizard."""
        log.info(f"Playwright: verifying subscription at Device Subscriptions page.")

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        device_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)[0]
        serial_no = device_details.get("serial_no")
        subscr_key = subscr_details["key"]
        subscr_tier = subscr_details["tier"]

        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_devices()
            devices_inventory_page = DevicesInventory(page, self.cluster)
            devices_inventory_page \
                .search_for_text(serial_no) \
                .should_have_rows_count(1) \
                .select_rows_with_text_in_column("Serial Number", serial_no) \
                .detach_subscription() \
                .should_have_row_with_values_in_columns({"Serial Number": serial_no,
                                                         "Subscription Tier": "--"}) \
                .select_rows_with_text_in_column("Serial Number", serial_no)

            model = \
                devices_inventory_page.table_utils.get_column_value_from_matched_row({"Serial Number": serial_no},
                                                                                     "Model")
            devices_inventory_page.should_subscr_apply_be_unavailable(model, subscr_tier, subscr_key)

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_expire_subscription(self, browser_instance, storage_state_path, subscr_details) -> bool:
        """Step #6: Set subscription expiration to the past date."""
        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        subscr_key = subscr_details["key"]
        log.info(f"Playwright: expire subscription '{subscr_key}' by TAC.")
        target_end_date_str = (date.today() - timedelta(days=1)).strftime("%m/%d/%Y")  # expiration date - yesterday

        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name_tac(self.admin_pcid_name) \
                .wait_for_loaded_state() \
                .open_manage_ccs() \
                .side_menu.navigate_to_customers()
            TacCustomersPage(page, self.cluster) \
                .wait_for_loaded_table() \
                .search_for_text(self.pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Subscriptions") \
                .wait_for_loaded_table() \
                .search_for_text(subscr_key) \
                .should_have_rows_count(1) \
                .modify_subscription(subscr_key, target_end_date_str) \
                .wait_for_loaded_table() \
                .should_have_row_with_values_in_columns({"Key": subscr_key, "End Date": f"{target_end_date_str} 00:00"})

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def verify_expired_subscr_detach(
            self, browser_instance, storage_state_path, devices_details, subscr_details) -> bool:
        """Step #7: Check that expired subscription detached from device."""
        log.info(f"Playwright: verifying subscription at Device Details page.")

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        device_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)[0]
        serial_no = device_details.get("serial_no")

        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_devices()
            devices_inventory_page = DevicesInventory(page, self.cluster)
            devices_inventory_page \
                .search_for_text(serial_no) \
                .should_have_rows_count(1) \
                .open_device_details_page("Serial Number", serial_no) \
                .should_not_have_subscription_key(subscr_details["key"]) \
                .should_not_have_subscription_key("--")

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_tac_move_devices_between_customers_from_athena_f(self, browser_instance,
                                                            storage_state_path,
                                                            devices_details,
                                                            initial_folder_name,
                                                            target_folder_name) -> bool:
        """Step #6: Check moving devices between allowed folders of different customers."""
        log.info("Playwright: verifying moving devices between not allowed folders via TAC Devices page.")
        devices_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)
        devices_ids = [device_details["serial_no"] for device_details in devices_details]

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name_tac(self.admin_pcid_name) \
                .wait_for_loaded_state() \
                .open_manage_ccs() \
                .side_menu.navigate_to_customers()
            customers_page = TacCustomersPage(page, self.cluster)
            devices_tab = customers_page \
                .wait_for_loaded_table() \
                .search_for_text(self.pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Devices") \
                .wait_for_loaded_table()
            for device_serial in devices_ids:
                devices_tab \
                    .search_for_text(device_serial) \
                    .should_have_row_with_values_in_columns({"Serial Number": device_serial,
                                                             "Folder": initial_folder_name})
            devices_tab.go_back_to_customers()
            customers_page.side_menu.navigate_to_devices()
            tac_devices_page = TacDevicesPage(page, self.cluster)
            tac_devices_page \
                .wait_for_loaded_table() \
                .move_devices_to_customer_folder(devices_ids, self.acc2_pcid, target_folder_name)

            tac_devices_page.side_menu.navigate_to_customers()
            customers_page \
                .wait_for_loaded_table() \
                .search_for_text(self.acc2_pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Devices") \
                .wait_for_loaded_table()

            for device_serial in devices_ids:
                devices_tab \
                    .search_for_text(device_serial) \
                    .should_have_row_with_values_in_columns({"Serial Number": device_serial,
                                                             "Folder": target_folder_name})

            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    @staticmethod
    def wf_existing_device_claim_app_assignment(
            device_type, ordered_devices, brnf_sa_login_load_account
    ):
        time.sleep(9)
        """adding delay for app provisioning to add application customer id
        Activate services for auto assignments"""
        device_list_di = {"devices": []}
        try:
            for idx in range(0, len(ordered_devices)):
                device_list_di["devices"].append(
                    {
                        "serial_number": ordered_devices[
                            "device_" + device_type + str(idx)
                            ]["serial_no"],
                        "mac_address": ordered_devices[
                            "device_" + device_type + str(idx)
                            ]["mac"],
                        "app_category": "NETWORK",
                    }
                )
        except Exception as e:
            log.warning(e)

        verify_claim_devices = brnf_sa_login_load_account.add_device_activate_inventory(
            device_list_di
        )
        if "OK" in verify_claim_devices:
            return verify_claim_devices
        else:
            return False

    @staticmethod
    def wf_existing_device_claim_with_app_api(device_type, ordered_devices, brnf_app_api_session):
        """
        Workflow to claim one or more devices of the same type using an app api
        :param device_type: Type of device to be claimed
        :param ordered_devices: device to be claimed
        :param brnf_app_api_session: Authorization bearer token
        :return: True is response status code is 200, else False
        """
        platform_cust_id = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1"]
        username = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_username"]

        try:
            for idx in range(0, len(ordered_devices)):
                serial_number = ordered_devices[f"device_{device_type}{idx}"]["serial_no"]
                mac_address = ordered_devices[f"device_{device_type}{idx}"]["mac"]
                verify_claim_devices = \
                    brnf_app_api_session.claim_device_app_api("NETWORK",
                                                              serial_number,
                                                              platform_cust_id,
                                                              username,
                                                              mac_address)
                if json.loads(verify_claim_devices.content).get('status') == 200:
                    # if the API response is 200, verify is the device is found in the customers account using
                    # get_devices_by_pcid call
                    if brnf_app_api_session.verify_device_claimed_by_pcid(platform_cust_id, serial_number):
                        log.info("Device {} is claimed by PCID {}".format(serial_number, platform_cust_id))
                    else:
                        raise ValueError("Device {} is Not claimed by PCID {}".format(serial_number, platform_cust_id))
                else:
                    raise ValueError(f"Device '{serial_number}' was not claimed. "
                                     f"Response: '{verify_claim_devices.content}'.")

        except Exception as e:
            log.warning(e)
            return False
        return True

    @staticmethod
    def wf_create_activate_verified_alias(tac_ui_doorway, alias, account_details):
        """Step #38: add end_username (alias) to the customer"""
        customer_alias_created = tac_ui_doorway.add_cm_activate_alias(alias, account_details.pcid)
        if customer_alias_created.get("response"):
            return True
        else:
            log.error("Not able to create customer alias.")
            return False

    def wf_check_device_at_msp_info(self, browser_instance, storage_state_path, devices_details) -> bool:
        """Step #39: Check device is present at device list of msp-account."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        devices_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)
        serial_numbers = [device.get("serial_no") for device in devices_details]
        app_name = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["app_name_network"]
        ztp_tenant = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]['tenant3_name']

        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster) \
                .open() \
                .go_to_account_by_name(self.msp_pcid_name) \
                .wait_for_loaded_state() \
                .nav_bar.navigate_to_devices()
            devices_inventory_page = DevicesInventory(page, self.cluster).wait_for_loaded_table()
            for serial_no in serial_numbers:
                devices_inventory_page.select_rows_with_text_in_column("Serial Number", serial_no)
            devices_inventory_page \
                .assign_devices_to_tenant(ztp_tenant) \
                .wait_for_loaded_table()
            for serial_no in serial_numbers:
                devices_inventory_page.should_have_row_with_values_in_columns({"Serial Number": serial_no,
                                                                               "Workspace": ztp_tenant,
                                                                               "Service Manager": app_name})
                model = \
                    devices_inventory_page.table_utils.get_column_value_from_matched_row({"Serial Number": serial_no},
                                                                                         "Model")
                lic_key = devices_inventory_page \
                    .select_rows_with_text_in_column("Serial Number", serial_no) \
                    .apply_subscription(model)
                devices_inventory_page \
                    .wait_for_loaded_table() \
                    .open_device_details_page("Serial Number", serial_no) \
                    .should_have_subscription_key(lic_key) \
                    .go_back_to_devices()
                devices_inventory_page.wait_for_loaded_table()

            for serial_no in serial_numbers:
                devices_inventory_page.select_rows_with_text_in_column("Serial Number", serial_no)
            devices_inventory_page \
                .archive_devices() \
                .add_filter_by_archived_visibility("Show Archived Devices Only") \
                .wait_for_loaded_table()
            for serial_no in serial_numbers:
                devices_inventory_page.should_have_row_with_values_in_columns({"Serial Number": serial_no,
                                                                               "Workspace": "--",
                                                                               "Service Manager": "--"})
            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_check_manual_claimed_device_at_msp_info(self, browser_instance, storage_state_path, user_login_load_account,
                                                   devices_details) -> bool:
        """Step #8: Check manually claimed device is present at device list and Audit Logs of msp-account."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        devices_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)
        app_name = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["app_name_network"]
        ztp_tenant = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]['tenant3_name']
        app_short_name = \
            ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]['app_short_name_network']
        check_event_types = [LogsEventType.CLAIM, LogsEventType.ASSIGN, LogsEventType.SUBSCRIPTION]

        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster) \
                .open() \
                .go_to_account_by_name(self.msp_pcid_name) \
                .wait_for_loaded_state() \
                .nav_bar.navigate_to_devices()
            devices_inventory_page = DevicesInventory(page, self.cluster)
            for device_details in devices_details:
                serial_no = device_details.get("serial_no")
                devices_inventory_page \
                    .search_for_text(serial_no, ensure_not_empty=False) \
                    .should_have_rows_count(0)

                DeviceInventoryHelper.claim_ordered_network_devices(devices_inventory_page, [device_details])

                devices_inventory_page \
                    .search_for_text(serial_no) \
                    .should_have_rows_count(1) \
                    .select_rows_with_text_in_column("Serial Number", serial_no) \
                    .assign_devices_to_tenant(ztp_tenant) \
                    .wait_for_loaded_table() \
                    .search_for_text(serial_no) \
                    .should_have_row_with_values_in_columns({"Serial Number": serial_no,
                                                             "Workspace": ztp_tenant,
                                                             "Service Manager": app_name})
                model = \
                    devices_inventory_page.table_utils.get_column_value_from_matched_row({"Serial Number": serial_no},
                                                                                         "Model")
                lic_key = devices_inventory_page \
                    .select_rows_with_text_in_column("Serial Number", serial_no) \
                    .apply_subscription(model)
                devices_inventory_page \
                    .wait_for_loaded_table() \
                    .search_for_text(serial_no) \
                    .open_device_details_page("Serial Number", serial_no) \
                    .should_have_subscription_key(lic_key) \
                    .go_back_to_devices()

                devices_inventory_page.nav_bar.navigate_to_manage()
                audit_logs_page = ManageAccount(page, self.cluster) \
                    .open_audit_logs() \
                    .wait_for_loaded_table()
                AuditLogsVerifier.check_device_events(audit_logs_page, check_event_types, device_details,
                                                      app_short_name=app_short_name, subscr_key=lic_key)
                audit_logs_page.nav_bar.navigate_to_devices()

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)
            # release licences
            self._unassign_license(user_login_load_account, devices_details)

    def wf_assign_archived_device_at_msp(self, browser_instance, storage_state_path, devices_details) -> bool:
        """Step #4: Check archived device cannot be assigned to tenant."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        device_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)[0]
        serial_no = device_details.get("serial_no")

        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster) \
                .open() \
                .go_to_account_by_name(self.msp_pcid_name) \
                .wait_for_loaded_state() \
                .nav_bar.navigate_to_devices()
            DevicesInventory(page, self.cluster) \
                .search_for_text(serial_no) \
                .should_have_rows_count(1) \
                .should_have_row_with_values_in_columns({"Serial Number": serial_no,
                                                         "Workspace": "--",
                                                         "Service Manager": "--"}) \
                .select_rows_with_text_in_column("Serial Number", serial_no) \
                .should_action_be_unavailable("Assign Devices")

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_assign_unarchived_device_at_msp(self, browser_instance, storage_state_path, devices_details) -> bool:
        """Step #5: Check unarchived device can be assigned to tenant."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        devices_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)
        serial_numbers = [device.get("serial_no") for device in devices_details]
        app_name = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["app_name_network"]
        ztp_tenant = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]['tenant3_name']

        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster) \
                .open() \
                .go_to_account_by_name(self.msp_pcid_name) \
                .wait_for_loaded_state() \
                .nav_bar.navigate_to_devices()
            devices_inventory_page = DevicesInventory(page, self.cluster).wait_for_loaded_table()
            for serial_no in serial_numbers:
                devices_inventory_page \
                    .should_have_row_with_values_in_columns({"Serial Number": serial_no,
                                                             "Workspace": "--",
                                                             "Service Manager": "--"}) \
                    .select_rows_with_text_in_column("Serial Number", serial_no)
            devices_inventory_page.unarchive_devices()
            for serial_no in serial_numbers:
                devices_inventory_page.select_rows_with_text_in_column("Serial Number", serial_no)
            devices_inventory_page.assign_devices_to_tenant(ztp_tenant).wait_for_loaded_table()
            for serial_no in serial_numbers:
                devices_inventory_page.should_have_row_with_values_in_columns({"Serial Number": serial_no,
                                                                               "Workspace": ztp_tenant,
                                                                               "Service Manager": app_name})
            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_reassign_device_to_other_tenant_msp(self, browser_instance, storage_state_path, user_login_load_account,
                                               msp_iap_subscription, devices_details) -> bool:
        """Step #9: Check device unassigned from some tenant can be assigned to other tenant."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        device_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)[0]
        serial_no = device_details.get("serial_no")
        subscr_key = msp_iap_subscription["key"]
        subscr_tier = msp_iap_subscription["tier"]
        app_name = \
            ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["app_name_network"]
        app_short_name = \
            ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["app_short_name_network"]
        reassigned_tenant = \
            ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]['tenant2_name']

        context, page = browser_page(browser_instance, storage_state_path)

        try:

            ChooseAccount(page, self.cluster) \
                .open() \
                .go_to_account_by_name(self.msp_pcid_name) \
                .wait_for_loaded_state() \
                .nav_bar.navigate_to_manage()
            audit_logs_page = ManageAccount(page, self.cluster) \
                .open_audit_logs() \
                .wait_for_loaded_table()
            initial_app_assigned, initial_app_unassigned, initial_subscr_assigned_count = \
                AuditLogsVerifier.get_matched_log_events_count(audit_logs_page,
                                                               [LogsEventType.ASSIGN,
                                                                LogsEventType.UNASSIGN,
                                                                LogsEventType.SUBSCRIPTION],
                                                               device_details,
                                                               app_short_name=app_short_name,
                                                               subscr_key=subscr_key)
            log.info(f"initial_app_assigned: {initial_app_assigned}")
            log.info(f"initial_app_unassigned: {initial_app_unassigned}")
            log.info(f"initial_subscr_assigned_count: {initial_subscr_assigned_count}")

            audit_logs_page.nav_bar.navigate_to_devices()
            devices_inventory_page = DevicesInventory(page, self.cluster)
            devices_inventory_page \
                .search_for_text(serial_no) \
                .should_have_rows_count(1) \
                .select_rows_with_text_in_column("Serial Number", serial_no) \
                .unassign_devices() \
                .should_have_row_with_values_in_columns({"Serial Number": serial_no,
                                                         "Workspace": "--",
                                                         "Service Manager": "--"}) \
                .select_rows_with_text_in_column("Serial Number", serial_no) \
                .assign_devices_to_tenant(reassigned_tenant) \
                .wait_for_loaded_table() \
                .should_have_row_with_values_in_columns({"Serial Number": serial_no,
                                                         "Workspace": reassigned_tenant,
                                                         "Service Manager": app_name})
            model = \
                devices_inventory_page.table_utils.get_column_value_from_matched_row({"Serial Number": serial_no},
                                                                                     "Model")
            devices_inventory_page \
                .select_rows_with_text_in_column("Serial Number", serial_no) \
                .apply_subscription(model, subscr_tier, subscr_key)
            devices_inventory_page.nav_bar.navigate_to_manage()

            audit_logs_page = ManageAccount(page, self.cluster) \
                .open_audit_logs() \
                .wait_for_loaded_table()

            expected_app_assigned_count = initial_app_assigned + 1
            expected_app_unassigned_count = initial_app_unassigned + 1
            expected_subscr_assigned_count = initial_subscr_assigned_count + 1
            AuditLogsVerifier.check_matched_log_event_count(audit_logs_page, LogsEventType.ASSIGN, device_details,
                                                            rows_count=expected_app_assigned_count,
                                                            app_short_name=app_short_name)
            AuditLogsVerifier.check_matched_log_event_count(audit_logs_page, LogsEventType.UNASSIGN, device_details,
                                                            rows_count=expected_app_unassigned_count,
                                                            app_short_name=app_short_name)
            AuditLogsVerifier.check_matched_log_event_count(audit_logs_page, LogsEventType.SUBSCRIPTION, device_details,
                                                            rows_count=expected_subscr_assigned_count,
                                                            subscr_key=subscr_key)

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)
            # release licences
            self._unassign_license(user_login_load_account, [device_details])

    def wf_add_tag_to_device_at_msp(self, browser_instance, storage_state_path, devices_details) -> bool:
        """Step #6: Check adding tag to device."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        device_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)[0]
        serial_no = device_details.get("serial_no")
        ztp_tenant = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]['tenant3_name']

        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster) \
                .open() \
                .go_to_account_by_name(self.msp_pcid_name) \
                .wait_for_loaded_state() \
                .nav_bar.navigate_to_devices()
            dev_inventory_page = DevicesInventory(page, self.cluster)
            dev_inventory_page \
                .search_for_text(serial_no) \
                .should_have_rows_count(1) \
                .select_rows_with_text_in_column("Serial Number", serial_no) \
                .assign_tag_to_devices("ztp_activate", ztp_tenant) \
                .wait_for_loaded_table() \
                .open_device_details_page("Serial Number", serial_no) \
                .should_have_tag("ztp_activate", ztp_tenant)

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    @staticmethod
    def wf_archive_device_api_at_msp(ui_doorway, devices_details):
        """Step #7: Check archiving device using API."""

        try:
            device_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)
            payload_data = []
            for device in device_details:
                device_data = {"serial_number": device["serial_no"], "device_type": device["device_type"]}
                payload_data.append(device_data)
            archive_response = ui_doorway.archive_device_activate_inventory(payload_data)
            if archive_response.get("message") == "All Devices updated successfully.":
                log.info(f"Device(s) archived successfully: '{payload_data}'.")
            else:
                raise ValueError(f"Failed to archive device(s) '{payload_data}'.")
            actual_devices_info = []
            for payload in payload_data:
                filtered_devices_info = \
                    ui_doorway.filter_devices(payload=payload)
                actual_devices_info.append(filtered_devices_info.get("devices"))
            return actual_devices_info
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

    def wf_verify_device_tag(self, browser_instance, storage_state_path, device_details) -> bool:
        """Step #8: Check device tag."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        serial_no = device_details.get("serial_no")
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_devices()
            dev_inventory_page = DevicesInventory(page, self.cluster)
            dev_inventory_page \
                .search_for_text(serial_no) \
                .should_have_rows_count(1) \
                .open_device_details_page("Serial Number", serial_no) \
                .should_have_tag("name1", device_details.get("device_type"))

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    @staticmethod
    def assign_subs_eval_by_key(device_type, ordered_devices, subscr_key, brnf_sa_login_load_account):
        try:
            part_number = SubscriptionData(device_type).part_number
            device_license = []
            for idx in range(0, len(ordered_devices)):
                device_license.append(
                    (
                        ordered_devices["device_" + device_type + str(idx)]["serial_no"],
                        subscr_key,
                    )
                )
            resp = False
            for index in range(3):
                resp = brnf_sa_login_load_account.assign_license_to_devices(device_license, device_type, part_number)
                if resp[0]["status"] == "SUCCESS":
                    log.info(f"Assign license response for device of '{device_type}' type: '{resp}'")
                    for idx in range(len(ordered_devices)):
                        # Store subscription_keys of licenced devices in devices' details
                        ordered_devices["device_" + device_type + str(idx)]["subscription_key"] = subscr_key
                    break
                time.sleep(5)
            return resp
        except SessionException as http_error:
            return http_error.response
        except Exception as ex:
            log.error(f"not able to license the device_type {device_type}. Error: {ex}")
            return False

    def wf_assign_subs_eval(self, device_type, ordered_devices, brnf_sa_login_load_account):
        subscr_data = SubscriptionData(device_type)
        subs_type = subscr_data.subscription_type
        part_number = subscr_data.part_number
        page_limit = 100
        expire_date_cut_off = int(datetime.today().timestamp()) * 1000
        query_params = {"limit": page_limit, "expire_date_cut_off_in_millis": expire_date_cut_off}

        try:
            for i in range(1, 10):
                license_list = brnf_sa_login_load_account.get_licenses(params=query_params)
                if len(license_list["subscriptions"]) < 14:
                    log.info(f"Number of active subscriptions: {len(license_list['subscriptions'])}")
                    time.sleep(10)
                if len(license_list["subscriptions"]) >= 14:
                    log.info(f"Number of active subscriptions: {len(license_list['subscriptions'])}")
                    break
            else:
                raise Exception("Not found license with sufficient count of subscriptions.")
        except Exception as e:
            log.error(e)
            return False

        total_count = license_list["pagination"]["total_count"]
        page_offsets = [i for i in range(0, total_count, page_limit)]
        license_key = None

        for page_offset in page_offsets:  # pagination loop
            query_params.update({"offset": page_offset})
            if page_offset > 0:
                license_list = brnf_sa_login_load_account.get_licenses(params=query_params)
            log.debug("found license for device {}: {}".format(subs_type, license_list))
            for subscription in license_list["subscriptions"]:  # top loop
                if subscription["subscription_type"] == subs_type == "CENTRAL_AP":
                    if subscription["license_tier"] == "ADVANCED":
                        subs_details = subscription
                        if self._is_actual_subs(subs_details):
                            license_key = subs_details["subscription_key"]
                            log.info(f"Found suitable subscription: {license_key}")
                            break  # exit from nested loop 2 (AP)
                elif subscription["subscription_type"] == subs_type == "CENTRAL_SWITCH":
                    if subscription["license_tier"] == "ADVANCED" and \
                            subscription["subscription_tier_description"] in [
                        "Advanced-Switch-62xx/29xx",
                        "Advanced-Switch-6200/29xx"
                    ]:
                        subs_details = subscription
                        if self._is_actual_subs(subs_details):
                            license_key = subs_details["subscription_key"]
                            log.info(f"Found suitable subscription: {license_key}")
                            break  # exit from nested loop 2 (SW)
                elif subscription["subscription_type"] == subs_type == "CENTRAL_GW":
                    if subscription["license_tier"] == "ADVANCED" and \
                            subscription["subscription_tier_description"] in [
                        "Advance-70XX",
                        "Advanced-70xx/90xx"
                    ]:
                        subs_details = subscription
                        if self._is_actual_subs(subs_details):
                            license_key = subs_details["subscription_key"]
                            log.info(f"Found suitable subscription: {license_key}")
                            break  # exit from nested loop 2 (GW)
            if license_key:
                break  # exit from pagination loop
        if not license_key:
            log.error("license key not found.")
            return False
        device_license = []
        try:
            for idx in range(0, len(ordered_devices)):
                device_license.append(
                    (
                        ordered_devices["device_" + device_type + str(idx)]["serial_no"],
                        license_key,
                    )
                )
        except Exception as e:
            log.warning(e)
        try:
            for index in range(3):
                resp = brnf_sa_login_load_account.assign_license_to_devices(
                    device_license, device_type, part_number
                )
                if resp[0]["status"] == "SUCCESS":
                    log.info(
                        "license response for device_type: {}, {}".format(
                            device_type, resp
                        )
                    )
                    for idx in range(0, len(ordered_devices)):
                        # Store subscription_keys of licenced devices in devices' details
                        ordered_devices["device_" + device_type + str(idx)]["subscription_key"] = device_license[idx][1]
                    return True
                time.sleep(5)
        except Exception as e:
            log.error(f"not able to license the device_type {device_type}. Error: {e}")
            return False

    @staticmethod
    def wf_adi_get_devices_by_acid(brnf_sa_login_load_account):
        app_adi = ActivateInventory(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_secret"],
        )
        log.info(brnf_sa_login_load_account)
        provisioned_apps = brnf_sa_login_load_account.get_provisions()
        for app in provisioned_apps["provisions"]:
            if app["provision_status"] == "PROVISIONED":
                app_cust_id = app["application_customer_id"]
                device_by_acid_list = app_adi.get_devices_by_acid(
                    application_customer_id=app_cust_id
                )
                if len(device_by_acid_list["devices"]) > 3:
                    log.info(
                        f'"subscriptions list by device_by_acid_list: {0}"'.format(
                            device_by_acid_list
                        )
                    )
                    return True
                else:
                    log.error("not able to run device_by_acid_list")
                    return False

    @staticmethod
    def wf_adi_get_devices_by_pcid(brnf_sa_login_load_account):
        app_adi = ActivateInventory(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_secret"],
        )
        log.info(brnf_sa_login_load_account)
        provisioned_apps = brnf_sa_login_load_account.get_provisions()
        for app in provisioned_apps["provisions"]:
            if app["provision_status"] == "PROVISIONED":
                platform_cust_id = app["platform_customer_id"]
                device_by_pcid_list = app_adi.get_devices_by_pcid(
                    platform_customer_id=platform_cust_id
                )
                device_list = json.loads(device_by_pcid_list.content)
                if len(device_list["devices"]) > 3:
                    log.info(f"subscriptions list by device_by_pcid_list: {device_list}.")
                    return True
                else:
                    log.error("not able to run device_by_pcid_list")
                    return False

    @staticmethod
    def wf_sm_app_subscription_info_acid(brnf_sa_login_load_account, secondary=None):
        app_sm = SubscriptionManagementApp(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_secret"],
        )
        log.info(brnf_sa_login_load_account)
        provisioned_apps = brnf_sa_login_load_account.get_provisions()
        for app in provisioned_apps["provisions"]:
            if app["provision_status"] == "PROVISIONED":
                app_cust_id = app["application_customer_id"]
                platform_cust_id = app["platform_customer_id"]
                sm_app_subs_by_acid = app_sm.get_sm_app_subscription_devices(
                    platform_cust_id, app_cust_id, secondary=secondary
                )
                log.info(sm_app_subs_by_acid)
                if len(sm_app_subs_by_acid["subscription_assignments"]) > 3:
                    log.info("subscriptions list by sm_app_subs_by_acid: {0}"
                             .format(len(sm_app_subs_by_acid["subscription_assignments"]
                                         )
                                     )
                             )
                    return True
                else:
                    log.error("not able to run sm_app_subs_by_acid")
                    return False

    @staticmethod
    def wf_sm_app_subscription_info_pcid(brnf_sa_login_load_account, secondary=None):
        app_sm = SubscriptionManagementApp(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_secret"],
        )
        log.info(brnf_sa_login_load_account)
        provisioned_apps = brnf_sa_login_load_account.get_provisions()
        for app in provisioned_apps["provisions"]:
            if app["provision_status"] == "PROVISIONED":
                platform_cust_id = app["platform_customer_id"]
                sm_app_subs_by_pcid = app_sm.get_sm_app_subscription_info_pcid(
                    platform_cust_id, secondary=secondary
                )
                if len(sm_app_subs_by_pcid["subscriptions"]) >= 14:
                    log.info(
                        f'"subscriptions list by sm_app_subs_by_pcid: {0}"'.format(
                            sm_app_subs_by_pcid
                        )
                    )
                    return True
                else:
                    log.error("not able to run sm_app_subs_by_pcid")
                    return False

    def brnf_sa_nw_device_firmware(self, ordered_devices, device_type, endpoint, x_type, fw_version):
        """
         Device firmware call for firmware checks, upgrade, base firmware version for IAP device.
            :param ordered_devices: device to be claimed.
            :param device_type: type of device to make firmware call
            :param endpoint: firmware endpoint for IAP device
            :param x_type: firmware request for firmware checks, upgrade, base firmware version for IAP device
            :param fw_version: firmware version for IAP device
            :return: firmware response of IAP formware call
        """
        serial_number = ordered_devices[f"device_{device_type}0"]["serial_no"]
        mac_address = ordered_devices[f"device_{device_type}0"]["mac"]
        part_number = self.dev_constants["DEFAULT_PART_MAP"][device_type]
        certs = ExistingUserAcctDevices.iap_certs
        aruba_device_url = ExistingUserAcctDevices.aruba_device_url
        cluster_device_url = ExistingUserAcctDevices.ccs_activate_v1_device_url
        make_add_iap_device_call = NetworkStorageComputeDeviceProvisionHelper(
            cluster_device_url,
            serial_number,
            part_number,
            device_type,
            certs,
            aruba_device_url=aruba_device_url,
            mac_address=mac_address,
        )
        return make_add_iap_device_call.add_call_firmware(endpoint, x_type, fw_version)

    def brnf_sa_nw_device_prov(self, ordered_devices, device_type):
        serial_number = ordered_devices[f"device_{device_type}0"]["serial_no"]
        mac_address = ordered_devices[f"device_{device_type}0"]["mac"]
        part_number = self.dev_constants["DEFAULT_PART_MAP"][device_type]
        certs = ExistingUserAcctDevices.iap_certs
        aruba_device_url = ExistingUserAcctDevices.aruba_device_url
        cluster_device_url = ExistingUserAcctDevices.ccs_activate_v1_device_url
        make_add_iap_device_call = NetworkStorageComputeDeviceProvisionHelper(
            cluster_device_url,
            serial_number,
            part_number,
            device_type,
            certs,
            aruba_device_url=aruba_device_url,
            mac_address=mac_address,
        )
        return make_add_iap_device_call.iap_add_call_fn()

    def brnf_sa_switch_device_prov(self, ordered_devices, device_type, api_path, x_type):
        serial_number = ordered_devices[f"device_{device_type}0"]["serial_no"]
        mac_address = ordered_devices[f"device_{device_type}0"]["mac"]
        part_number = self.dev_constants["DEFAULT_PART_MAP"][device_type]
        certs = ExistingUserAcctDevices.storage_certs
        activate_v2_device_url = ExistingUserAcctDevices.aruba_switch_device_url
        cluster_device_url = ExistingUserAcctDevices.ccs_activate_v2_device_url
        make_switch_device_call = NetworkStorageComputeDeviceProvisionHelper(
            cluster_device_url,
            serial_number,
            part_number,
            device_type,
            certs,
            activate_v2_device_url=activate_v2_device_url,
            mac_address=mac_address,
        )
        return make_switch_device_call.make_switch_provision_request(api_path, x_type)

    @staticmethod
    def wf_new_device_app_assignment(device_type,
                                     devices_details,
                                     brnf_sa_login_load_account
                                     ):
        part_number = ActivateInventoryPartMap.activate_inventory_part_map(device_type)
        appid = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_app_id"]
        application_instance_id = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_app_instance"]
        '''adding delay for app provisioning to add application customer id 
        Activate services for auto assignments'''
        device_data = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)
        device_sn = device_data[0]["serial_no"]
        device_list = [{"serial_number": device_sn,
                        "device_type": device_type,
                        "part_number": part_number}]
        for i in range(2):
            verify_claim_devices = brnf_sa_login_load_account \
                .assign_devices_to_app_in_activate_inventory(device_list,
                                                             appid,
                                                             application_instance_id)

            if verify_claim_devices == "OK":
                return verify_claim_devices
            else:
                time.sleep(3)
        return False

    def tac_webui_login(self, login_info, browser):
        with browser.new_context(record_video_dir=RECORD_DIR) as context:
            with context.new_page() as page:
                Login(page, self.cluster) \
                    .open() \
                    .login_acct_tac(login_info.user, login_info.password, self.admin_pcid_name) \
                    .go_to_account_by_name_tac(self.admin_pcid_name) \
                    .wait_for_loaded_state()
                storage_state_path = os.path.join(RECORD_DIR, "brnf_tac_new_dev_logged_in_state.json")
                context.storage_state(path=storage_state_path)
        return storage_state_path

    def _unassign_license(self, user_login_load_account, devices_details):
        payload = []
        for device_details in devices_details:
            device_type = device_details["device_type"]
            payload.append({"serial_number": device_details["serial_no"],
                            "part_number": self.dev_constants["DEFAULT_PART_MAP"][device_type],
                            "device_type": device_type})
        user_login_load_account.unassign_license_from_devices(payload)

    def _is_actual_subs(self, subs_details: dict, seats_required=2):
        usage_allowed = subs_details["subscription_key"] not in self.expiring_subscriptions
        subscription_end = subs_details.get("appointments", {}).get("subscription_end", 0) // 1000
        current_date = int(datetime.today().timestamp())
        available_quantity = subs_details.get("available_quantity")
        return usage_allowed and subscription_end > current_date and available_quantity >= seats_required
