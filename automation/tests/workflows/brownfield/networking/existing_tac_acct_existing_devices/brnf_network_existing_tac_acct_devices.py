import logging
import os

from automation.conftest import ExistingUserAcctDevices
from automation.constants import RECORD_DIR
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.choose_account_page import ChooseAccount
from hpe_glcp_automation_lib.libs.adi.ui.rule_data import RuleData
from hpe_glcp_automation_lib.libs.authn.ui.login_page import Login
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_customer_details_page import TacCustomerDetailsPage
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_customers_page import TacCustomersPage
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_devices_page import TacDevicesPage
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_folder_details_page import TacFolderDetails
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_subscriptions_page import TacSubscriptionsPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import browser_stop, browser_page

log = logging.getLogger(__name__)


class WfExistingTacExistingDevices:

    def __init__(self):
        log.info("Initialize existing_device_existing_tac_user.")
        """Step #0: Create Test constants and variables like sn, mac, system under test, device_category, device_type"""
        self.cluster = ExistingUserAcctDevices.login_page_url
        self.app_api_hostname = ExistingUserAcctDevices.app_api_hostname
        self.admin_pcid = ExistingUserAcctDevices.test_data["tac_admin_pcid1"]
        self.admin_pcid_name = ExistingUserAcctDevices.test_data.get("tac_admin_pcid1_name")
        self.pcid = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1"]
        self.pcid_name = ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_name"]
        self.initial_dev_owner_pcid_name = \
            ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1_name"]
        self.rule = RuleData()

    def wf_tac_folders_page(self, browser_instance, storage_state_path, device_folder_name) -> bool:
        """Step #1: Check Device Folders creation."""
        log.info("Playwright: verifying Folder creation at TAC Folders page.")

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name_tac(self.admin_pcid_name) \
                .wait_for_loaded_state() \
                .open_manage_ccs() \
                .side_menu.navigate_to_customers()
            folders_tab = TacCustomersPage(page, self.cluster) \
                .wait_for_loaded_table() \
                .search_for_text(self.pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Folders")

            folder_description = f"{device_folder_name}_description"
            folders_tab \
                .create_new_folder(device_folder_name, description=folder_description) \
                .wait_for_loaded_table() \
                .search_for_text(device_folder_name) \
                .should_have_rows_count(1) \
                .should_have_row_with_values_in_columns({"Name": device_folder_name,
                                                         "Parent": "default",
                                                         "Description": folder_description})

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_tac_create_rule_for_folder(self, browser_instance, storage_state_path, folder_name) -> bool:
        """Step #2: Check Folder's rule creation."""
        log.info("Playwright: verifying Rule creation at TAC Folder Details page.")

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)
        self.rule.name = folder_name
        self.rule.folder = folder_name
        self.rule.type = "Notification"
        self.rule.email_on = "Firmware Upgrade"
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
                .click_tab_link("Folders") \
                .open_folder_details_page("Name", folder_name)
            TacFolderDetails(page, self.cluster) \
                .add_new_rule(self.rule) \
                .should_have_rule_in_the_list(self.rule.name) \
                .delete_rule(self.rule.name)

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_tac_edit_folder(self, browser_instance, storage_state_path, folder_name) -> bool:
        """Step #7: Check Folder's edition."""
        log.info("Playwright: verifying folder edition at TAC Customer Folders page.")

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)
        new_description = folder_name + " edited description"
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
                .click_tab_link("Folders") \
                .open_folder_details_page("Name", folder_name) \
                .edit_folder(parent=folder_name, description=new_description) \
                .go_back_to_folders()
            TacCustomerDetailsPage(page, self.cluster) \
                .click_tab_link("folders") \
                .search_for_text(folder_name) \
                .should_have_row_with_text_in_column("Description", new_description) \
                .should_have_row_with_text_in_column("Parent", folder_name)
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_tac_delete_folder(self, browser_instance, storage_state_path, folder_name) -> bool:
        """Step #9: Check Folder's deletion."""
        log.info("Playwright: verifying folder deletion at TAC Customer Folders page.")

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
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
                .click_tab_link("Folders") \
                .open_folder_details_page("Name", folder_name) \
                .delete_folder()
            TacCustomerDetailsPage(page, self.cluster) \
                .click_tab_link("folders") \
                .search_for_text(folder_name, ensure_not_empty=False) \
                .should_have_rows_count(0)
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_verify_devices_on_device_tab(self, browser_instance, storage_state_path, folder_name, devices_serials):
        """Step #3: Check moving devices between folders."""
        log.info("Playwright: verifying moving devices between folders TAC Devices page.")

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)
        device1_serial, device2_serial, device3_serial = devices_serials
        try:
            dev_tab = self._tac_move_devices_to_folder(page, folder_name, devices_serials)
            dev_tab \
                .search_for_text(device1_serial) \
                .should_have_row_with_values_in_columns({"Serial Number": device1_serial, "Folder": folder_name}) \
                .search_for_text(device2_serial) \
                .should_have_row_with_values_in_columns({"Serial Number": device2_serial, "Folder": folder_name}) \
                .search_for_text(device3_serial) \
                .should_have_row_with_values_in_columns({"Serial Number": device3_serial, "Folder": folder_name})
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_tac_move_devices_to_aruba_f_stock(self, browser_instance,
                                             storage_state_path,
                                             devices_details,
                                             initial_folder_name,
                                             target_stock_folder_name) -> bool:
        """Step #4: Check moving devices between folders of regular and Aruba-Factory-Stock customers."""
        log.info(
            "Playwright: verifying move devices between customers to Aruba-Factory-Stock folder via TAC Devices page.")
        devices_ids = [device_details["serial_number"] for device_details in devices_details]

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name_tac(self.admin_pcid_name) \
                .wait_for_loaded_state() \
                .open_manage_ccs() \
                .side_menu.navigate_to_customers()
            customers_page = TacCustomersPage(page, self.cluster)
            folders_tab = customers_page \
                .wait_for_loaded_table() \
                .search_for_text(self.initial_dev_owner_pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Folders") \
                .wait_for_loaded_table() \
                .search_for_text(initial_folder_name)
            folder_devices_initial_count = folders_tab.get_visible_devices_count_in_folder(initial_folder_name)
            folders_tab.go_back_to_customers()
            customers_page.side_menu.navigate_to_devices()
            first_device_serial = devices_details[0]["serial_number"]
            last_device_mac = devices_details[-1]["mac_address"]
            TacDevicesPage(page, self.cluster) \
                .wait_for_loaded_table() \
                .move_devices_to_customer_folder(devices_ids, "Aruba-Factory-CCS-Platform", target_stock_folder_name) \
                .search_for_text(first_device_serial) \
                .should_have_row_with_values_in_columns({"Serial Number": first_device_serial,
                                                         "Folder": target_stock_folder_name,
                                                         "Customer ID": "Aruba-Factory-CCS-Platform"}) \
                .side_menu.navigate_to_customers()
            devices_tab = TacCustomersPage(page, self.cluster) \
                .wait_for_loaded_table() \
                .search_for_text(self.initial_dev_owner_pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Devices") \
                .wait_for_loaded_table()
            # First of moved devices in list should not exist in original owner-customer - search by serial number.
            devices_tab \
                .search_for_text(first_device_serial, ensure_not_empty=False) \
                .should_have_rows_count(0)
            # Last of moved devices in list should not exist in original owner-customer - search by MAC-address.
            devices_tab \
                .search_for_text(last_device_mac, ensure_not_empty=False) \
                .should_have_rows_count(0)
            # Target folder should contain expected count of moved devices.
            folders_tab = devices_tab.click_tab_link("Folders")
            expected_dev_count = str(folder_devices_initial_count - len(devices_ids))
            folders_tab \
                .wait_for_loaded_table() \
                .search_for_text(initial_folder_name) \
                .should_have_rows_count(1) \
                .should_have_row_with_values_in_columns({"Name": initial_folder_name,
                                                         "Number of Devices": expected_dev_count}) \
                .go_back_to_customers()

            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_tac_move_devices_between_customers(self, browser_instance,
                                              storage_state_path,
                                              devices_details,
                                              folder_name) -> bool:
        """Step #4, #5: Check moving devices between folders of different customers."""
        log.info("Playwright: verifying moving devices between folders of different customers via TAC Devices page.")
        devices_ids = [device_details["serial_number"] for device_details in devices_details]

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name_tac(self.admin_pcid_name) \
                .wait_for_loaded_state() \
                .open_manage_ccs() \
                .side_menu.navigate_to_customers()
            customers_page = TacCustomersPage(page, self.cluster)
            folders_tab = customers_page \
                .wait_for_loaded_table() \
                .search_for_text(self.pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Folders") \
                .wait_for_loaded_table() \
                .search_for_text(folder_name)
            folder_devices_initial_count = folders_tab.get_visible_devices_count_in_folder(folder_name)
            folders_tab.go_back_to_customers()
            customers_page.side_menu.navigate_to_devices()
            TacDevicesPage(page, self.cluster) \
                .wait_for_loaded_table() \
                .move_devices_to_customer_folder(devices_ids, self.pcid, folder_name) \
                .side_menu.navigate_to_customers()
            devices_tab = TacCustomersPage(page, self.cluster) \
                .wait_for_loaded_table() \
                .search_for_text(self.pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Devices") \
                .wait_for_loaded_table()
            # First of moved devices in list should be present in devices list - search by serial number.
            device_details = devices_details[0]
            devices_tab \
                .search_for_text(device_details["serial_number"]) \
                .should_have_row_with_values_in_columns({"Serial Number": device_details["serial_number"],
                                                         "Folder": folder_name}) \
                .open_device_details_page("Serial Number", device_details["serial_number"]) \
                .wait_for_loaded_details() \
                .should_have_mac_address(device_details["mac_address"]) \
                .should_have_serial(device_details["serial_number"]) \
                .should_have_part_no(device_details["part_number"]) \
                .should_have_assigned_folder(folder_name) \
                .should_have_assigned_pcid(self.pcid) \
                .go_back_to_devices()
            # Last of moved devices in list should be present in devices list - search by MAC-address.
            device_details = devices_details[-1]
            devices_tab \
                .search_for_text(device_details["mac_address"]) \
                .should_have_row_with_values_in_columns({"MAC Address": device_details["mac_address"],
                                                         "Folder": folder_name}) \
                .open_device_details_page("MAC Address", device_details["mac_address"]) \
                .wait_for_loaded_details() \
                .should_have_mac_address(device_details["mac_address"]) \
                .should_have_serial(device_details["serial_number"]) \
                .should_have_part_no(device_details["part_number"]) \
                .should_have_assigned_folder(folder_name) \
                .should_have_assigned_pcid(self.pcid) \
                .go_back_to_devices()

            # Target folder should contain expected count of all moved devices.
            folders_tab = devices_tab.click_tab_link("Folders")
            expected_dev_count = str(len(devices_ids) + folder_devices_initial_count)
            folders_tab \
                .search_for_text(folder_name) \
                .should_have_rows_count(1) \
                .should_have_row_with_values_in_columns({"Name": folder_name,
                                                         "Number of Devices": expected_dev_count}) \
                .go_back_to_customers()

            # Moved device should not exist in original owner-customer
            customers_page \
                .wait_for_loaded_table() \
                .search_for_text(self.initial_dev_owner_pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Devices") \
                .wait_for_loaded_table() \
                .search_for_text(device_details["serial_number"], ensure_not_empty=False) \
                .should_have_rows_count(0)

            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_tac_move_devices_between_customers_to_athena_f(self, browser_instance,
                                                          storage_state_path,
                                                          devices_details,
                                                          initial_folder_name,
                                                          target_folder_name) -> bool:
        """Step #6: Check moving devices between not allowed folders of different customers."""
        log.info("Playwright: verifying moving devices between not allowed folders via TAC Devices page.")
        devices_ids = [device_details["serial_number"] for device_details in devices_details]

        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name_tac(self.admin_pcid_name) \
                .wait_for_loaded_state() \
                .open_manage_ccs() \
                .side_menu.navigate_to_customers()
            customers_page = TacCustomersPage(page, self.cluster)
            folders_tab = customers_page \
                .wait_for_loaded_table() \
                .search_for_text(self.pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Folders") \
                .wait_for_loaded_table() \
                .search_for_text(target_folder_name)
            folder_devices_initial_count = folders_tab.get_visible_devices_count_in_folder(target_folder_name)
            folders_tab.go_back_to_customers()
            customers_page.side_menu.navigate_to_devices()
            TacDevicesPage(page, self.cluster) \
                .wait_for_loaded_table() \
                .move_devices_to_customer_folder(devices_ids, self.pcid, target_folder_name, expect_failure=True) \
                .should_have_error_containing_text(
                f"Devices can only be moved to DEFAULT folder not to {target_folder_name}") \
                .close_move_devices_dialog() \
                .side_menu.navigate_to_customers()

            devices_tab = customers_page \
                .wait_for_loaded_table() \
                .search_for_text(self.pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Devices") \
                .wait_for_loaded_table()
            # First of the devices in list should not be present in devices list - search by serial number.
            device_details = devices_details[0]
            devices_tab \
                .search_for_text(device_details["serial_number"], ensure_not_empty=False) \
                .should_have_rows_count(0)
            # Last of the devices in list should not be present in devices list - search by MAC-address.
            device_details = devices_details[-1]
            devices_tab \
                .search_for_text(device_details["mac_address"], ensure_not_empty=False) \
                .should_have_rows_count(0)

            # Target folder should contain unchanged count of devices.
            folders_tab = devices_tab.click_tab_link("Folders")
            expected_dev_count = str(folder_devices_initial_count)
            folders_tab \
                .search_for_text(target_folder_name) \
                .should_have_rows_count(1) \
                .should_have_row_with_values_in_columns({"Name": target_folder_name,
                                                         "Number of Devices": expected_dev_count}) \
                .go_back_to_customers()

            # Devices still should exist in original owner-customer
            customers_page \
                .wait_for_loaded_table() \
                .search_for_text(self.initial_dev_owner_pcid_name) \
                .click_table_row(1) \
                .click_tab_link("Devices") \
                .wait_for_loaded_table() \
                .search_for_text(device_details["serial_number"]) \
                .should_have_row_with_values_in_columns({"Serial Number": device_details["serial_number"],
                                                         "Folder": initial_folder_name})

            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_verify_devices_on_folder_details(self, browser_instance, storage_state_path, folder_name, devices_serials):
        """Step #8: Check Folder's devices."""
        log.info("Playwright: verifying devices at TAC Folder Details page.")
        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)
        device1_serial, device2_serial, device3_serial = devices_serials
        try:
            dev_tab = self._tac_move_devices_to_folder(page, folder_name, devices_serials)
            folder_details = dev_tab.click_tab_link("Folders").open_folder_details_page("Name", folder_name)
            folder_details \
                .search_for_text(device1_serial) \
                .should_have_device_in_the_folder(device1_serial) \
                .search_for_text(device2_serial) \
                .should_have_device_in_the_folder(device2_serial) \
                .search_for_text(device3_serial) \
                .should_have_device_in_the_folder(device3_serial)
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_verify_add_alias(self, browser_instance, storage_state_path, alias_name):
        """Step #14: Check Alias successfully added."""
        log.info("Playwright: verifying aliases at TAC Aliases page.")
        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
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
                .click_tab_link("Aliases") \
                .create_new_alias(alias_name) \
                .search_for_text(alias_name) \
                .should_have_row_with_values_in_columns({"Alias Name": alias_name, "Alias Type": "CUSTOMER_NAME"})
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_verify_delete_alias(self, browser_instance, storage_state_path, alias_name):
        """Step #15: Check Alias successfully deleted."""
        log.info("Playwright: verifying aliases at TAC Aliases page.")
        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
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
                .click_tab_link("Aliases") \
                .search_for_text(alias_name) \
                .delete_alias(alias_name) \
                .search_for_text(alias_name, ensure_not_empty=False) \
                .should_have_rows_count(0)
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_generate_eval_subscription(self, ui_doorway):
        """Step #10: Check eval subscription generation"""
        log.info("Verifying eval subscription generation")
        eval_subscription = ui_doorway.create_cm_eval_subscription(self.pcid, subscription_tiers=["FOUNDATION_AP"])
        if eval_subscription and eval_subscription[0].get('platform_customer_id') == self.pcid:
            return ui_doorway.get_cm_customer_subscriptions(
                subscription_key_pattern=eval_subscription[0].get("subscription_key")
            )[0]
        else:
            return False

    def wf_modify_eval_subscription(self, ui_doorway, subscription_data, new_values):
        """Step #11,12: Check that eval subscription modified successfully"""
        log.info("Verifying eval subscription modification")
        updated_subscription = ui_doorway.update_cm_eval_subscription(
            self.pcid,
            subscription_data["subscription_key"],
            quantity_increment=new_values.get("quantity", 0),
            end_date_incremental=new_values.get("subscription_end", 0),
        )
        if updated_subscription.get("response") == "success":
            return ui_doorway.get_cm_customer_subscriptions(
                subscription_key_pattern=subscription_data.get("subscription_key")
            )[0]
        else:
            return False

    def wf_transfer_subscription(self, browser_instance, storage_state_path, subscription_data):
        """Step #13: Check that eval subscription transferred successfully"""
        log.info("Verifying eval subscription transferring")
        assert subscription_data.get("platform_customer_id") != self.admin_pcid, \
            "Subscription already belongs to destination customer"
        subs_key = subscription_data.get("subscription_key")
        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)
        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name_tac(self.admin_pcid_name) \
                .wait_for_loaded_state() \
                .open_manage_ccs() \
                .side_menu.navigate_to_subscriptions()
            TacSubscriptionsPage(page, self.cluster) \
                .wait_for_loaded_table() \
                .transfer_subscription(subs_key, self.admin_pcid) \
                .search_for_text(subs_key) \
                .should_have_row_with_text_in_column("Platform Customer ID", self.admin_pcid)
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_verify_error_transferring_subscription(self, browser_instance, storage_state_path, subscription_data):
        """Step #14: Check that assigned eval subscription cannot be transferred"""
        log.info("Verifying error on eval subscription transferring")
        assert subscription_data.get("platform_customer_id") != self.admin_pcid, \
            "Subscription already belongs to destination customer"
        subs_key = subscription_data.get("subscription_key")
        test_name = (os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0])
        context, page = browser_page(browser_instance, storage_state_path)
        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name_tac(self.admin_pcid_name) \
                .wait_for_loaded_state() \
                .open_manage_ccs() \
                .side_menu.navigate_to_subscriptions()
            subs_page = TacSubscriptionsPage(page, self.cluster) \
                .wait_for_loaded_table()
            error_message = subs_page.get_error_on_transfer_subscription(subs_key, self.admin_pcid)
            subs_page.search_for_text(subs_key) \
                .should_have_row_with_text_in_column("Platform Customer ID", self.pcid)
            return "Subscription is already assigned to a device" in error_message
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_webui_login(self, login_info, browser):
        with browser.new_context(record_video_dir=RECORD_DIR) as context:
            with context.new_page() as page:
                Login(page, self.cluster) \
                    .open() \
                    .login_acct_tac(login_info.user, login_info.password, self.admin_pcid_name) \
                    .go_to_account_by_name_tac(self.admin_pcid_name) \
                    .wait_for_loaded_state()
                storage_state_path = os.path.join(RECORD_DIR, "brnf_tac_logged_in_state.json")
                context.storage_state(path=storage_state_path)
        return storage_state_path

    def _tac_move_devices_to_folder(self, page, folder_name, devices_serials) -> TacCustomerDetailsPage:
        ChooseAccount(page, self.cluster).open() \
            .go_to_account_by_name_tac(self.admin_pcid_name) \
            .wait_for_loaded_state() \
            .open_manage_ccs() \
            .side_menu.navigate_to_customers()
        devices_tab = TacCustomersPage(page, self.cluster) \
            .wait_for_loaded_table() \
            .search_for_text(self.pcid_name) \
            .click_table_row(1) \
            .click_tab_link("Devices") \
            .wait_for_loaded_table()
        device1_serial, device2_serial, device3_serial = devices_serials
        devices_tab \
            .search_for_text(device1_serial) \
            .select_rows_with_text_in_column("Serial Number", device1_serial) \
            .move_to_folder(folder_name) \
            .wait_for_loaded_table() \
            .search_for_text(device2_serial) \
            .select_rows_with_text_in_column("Serial Number", device2_serial) \
            .move_to_folder(folder_name) \
            .wait_for_loaded_table() \
            .search_for_text(device3_serial) \
            .select_rows_with_text_in_column("Serial Number", device3_serial) \
            .move_to_folder(folder_name) \
            .wait_for_loaded_table()
        return devices_tab
