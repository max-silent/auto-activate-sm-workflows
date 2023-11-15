import logging

import allure
import pytest

from automation.conftest import ExistingUserAcctDevices

log = logging.getLogger(__name__)


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices")
@allure.sub_suite("Brownfield existing account new network devices - API claim")
class TestVerifyDeviceClaim:
    @pytest.mark.testrail(id=1220656)
    @pytest.mark.Regression
    @pytest.mark.Plv
    def test_verify_device_claim_c1220656(self, adi_app_api_session, brnf_sa_order_iap_devices):
        """
        Tesing API used to verify the device claim
        """
        log.info(brnf_sa_order_iap_devices)
        pcid = ExistingUserAcctDevices.test_data['brownfield_account_with_one_network_app']['pcid']
        serial_number = brnf_sa_order_iap_devices['device_IAP0']['serial_no']
        claim_status = \
            adi_app_api_session.verify_claim_and_assignment_to_application(pcid=pcid,
                                                                           device_serial_number=serial_number)
        dict_claim_status = claim_status.json()

        assert claim_status.status_code == 200 and dict_claim_status["response"] == "claimable"

        reset_device_response = adi_app_api_session.device_reset_afs(serial=serial_number)
        log.info(reset_device_response.json())
