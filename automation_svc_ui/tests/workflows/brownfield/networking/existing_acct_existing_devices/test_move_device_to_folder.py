import logging

import allure
import pytest

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.tests.workflows.brownfield.networking.existing_acct_existing_devices.network_existing_device_test_helper \
    import ExistingAccountExistingNetworkDeviceHelper

log = logging.getLogger(__name__)


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices")
@allure.sub_suite("Existing account - Existing network devices")
@pytest.mark.xfail
class TestMoveDeviceToFolder:
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220650)
    def test_move_device_to_folder_for_platform_customer_C1220650(self, adi_app_api_session):
        """
        ==== Test case to move a device from one folder to another ======
        """

        acid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_acid"]
        pcid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_pcid"]

        # Getting one device to move it to default folder
        devices = adi_app_api_session.get_devices_by_acid(application_customer_id=acid)
        dict_devices = devices.json()
        device_list = dict_devices["devices"]
        serial_number = device_list[0]["serial_number"]
        device = device_list[0]

        # moving the device to default folder, which will un-assign the device automatically
        adi_app_api_session.move_device_to_folder(device_list=[device], pcid=pcid, folder_name='default')

        # Checking if the device is moved to default folder and not assigned to any application anymore
        is_device_assigned = ExistingAccountExistingNetworkDeviceHelper.is_device_provisioned_to_acid_for_pcid(
            adi_app_api_session, pcid, acid, serial_number)

        assert is_device_assigned == False, "Device not moved to default folder and is still assigned."

        # Provisioning the device back which will move the device back to athena-f-<acid> folder
        response = adi_app_api_session.provision_dev_acid(payload=device_list[0], acid=acid)
        log.info(response)

        # Checking if the device got provisioned successfully
        is_device_assigned = ExistingAccountExistingNetworkDeviceHelper.is_device_provisioned_to_acid_for_pcid(
            adi_app_api_session, pcid, acid, serial_number)

        assert is_device_assigned == True, "Device did not get assigned back to application..."
