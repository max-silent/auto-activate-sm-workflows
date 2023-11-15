import logging

import allure
import pytest

log = logging.getLogger(__name__)


@pytest.mark.nonsvc
@allure.parent_suite("activate-sm-workflows")
@allure.suite("Greenfield network devices - service_centric_ui")
@allure.sub_suite("Greenfield app api claim existing account new network devices")
class TestAppApiExistingAccountNewDevicesSvc:
    @pytest.mark.order(1)
    @pytest.mark.Regression
    def test_brnf_sa_order_iap_devices(self, brnf_sa_order_iap_devices):
        """
        ===== Create IAP device on Activate order process ======
        1. Run AOP API manufacturing API to create IAP network device
        """
        assert brnf_sa_order_iap_devices

    @pytest.mark.order(2)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220654)
    def test_brnf_app_api_iap_claim_c1220654(self, brnf_sa_manual_claim_iap_device_app_api,
                                             brnf_app_api_session):
        """
        ===== Manually add IAP into account and verify claim ======
        1. Using the app api session
        2. Manually add IAP into account
        3. Verify the IAP is added/claimed to the account
        """
        log.info("Running test_brnf_app_api_iap_claim_c1220654")
        if brnf_app_api_session:
            assert brnf_sa_manual_claim_iap_device_app_api
