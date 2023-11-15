import logging
import time

import allure
import pytest

from automation.conftest import ExistingUserAcctDevices
from automation.local_libs.activate_inventory.adi_test_helper import AdiTestHelper

log = logging.getLogger(__name__)
SLEEP_TIME_LOW = 5
SLEEP_TIME_HIGH = 10


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices")
@allure.sub_suite("Brownfield existing account existing network devices")
class TestArchiveAssignedDevice:
    @pytest.mark.Regression
    @pytest.mark.Plv
    @pytest.mark.testrail(id=1220641)
    def test_archive_assigned_device_from_list_of_device_C1220641(self, adi_app_api_session, adi_app_api_helper):
        """
        ============== Archiving assigned device =================

        1. Picking a device from list of assigned devices.
        2. Archiving the device.
        3. Verify device is archived
        4. Revert state of device to Provisioned (unarchive and provision)
        """

        pcid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_pcid']
        acid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_acid']

        #get a device that is assigned
        device = adi_app_api_helper.get_provisioned_device_for_pcid(pcid, device_type="SWITCH")
        serial_number = device['serial_number']
        #provisioned_acid = device["application_customer_id"]
        log.info("PICKING device {}".format(serial_number))
        #archive the device
        devices = {"devices": [{"serial_number": serial_number,"archive": True}]}
        archived_response = adi_app_api_session.update_archive_status(pcid, devices)

        assert archived_response.status_code == 200

        #add some wait
        time.sleep(SLEEP_TIME_LOW)

        #Device should not be assigned anymore, verify the same
        is_device_found = AdiTestHelper.is_device_provisioned_to_acid_for_pcid(
             adi_app_api_session = adi_app_api_session,
             pcid=pcid,
             acid=acid,
             serial_number=serial_number)
        if is_device_found:
             assert False, "device is still in assigned state"
        else:
            log.info("Device is not Found in the list of assigned devices anymore!!..and it's expected..")

            #verify the device is archived under the account
            is_arch_device_found = AdiTestHelper.find_archived_device_in_get_devices_by_pcid(
                   adi_app_api_session=adi_app_api_session,
                   pcid=pcid,
                   serial_number=serial_number)
            device_found_in_archived_list = " NOT "
            if is_arch_device_found:
                device_found_in_archived_list = " "
                log.info(f"Device {serial_number} {device_found_in_archived_list} found In Archive List...")
                assert True
            else:
                assert False, f"Device {serial_number} {device_found_in_archived_list} found In Archive List..."

            # Reverting the device's state, unarchive and provision
            devices = {"devices": [{"serial_number": serial_number, "archive": False}]}
            unarchived_response = adi_app_api_session.update_archive_status(pcid, devices)
            assert unarchived_response.status_code == 200
            log.info("Reverted test device state: Step1: Unarchived the device.")

            assign_response = adi_app_api_session.provision_dev_acid(
                                   acid = acid,
                                   payload = device
            )
            assert assign_response.status_code == 200
            log.info("Reverted test device state: Step2: Provisioned the device to acid {}.".format(acid))

        





