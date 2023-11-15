import logging

import allure
import pytest

from automation_svc_ui.local_libs.activate_inventory.adi_test_helper import AdiTestHelper

log = logging.getLogger(__name__)


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield_network_devices")
@allure.sub_suite("Brownfield_existing_account_existing_network_devices")
@pytest.mark.xfail
class TestClaimVgwDevice:
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220623)
    def test_claim_vgw_device_C1220623(self, adi_app_api_session):
        """
           ====== Creates the vgw device ========
           - Verify if it is claimed.
           - Check if the device is provisioned.

        """
        aditesthlper = AdiTestHelper()
        assert aditesthlper.claim_vgw_device(adi_app_api_session), "VGW device is not Claimed.."
