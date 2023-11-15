import logging

import allure
import pytest

from automation.conftest import ExistingUserAcctDevices
from automation.local_libs.activate_inventory.adi_test_helper import AdiTestHelper

log = logging.getLogger(__name__)


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices")
@allure.sub_suite("Brownfield app api provision existing archived network device")
class TestProvisionExistingArchivedDevice:
    """
    Contains Test case including steps for archiving/unarchiving device.
    """

    @pytest.mark.testrail(id=1220642)
    @pytest.mark.Regression
    @pytest.mark.Plv
    @pytest.mark.order(2)
    @pytest.mark.parametrize(
        "archive_network_device", [ExistingUserAcctDevices.test_data['archive_devices_related_account']["pcid"]], indirect= True
    )
    def test_provision_archived_device_C1220642(self, adi_app_api_session, archive_network_device):
        """
        Test case to provision an archived device for a specific application customer ID (ACID).
        """

        log.info(archive_network_device)
        
        pcid = ExistingUserAcctDevices.test_data['archive_devices_related_account']["pcid"]
        acid = ExistingUserAcctDevices.test_data['archive_devices_related_account']["acid_network"]

        # Retrieve device serial number, and MAC address from the archive_network_device
        serial_number = archive_network_device["serial_number"]    
        device_type = archive_network_device["device_type"]

        # Create a list of devices to provision, using the MAC address, device serial number, and device type.
        device_list = {
                "serial_number": serial_number,
                "device_type": device_type
            }
        

        # Provision the device for the specified ACID and device type.
        response = adi_app_api_session.provision_dev_acid(
                            acid = acid,
                            payload = device_list)

        # Log the final response for debugging purposes.
        log.info(f'This final response: {response.json()}')
        log.info(f'This final response code: {response.status_code}')

        assert response.status_code == 412, "Device got provisioned, which is not expected!!"

        # Check if the device was provisioned successfully by searching for it using its PCID, ACID, and serial number.
        is_device_provisioned = AdiTestHelper.is_device_provisioned_to_acid_for_pcid(
            adi_app_api_session=adi_app_api_session,
            pcid=pcid,
            acid=acid,
            serial_number=serial_number
        )

        # Log whether or not the device was provisioned or not for debugging purposes.
        log.info(is_device_provisioned)

        # Assert that the device was not provisioned.
        assert is_device_provisioned == False

        # Reverting the device to original state
        payload = {}
        archive_network_device["archive"] = False
        payload["devices"] = [archive_network_device]
        archive_response = adi_app_api_session.update_archive_status(pcid = pcid, devices = payload)
        assert archive_response.status_code == 200