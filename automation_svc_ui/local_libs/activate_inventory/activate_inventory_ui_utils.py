import logging
from typing import Union, List, Tuple

from hpe_glcp_automation_lib.libs.adi.ui.dev_inventory_page import DevicesInventory

log = logging.getLogger(__name__)


class DeviceInventoryHelper:
    """
    Device Inventory helper class.
    """

    @staticmethod
    def claim_ordered_network_devices(page: DevicesInventory, devices_details: Union[List[dict], Tuple[dict, ...]],
                                      delivery_contact_idx: int = 1):
        """Add ordered network devices with provided serials and macs via UI.

        :param page: instance of DevicesInventory page-object class.
        :param devices_details: list/tuple of dictionaries with device details. Following keys in dictionaries
             are required for this method: "serial_no", "mac".
        :param delivery_contact_idx: index (starting from 1) of item to be selected in delivery contact dropdown list.
        """
        add_devices_page = page.click_add_devices() \
            .select_device_type("Networking Devices") \
            .click_next_button() \
            .select_serial_and_mac_option()
        for device_details in devices_details:
            add_devices_page.enter_serial_and_mac(device_details["serial_no"], device_details["mac"])
        add_devices_page \
            .should_have_rows_count(len(devices_details)) \
            .click_next_button().click_next_button() \
            .select_delivery_contact_by_number(delivery_contact_idx) \
            .click_next_button() \
            .click_finish_button() \
            .close_popup()


class ActivateInventoryVerifier:
    """
    ADD-service verifications class.
    """

    @staticmethod
    def check_devices_inventory(dev_inventory_page: DevicesInventory, device_details: dict):
        """Check that device details are present at Devices Inventory page.

        :param dev_inventory_page: instance of DevicesInventory page-object class.
        :param device_details: dictionary with device details. Following keys are required for this method:
            "device_type", "serial_no", "mac".
        """
        device_type = device_details["device_type"]
        device_serial_number = device_details["serial_no"]
        mac_address = device_details["mac"]
        log.info(
            f"Playwright: verifying info of '{device_type}' device with id '{device_serial_number}' at Devices page.")
        dev_inventory_page \
            .search_for_text(device_serial_number) \
            .should_have_rows_count(1) \
            .should_have_row_with_text_in_column("Serial Number", device_serial_number) \
            .should_have_row_with_values_in_columns({"Serial Number": device_serial_number, "MAC Address": mac_address})

    @staticmethod
    def check_devices_filtering_by_tier(dev_inventory_page: DevicesInventory, tiers_list: List[str]):
        """Check that devices table is filtered properly according to the list of tiers applied with filter.

        :param dev_inventory_page: instance of DevicesInventory page-object class.
        :param tiers_list: list of tiers (str), to be applied with filter.
        """
        dev_inventory_page.clear_filter()
        dev_inventory_page \
            .add_filter_by_subscription_tiers(tiers_list) \
            .wait_for_loaded_table() \
            .should_all_rows_have_text_in_column("Subscription Tier", tiers_list)
