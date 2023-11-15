import logging

from hpe_glcp_automation_lib.libs.adi.ui.activate_devices_page import ActivateDevices
from hpe_glcp_automation_lib.libs.adi.ui.device_history_page import DeviceHistory

log = logging.getLogger(__name__)
expected_status = "application_assigned"


class DeviceHistoryVerifier:
    """
    ADI-service verifications class.
    """

    @staticmethod
    def check_devices_history(active_dev_page: ActivateDevices, device_details: dict):
        """Check that device details are present at Devices History page.

        :param active_dev_page: instance of ActiveDevices page-object class.
        :param device_details: dictionary with device details. Following keys are required for this method:
            "device_type", "serial_no".
        """
        device_type = device_details["device_type"]
        device_serial_number = device_details["serial_no"]
        log.info(
            f"Playwright: verifying info of '{device_type}' device with id '{device_serial_number}' at Active "
            f"Devices page.")
        active_dev_page \
            .open_device_history(device_serial_number)
        DeviceHistory(active_dev_page.page, active_dev_page.cluster, device_serial_number) \
            .wait_for_loaded_table() \
            .should_have_valid_date_for_status(expected_status, timedelta=900) \
            .go_back_to_activate_device_page()
