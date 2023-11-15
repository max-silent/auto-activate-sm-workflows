import logging

import allure
import pytest

from automation.conftest import ExistingUserAcctDevices
from automation.local_libs.activate_inventory.verify_by_api import VerifyByApi

log = logging.getLogger(__name__)


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices")
@allure.sub_suite("Brownfield move device from parent to child customer")
class TestMoveDeviceFromParentToChildCustomer:
    @pytest.mark.testrail(id=1220657)
    @pytest.mark.Regression
    def test_move_device_from_parent_to_child_customer_c1220657(self, adi_app_api_session):
        """
        === Move device from parent to child customer ===
        1. get iap devices by parent pcid
        2. move device b/w parent and child
        3. verify the device moved successfully
        4. move device back to parent customer
        5. verify the device moved back successfully
        """

        parent_pcid = ExistingUserAcctDevices.test_data["harness_brownfield_account_parent_pcid"]
        child_pcid = ExistingUserAcctDevices.test_data["harness_brownfield_account_child_pcid"]


        # get network devices from list of devices
        iap_devices = VerifyByApi.get_all_network_devices_by_pcid(adi_app_api_session=adi_app_api_session, pcid=parent_pcid)
        
        # prepare payload for move device b/w parent and child
        devices = []
        device_serial = iap_devices[0]["serial_number"]
        devices.append(device_serial)

        # move device to child customer
        moveTo_response = adi_app_api_session.move_device_bw_parent_child(operation="moveTo", device_list=devices, pcid=child_pcid)

        assert moveTo_response.status_code == 200 and adi_app_api_session.verify_device_claimed_by_pcid(platform_customer_id=child_pcid, device_serial_number=device_serial)

        # move back device to parent customer
        moveFrom_response = adi_app_api_session.move_device_bw_parent_child(operation="MoveFrom", device_list=devices, pcid=child_pcid)

        assert moveFrom_response.status_code == 200 and adi_app_api_session.verify_device_claimed_by_pcid(platform_customer_id=parent_pcid, device_serial_number=device_serial)
