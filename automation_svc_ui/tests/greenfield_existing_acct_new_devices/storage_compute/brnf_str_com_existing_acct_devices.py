import json
import logging
import os
import random
import string
import time
from datetime import datetime, timedelta

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.choose_account_page import ChooseAccount
from hpe_glcp_automation_lib.libs.add.device_calls.device_prov import (
    NetworkStorageComputeDeviceProvisionHelper,
)
from hpe_glcp_automation_lib.libs.adi.app_api.adi_app_api import ActivateInventory
from hpe_glcp_automation_lib.libs.adi.ui.dev_inventory_page import DevicesInventory
from hpe_glcp_automation_lib.libs.aop.helpers.aop_order_device_helper import (
    NewDeviceOrder,
)
from hpe_glcp_automation_lib.libs.aop.helpers.aop_payload_constants import (
    AOPDeviceConstants,
)
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import browser_page, browser_stop

from automation_svc_ui.conftest import ExistingUserAcctDevices, NewUserAcctDevices
from automation_svc_ui.local_libs.activate_devices.manufacture_order_utils import ManufactureDevicesHelper
from automation_svc_ui.local_libs.activate_orders.activate_orders_utils import ActivateOrdersHelper

log = logging.getLogger(__name__)


class WfScExistingAcctDevices:
    def __init__(self):
        log.info("Initialize new_device_existing_user.")
        """Step #0: Create Test constants and variables like sn, mac, system under test, device_category, device_type"""
        end_username = "".join(random.choice(string.ascii_lowercase) for _ in range(7))
        self.cluster = ExistingUserAcctDevices.login_page_url
        self.email_IdRand = "hcloud203+" + str(end_username) + "@gmail.com"
        self.end_username = "".join(
            random.choice(string.ascii_lowercase) for _ in range(7)
        )
        self.app_api_hostname = ExistingUserAcctDevices.app_api_hostname
        self.pcid_name = ExistingUserAcctDevices.test_data["brnf_sc_pcid_name"]
        self.dev_constants = AOPDeviceConstants.generate_devices_details()

    def existing_acct_sc_create_device_fn(self, device_type, devices_count=1, lic_devices=None, **kwargs):
        """Step # 1: Create 1 iap devices"""
        aop_client = ExistingUserAcctDevices.test_data["brnf_sc_api_client_id"]
        aop_secret = ExistingUserAcctDevices.test_data["brnf_sc_api_client_secret"]
        return ManufactureDevicesHelper(aop_client, aop_secret, self.dev_constants) \
            .create_device_of_type(device_type, devices_count, lic_devices=lic_devices, **kwargs)

    def existing_acct_sc_create_device_for_iaas(self, device_type, subs_device_list):
        """
        Create gecko/iaas devices
        :params device_type: type of the device
        :params device_list: list of gecko/iaas devices
        :return device_info: s/n, mac, if applicable for storage/compute devices part_number, entitlements
        """
        number_of_devices = len(subs_device_list)
        device_info = {}
        device_list = []
        device_count = number_of_devices
        for num in range(0, device_count):
            init_dev_constants = AOPDeviceConstants()
            dev_constants = init_dev_constants.new_mfr_device_constants()
            serial = subs_device_list[num]["serial"]
            mac = dev_constants[device_type + "_mac"]
            aop_sso_url = ExistingUserAcctDevices.test_data["sso_host"]
            aop_client = ExistingUserAcctDevices.test_data["brnf_sc_api_client_id"]
            aop_secret = ExistingUserAcctDevices.test_data["brnf_sc_api_client_secret"]

            device_category = dev_constants["device_category_compute"]
            init_new_device_order = NewDeviceOrder(
                self.app_api_hostname,
                device_category,
                device_type,
                serial,
                mac,
                self.cluster,
                self.end_username,
                aop_sso_url,
                aop_client,
                aop_secret,
            )
            part = subs_device_list[num]["material"]

            mfr_device = init_new_device_order.create_manufacturing(part)
            init_new_device_order.create_pos_order()
            init_new_device_order.create_sds_order(part)
            if not mfr_device:
                log.error("not able to manufacture the device")
                return False
            device_info["device_" + str(device_type) + str(num)] = {}
            device_info["device_" + str(device_type) + str(num)]["serial_no"] = serial
            device_info["device_" + str(device_type) + str(num)]["mac"] = mac
            device_info["device_" + str(device_type) + str(num)]["part_num"] = part

        device_list.append(device_info)
        log.info("List of created devices {}".format(device_list))
        if len(device_list) != number_of_devices:
            log.info("Not able to create devices in AOP")
            return False
        else:
            NewUserAcctDevices.iap_device_list = device_info
            log.info(device_info)
            return device_info

    @staticmethod
    def wf_sc_adi_get_devices_by_acid(brnf_sa_login_load_account):
        app_adi = ActivateInventory(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["brnf_sc_api_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["brnf_sc_api_client_secret"],
        )
        log.info(brnf_sa_login_load_account)
        provisioned_apps = brnf_sa_login_load_account.get_provisions()
        for app in provisioned_apps["provisions"]:
            if app["provision_status"] == "PROVISIONED":
                app_cust_id = app["application_customer_id"]
                device_by_acid_list = app_adi.get_devices_by_acid(
                    application_customer_id=app_cust_id
                )
                if len(device_by_acid_list.json()["devices"]) > 1:
                    log.info(
                        f"subscriptions list by device_by_acid_list: {len(device_by_acid_list.json()['devices'])}"
                    )
                    return True
                else:
                    log.error("not able to run device_by_acid_list")
                    return False

    @staticmethod
    def wf_sc_adi_get_devices_by_pcid(brnf_sa_login_load_account):
        app_adi = ActivateInventory(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["brnf_sc_api_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["brnf_sc_api_client_secret"],
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
                if len(device_list["devices"]) > 1:
                    log.info(
                        f"subscriptions list by device_by_pcid_list: {len(device_list['devices'])}"
                    )
                    return True
                else:
                    log.error("not able to run device_by_pcid_list")
                    return False

    @staticmethod
    def brnf_sa_sc_prov(device_type, order_sc_storage_legacy_devices):
        serial_number = order_sc_storage_legacy_devices[
            "device_" + device_type + str(0)
            ]["serial_no"]
        part_number = order_sc_storage_legacy_devices["device_" + device_type + str(0)][
            "part_num"
        ]
        certs = ExistingUserAcctDevices.storage_certs
        hpe_device_url = ExistingUserAcctDevices.hpe_device_url
        cluster_device_url = ExistingUserAcctDevices.ccs_device_url
        make_add_device_call = NetworkStorageComputeDeviceProvisionHelper(
            cluster_device_url,
            serial_number,
            part_number,
            device_type,
            certs,
            hpe_device_url,
        )
        return make_add_device_call.make_device_provision_request()

    @staticmethod
    def brnf_idev_ldev_compute_prov(device_type, serial, part, certs):
        serial_number = serial
        part_number = part
        certs = getattr(ExistingUserAcctDevices(), certs)
        hpe_device_url = ExistingUserAcctDevices.hpe_device_url
        cluster_device_url = ExistingUserAcctDevices.ccs_device_url
        make_add_device_call = NetworkStorageComputeDeviceProvisionHelper(
            cluster_device_url,
            serial_number,
            part_number,
            device_type,
            certs,
            hpe_device_url,
        )
        return make_add_device_call.make_device_provision_request()

    @staticmethod
    def wf_existing_device_app_unassignment(device_type,
                                            part_number,
                                            device_data,
                                            brnf_sa_sc_user_login_load_account,
                                            appid,
                                            application_instance_id):

        """ Helper function to unassign the device from an application
        params:- serial, device_type, part number"""

        device_list = [{"serial_number": device_data,
                        "device_type": device_type,
                        "part_number": part_number}]

        try:
            brnf_sa_sc_user_login_load_account.assign_devices_to_app_in_activate_inventory(device_list, appid,
                                                                                           application_instance_id)
        except Exception as e:
            log.info(f"Device might be already in assigned state. Assigning error: {e}")

        application_unassignment = brnf_sa_sc_user_login_load_account.unassign_devices_from_app_in_activate_inventory(
            device_list)

        if application_unassignment == "OK":
            return application_unassignment
        else:
            return False

    @staticmethod
    def wf_existing_device_app_assignment(device_type,
                                          part_number,
                                          device_data,
                                          brnf_sa_sc_user_login_load_account,
                                          appid,
                                          application_instance_id):
        """ Helper function to assign the device from an application
                params:- serial, device_type, part number, appid and application instance id"""

        device_list = [{"serial_number": device_data,
                        "device_type": device_type,
                        "part_number": part_number}]
        try:
            brnf_sa_sc_user_login_load_account.unassign_devices_from_app_in_activate_inventory(
                device_list)
            time.sleep(10)
        except Exception as e:
            log.info(f"Device might be already in unassigned state. Unassigning error: {e}")

        application_assignment = brnf_sa_sc_user_login_load_account \
            .assign_devices_to_app_in_activate_inventory(device_list,
                                                         appid,
                                                         application_instance_id)
        if application_assignment == "OK":
            return application_assignment
        else:
            return False

    def wf_ui_add_compute_csv_device(self, browser_instance, storage_state_path, csv_file) -> bool:
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
                .select_device_type("Compute Devices") \
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

    def wf_ui_claim_storage_device(self, browser_instance, storage_state_path, devices_details) -> bool:
        """Step #20: Add BaaS storage device claim via UI."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)
        try:
            device_details = ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details)[0]
            serial_no = device_details.get("serial_no")
            lic_key = device_details.get("lic_key")
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_devices()
            devices_inventory = DevicesInventory(page, self.cluster)
            add_devices_page = devices_inventory.click_add_devices() \
                .select_device_type("Storage Devices") \
                .click_next_button() \
                .select_purchase_or_lease_option() \
                .enter_serial_and_subscr_key(serial_no, lic_key) \
                .click_next_button() \
                .click_next_button() \
                .click_next_button() \
                .click_finish_button()
            add_devices_page.close_popup()
            devices_inventory \
                .wait_for_loaded_table() \
                .should_have_row_with_text_in_column("Serial Number", serial_no)
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

    @staticmethod
    def api_verify_device_tag(tag_name, tag_value, serials, ui_doorway):
        """Step #16-2: Check device tag."""
        tagged_devices = tags = []
        start_time = datetime.now()
        while not tags and datetime.now() < start_time + timedelta(seconds=15):
            tags = ui_doorway.filter_tags(tag_name=tag_name, tag_value=tag_value).get("tags")
        for tag in tags:
            devices = tag.get("devices")
            for device in devices:
                device_serial = device.get("serial_number")
                if device_serial in serials:
                    tagged_devices.append(device_serial)
        return set(serials).issubset(tagged_devices)

    def wf_ui_verify_device_tag(self, browser_instance, storage_state_path, device_details) -> bool:
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
                .should_have_tag("name1", device_details.get("mac"))
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)

    def wf_add_tag_to_device(self, browser_instance, storage_state_path, device_details, tag_name, tag_value) -> bool:
        """Step #16-1: Add tag to device via UI."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)
        try:
            ChooseAccount(page, self.cluster).open() \
                .go_to_account_by_name(self.pcid_name) \
                .wait_for_loaded_state().nav_bar.navigate_to_devices()
            dev_inventory_page = DevicesInventory(page, self.cluster)
            for device in device_details:
                serial_no = device.get("serial_no")
                dev_inventory_page \
                    .search_for_text(serial_no) \
                    .should_have_rows_count(1) \
                    .select_rows_with_text_in_column("Serial Number", serial_no) \
                    .assign_tag_to_devices(tag_name, tag_value)
            return True
        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False
        finally:
            browser_stop(context, page, test_name)
