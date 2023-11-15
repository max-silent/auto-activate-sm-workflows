import logging

import allure
import pytest

from automation.conftest import ExistingUserAcctDevices

log = logging.getLogger(__name__)


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices")
@allure.sub_suite("Brownfield app api claim existing account new network devices")
class TestArchiveDevice:
    @pytest.mark.Regression
    @pytest.mark.Plv
    @pytest.mark.testrail(id=1220640)
    def test_archive_device_c1220640(self, brnf_sa_order_iap_devices, adi_app_api_session):
        """
        Test to archive a device.

        Args:
            brnf_sa_order_iap_devices (dict): Dictionary containing the device information.
            adi_app_api_session (obj): Instance of AppApiSession.

        Returns:
            Whether device is archived or not.
        """
        pcid = ExistingUserAcctDevices.test_data['brownfield_account_with_one_network_app']['pcid']
        username = ExistingUserAcctDevices.test_data['brownfield_account_with_one_network_app']['username']

        mac = brnf_sa_order_iap_devices['device_IAP0']['mac']
        device_serial_number = brnf_sa_order_iap_devices['device_IAP0']['serial_no']

        # Claim the device using the app_api_session's claim_device_app_api function..
        adi_app_api_session.claim_device_app_api(
            device_category="NETWORK",
            serial=device_serial_number,
            platform_id=pcid,
            username=username,
            mac=mac,
            entitlement_id=None)

        # Create a dictionary with the device information and 'archive' set to True
        device_data = {
            "devices": [
                {
                    "serial_number": device_serial_number,
                    "mac": mac,
                    "archive": True
                }
            ]
        }
        # Archive the device using the app_api_session's update_archive_status function
        archived_response = adi_app_api_session.update_archive_status(
            pcid=pcid,
            devices=device_data)
        if archived_response.status_code == 200:
            log.info("Device is archived")
            assert True

            # Move device to Aruba-Factory-Stock
            resp = adi_app_api_session.device_reset_afs(serial=device_serial_number, mac_address=mac, pcid=pcid)
            assert resp.status_code == 200
            log.info("Device moved to AFS from Customer account{}".format(resp))
        else:
            assert False, "Device is not archived"
