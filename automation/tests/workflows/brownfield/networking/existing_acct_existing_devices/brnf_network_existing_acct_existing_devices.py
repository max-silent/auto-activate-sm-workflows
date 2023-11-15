import logging
import os
import re
import time

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.choose_account_page import ChooseAccount
from hpe_glcp_automation_lib.libs.add.device_calls.device_prov import NetworkStorageComputeDeviceProvisionHelper
from hpe_glcp_automation_lib.libs.adi.ui.activate_folder_details_page import ActivateFolderDetails
from hpe_glcp_automation_lib.libs.adi.ui.activate_folders_page import ActivateFolders
from hpe_glcp_automation_lib.libs.adi.ui.dev_inventory_page import DevicesInventory
from hpe_glcp_automation_lib.libs.adi.ui.rule_data import RuleData
from hpe_glcp_automation_lib.libs.aop.helpers.aop_payload_constants import AOPDeviceConstants
from hpe_glcp_automation_lib.libs.authn.user_api.session.core.exceptions import SessionException
from hpe_glcp_automation_lib.libs.commons.ui.manage_account_page import ManageAccount
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import browser_page, browser_stop

from automation.configs.device_mappings.activate_inventory_device_mapping import ActivateInventoryPartMap
from automation.conftest import ExistingUserAcctDevices
from automation.local_libs.activate_inventory.activate_device_ui_utils import DeviceHistoryVerifier
from automation.local_libs.activate_inventory.activate_inventory_ui_utils import ActivateInventoryVerifier
from automation.local_libs.activate_orders.activate_orders_utils import ActivateOrdersHelper
from automation.local_libs.audit_logs.audit_logs_ui_utils import AuditLogsVerifier, LogsEventType
from automation.local_libs.ui_doorway.ui_doorway_devices_by_api import UiDoorwayDevices

log = logging.getLogger(__name__)


class WfExistingAcctExistingDevices:
    def __init__(self):
        """Step #0: Create Test constants and variables like sn, mac, system under test, device_category, device_type"""
        log.info("Initialize existing_device_existing_user.")
        self.pcid_name = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_acct1"]
        self.username = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_username"]
        self.cluster = ExistingUserAcctDevices.login_page_url
        self.app_api_url = ExistingUserAcctDevices.app_api_hostname
        self.dev_constants = AOPDeviceConstants.generate_devices_details()
        self.rule = RuleData()

    def wf_sm_activate_folder_add_rule_check(self, browser_instance, storage_state_path, folder_name):
        """ Step #11: Check that rule can be added to the folder."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)
        self.rule.name = folder_name
        self.rule.folder = folder_name
        self.rule.type = "Notification"
        self.rule.email_on = "Firmware Upgrade"

        try:
            ChooseAccount(page, self.cluster).open().go_to_account_by_name(
                self.pcid_name
            ).wait_for_loaded_state().nav_bar.navigate_to_manage()
            ManageAccount(page, self.cluster) \
                .open_activate() \
                .side_menu.navigate_to_folders()
            ActivateFolders(page, self.cluster) \
                .wait_for_loaded_table() \
                .open_folder_details(folder_name)
            ActivateFolderDetails(page, self.cluster) \
                .add_new_rule(self.rule) \
                .should_have_rule_in_the_list(self.rule.name) \
                .delete_rule(self.rule.name)
            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_sm_activate_devices_download_csv_check(self, browser_instance, storage_state_path):
        """ Step #10: Check event history for device's serial number."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open().go_to_account_by_name(
                self.pcid_name
            ).wait_for_loaded_state().nav_bar.navigate_to_manage()
            activate_devices = ManageAccount(page, self.cluster).open_activate().wait_for_loaded_table()
            activate_devices.export_inventory_csv(self.username)
            activate_devices.should_have_export_success_notification()
            activate_devices.close_success_notification()
            expected_text_regexp = \
                re.compile(r"Activate Inventory report.*successfully generated and sent to the email")
            activate_devices.should_contain_notification_banner_text(expected_text_regexp)
            activate_devices.close_notification_banner()
            # TODO: add verification of received email and/or downloaded CSV with exported report
            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_sm_device_history_check(self, browser_instance, storage_state_path, devices_details):
        """ Step #9: Check event history for device's serial number."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open().go_to_account_by_name(
                self.pcid_name
            ).wait_for_loaded_state().nav_bar.navigate_to_manage()
            activate_devices = ManageAccount(page, self.cluster).open_activate().wait_for_loaded_table()

            device1, device2, device3 = devices_details
            DeviceHistoryVerifier.check_devices_history(activate_devices, device1)
            DeviceHistoryVerifier.check_devices_history(activate_devices, device2)
            DeviceHistoryVerifier.check_devices_history(activate_devices, device3)
            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_folders_page(self, browser_instance, storage_state_path, device_folder_name) -> bool:
        """Step #18: Check Device Folders creation."""
        log.info("Playwright: verifying Folder creation at Activate Folders page.")

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_manage()
            activate_devices_page = ManageAccount(page, self.cluster).open_activate().wait_for_loaded_table()
            activate_devices_page.side_menu.navigate_to_folders()

            folders_page = ActivateFolders(page, self.cluster)
            folder_description = f"{device_folder_name}_description"
            folders_page.create_new_folder(device_folder_name, description=folder_description)
            folders_page.wait_for_loaded_table().search_for_text(device_folder_name).should_have_rows_count(1)
            folders_page.should_have_row_with_values_in_columns(
                {"Name": device_folder_name,
                 "Parent": "default",
                 "Description": folder_description})

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_sm_activate_folder_delete_check(self, browser_instance, storage_state_path, folder_name):
        """ Step #21: Check Folder's deletion."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)
        try:
            ChooseAccount(page, self.cluster).open().go_to_account_by_name(
                self.pcid_name
            ).wait_for_loaded_state().nav_bar.navigate_to_manage()
            ManageAccount(page, self.cluster) \
                .open_activate() \
                .side_menu.navigate_to_folders()
            ActivateFolders(page, self.cluster) \
                .wait_for_loaded_table() \
                .open_folder_details(folder_name) \
                .delete_folder()
            ActivateFolders(page, self.cluster) \
                .search_for_text(folder_name, ensure_not_empty=False) \
                .should_have_rows_count(0)
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_filter_devices_by_subscription_tier(self, browser_instance, storage_state_path, filtering_tiers_lists):
        """ Step #23: Check devices filtering by subscription tier."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)
        try:
            tiers_list_1, tiers_list_2, tiers_list_3, tiers_list_4 = filtering_tiers_lists
            ChooseAccount(page, self.cluster).open().go_to_account_by_name(
                self.pcid_name
            ).wait_for_loaded_state().nav_bar.navigate_to_devices()
            devices_inventory_page = DevicesInventory(page, self.cluster)
            ActivateInventoryVerifier.check_devices_filtering_by_tier(devices_inventory_page, tiers_list_1)
            ActivateInventoryVerifier.check_devices_filtering_by_tier(devices_inventory_page, tiers_list_2)
            ActivateInventoryVerifier.check_devices_filtering_by_tier(devices_inventory_page, tiers_list_3)
            ActivateInventoryVerifier.check_devices_filtering_by_tier(devices_inventory_page, tiers_list_4)
            combined_tiers_list = tiers_list_1 + tiers_list_4
            ActivateInventoryVerifier.check_devices_filtering_by_tier(devices_inventory_page, combined_tiers_list)
            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_sm_audit_log_info(self, browser_instance, storage_state_path, devices_details,
                             brnf_sa_user_login_load_account) -> bool:
        """ Step #8: Check subscription for device's serial number."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open().go_to_account_by_name(
                self.pcid_name
            ).wait_for_loaded_state().nav_bar.navigate_to_manage()
            audit_logs = ManageAccount(page, self.cluster).open_audit_logs().wait_for_loaded_table()

            for device in devices_details:
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

    def wf_existing_device_app_assignment(self,
                                          device_type,
                                          device_data,
                                          brnf_sa_login_load_account,
                                          appid,
                                          application_instance_id):
        part_number = ActivateInventoryPartMap.activate_inventory_part_map(device_type)
        time.sleep(9)
        '''adding delay for app provisioning to add application customer id 
        Activate services for auto assignments'''
        device_list = [{"serial_number": device_data,
                        "device_type": device_type,
                        "part_number": part_number}]
        try:
            brnf_sa_login_load_account.unarchive_device_activate_inventory(device_list)
        except Exception as e:
            log.info(f"device is already in unarchive state, unarchive before assigning. Error: {e}")
            pass

        try:
            brnf_sa_login_load_account.unassign_devices_from_app_in_activate_inventory(device_list)
        except Exception as e:
            log.info(f"device in assign state, unassign before assigning. Error: {e}")
            pass
        time.sleep(10)
        verify_claim_devices = brnf_sa_login_load_account \
            .assign_devices_to_app_in_activate_inventory(device_list,
                                                         appid,
                                                         application_instance_id)
        if verify_claim_devices == "OK":
            return verify_claim_devices
        else:
            return False

    def brnf_sa_nw_device_prov(self, serial_number, mac_address, device_type):
        part_number = self.dev_constants['DEFAULT_PART_MAP'][device_type]
        certs = ExistingUserAcctDevices.iap_certs
        aruba_device_url = ExistingUserAcctDevices.aruba_device_url
        cluster_device_url = ExistingUserAcctDevices.ccs_activate_v1_device_url
        make_add_iap_device_call = NetworkStorageComputeDeviceProvisionHelper(cluster_device_url,
                                                                              serial_number,
                                                                              part_number,
                                                                              device_type,
                                                                              certs,
                                                                              aruba_device_url=aruba_device_url,
                                                                              mac_address=mac_address)
        return make_add_iap_device_call.iap_add_call_fn()

    @staticmethod
    def check_iaas_license_key_assign_to_device(device_type, serial, license_key, brnf_sa_login_load_account):
        if "COMPUTE" in device_type:
            part_number = "P28948-B21"
        elif "STORAGE" in device_type:
            part_number = "6050"

        params = {"subscription_key": license_key}
        try:
            license_list = brnf_sa_login_load_account.get_licenses(params=params)
        except Exception as e:
            log.info(e)
            return False
        log.info("found license for device: {}".format(license_list))

        if not license_list['subscriptions'][0]['subscription_key']:
            log.error("license key not found.")
            return False
        log.info("License key found in details: {}".format(license_list['subscriptions'][0]['subscription_key']))
        log.info("Assign license, {}, to device.".format(license_key))
        device_license = [(serial, license_key)]
        try:
            resp = brnf_sa_login_load_account.assign_license_to_devices(device_license, device_type, part_number)
            if resp[0]['status'] == "SUCCESS":
                log.info("license response for device_type: {}, {}".format(device_type, resp))
                return resp
        except Exception as e:
            log.error(f"not able to license the device_type {device_type}. Error: {e}")
            return False

    @staticmethod
    def wf_sa_manual_claim_already_claimed_device(ui_doorway, serial_no, mac):
        device_payload = {
            "devices": [
                {
                    "serial_number": serial_no,
                    "mac_address": mac,
                    "app_category": "NETWORK"
                }
            ]
        }
        try:
            ui_doorway.add_device_activate_inventory(device_payload)
            return False
        except SessionException as ex:
            log.info(f"Expected error: {ex}")
            return ex.response.content

    @staticmethod
    def wf_verify_device_has_app_assignment(ui_doorway, serial_no, acid):
        filter_payload = {
            "serial_number": serial_no,
            "archive_visibility": "HIDE_ARCHIVED"
        }
        filtering_result = ui_doorway.filter_devices(filter_payload)
        for device in filtering_result.get("devices", []):
            if device.get("application_customer_id") == acid:
                return True
        return False

    def check_already_claimed_device_upload_via_csv(self, browser_instance, storage_state_path):
        """
        Step #24-1: Check that already claimed and assigned device cannot be claimed by other account via CSV upload.
        """
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)
        claimed_iap_serial_no = ExistingUserAcctDevices.test_data[
            "brnf_existing_acct_existing_devices_iap_serial_subs_mgmt"]
        claimed_iap_mac = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_iap_mac_subs_mgmt"]
        claimed_sw_serial_no = ExistingUserAcctDevices.test_data[
            "brnf_existing_acct_existing_devices_sw_serial_subs_mgmt"]
        claimed_sw_mac = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_sw_mac_subs_mgmt"]
        device_info = [
            {
                "serial_no": claimed_iap_serial_no,
                "mac": claimed_iap_mac,
                "device_type": "NETWORK"
            },
            {
                "serial_no": claimed_sw_serial_no,
                "mac": claimed_sw_mac,
                "device_type": "NETWORK"
            }
        ]
        device_csv = ActivateOrdersHelper.generate_device_csv(device_info, filename="claimed_device.csv")
        second_user_pcid_name = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1_name"]
        try:
            ChooseAccount(page, self.cluster).open().go_to_account_by_name(
                second_user_pcid_name
            ).wait_for_loaded_state().nav_bar.navigate_to_devices()
            add_device = DevicesInventory(page, self.cluster).click_add_devices() \
                .select_device_type("Networking Devices") \
                .click_next_button() \
                .pickup_upload_device_csv_file(device_csv) \
                .click_finish_button()
            add_device.close_popup()
            DevicesInventory(page, self.cluster) \
                .search_for_text(claimed_iap_serial_no, ensure_not_empty=False) \
                .should_have_rows_count(0) \
                .search_for_text(claimed_sw_serial_no, ensure_not_empty=False) \
                .should_have_rows_count(0)
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def check_claimed_device_remains_claimed(self, browser_instance, storage_state_path):
        """
        Step #24-2: Check that already claimed and assigned device cannot be claimed by other account via CSV upload.
        """
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open().go_to_account_by_name(
                self.pcid_name
            ).wait_for_loaded_state().nav_bar.navigate_to_devices()
            DevicesInventory(page, self.cluster) \
                .search_for_text(ExistingUserAcctDevices.test_data[
                                     "brnf_existing_acct_existing_devices_iap_serial_subs_mgmt"]) \
                .should_have_rows_count(1) \
                .search_for_text(ExistingUserAcctDevices.test_data[
                                     "brnf_existing_acct_existing_devices_sw_serial_subs_mgmt"]) \
                .should_have_rows_count(1)
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def brnf_sa_device_est_prov(self, device_type, serial_number, mac_address, part_number):
        """
         To make /estprovision call for VGW/NONTPM device
            :param device_type: type of device to make est provision
            :param serial_number: serial number of VGW/NONTPM  device
            :param mac_address: mac address of VGW/NONTPM  device
            :param part_number: part number of VGW/NONTPM  device
            :return: est provision response for VGW/NONTPM  device.
        """
        aruba_device_url = ExistingUserAcctDevices.aruba_device_url
        cluster_device_url = ExistingUserAcctDevices.ccs_activate_v1_device_url
        make_device_call = NetworkStorageComputeDeviceProvisionHelper(
            cluster_device_url,
            serial_number,
            part_number,
            device_type,
            certs=None,
            aruba_device_url=aruba_device_url,
            mac_address=mac_address
        )
        return make_device_call.est_provision_request()

    def brnf_sa_verify_est(self, device_type, serial_number, mac_address, part_number, username, device_payload):
        """
         To make /verifyestchallenge for VGW/NONTPM device
            :param device_type: type of device to make est provision
            :param serial_number: serial number of device
            :param mac_address: mac address of device
            :param part_number: part number of device
            :param username: serial, part, mac and device model detail
            :param device_payload: payload data of device for request
            :return: est verify challenge response for VGW device.
        """
        aruba_device_url = ExistingUserAcctDevices.aruba_device_url
        cluster_device_url = ExistingUserAcctDevices.ccs_activate_v1_device_url
        verify_est_call = NetworkStorageComputeDeviceProvisionHelper(
            cluster_device_url,
            serial_number,
            part_number,
            device_type,
            certs=None,
            aruba_device_url=aruba_device_url,
            mac_address=mac_address
        )
        return verify_est_call.est_verify_challenge(username, device_payload)

    def brnf_sa_switch_device_prov(self, device_type, serial_number, mac_address, part_number, api_path, x_type):
        """
         To make /verifyestchallenge for VGW/NONTPM device
            :param device_type: type of device to make device provision
            :param serial_number: serial number of device
            :param mac_address: mac address of device
            :param part_number: part number of device
            :param api_path: endpoint for device provision call
            :param x_type: x_type of device for request
            :return: switch provision response for VGW device.
        """
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

    def brnf_nw_device_prov(self, serial_number, mac_address, device_type, part_number):
        certs = ExistingUserAcctDevices.iap_certs
        aruba_device_url = ExistingUserAcctDevices.aruba_device_url
        cluster_device_url = ExistingUserAcctDevices.ccs_activate_v1_device_url
        make_add_iap_device_call = NetworkStorageComputeDeviceProvisionHelper(cluster_device_url,
                                                                              serial_number,
                                                                              part_number,
                                                                              device_type,
                                                                              certs,
                                                                              aruba_device_url=aruba_device_url,
                                                                              mac_address=mac_address)
        return make_add_iap_device_call.iap_add_call_fn()