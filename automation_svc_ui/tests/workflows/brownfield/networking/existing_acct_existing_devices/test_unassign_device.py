import logging

import allure
import pytest

from automation_svc_ui.conftest import ExistingUserAcctDevices

log = logging.getLogger(__name__)


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices")
@allure.sub_suite("Existing account - Existing network devices")
@pytest.mark.xfail
class TestExistingDevicesUnassignDevicesAppApi:
    @pytest.mark.order(1)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220639)
    def test_unassign_device_from_app_c1220639(self, adi_app_api_session, adi_app_api_helper):
        """
        ===== Unassign a device from Application ======
        1. get device by acid
        2. unprovision a device
        3. verify the device is unprovision successfully
        """
        pcid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_pcid"]
        acid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_acid"]

        # get devices from list of assigned devices
        acid_devices = adi_app_api_session.get_devices_by_acid(application_customer_id=acid)
        device = acid_devices.json()["devices"][0]
        # unassign device from application
        unassign_response = adi_app_api_session.unprovision_device_from_application(device)
        if unassign_response.status_code == 200:
            # verify device should successfully unprovisioned
            verify_response = adi_app_api_helper.is_device_provisioned_to_pcid(platform_customer_id=pcid,
                                                                               serial_number=device["serial_number"])
            assert verify_response == False
        else:
            assert False
