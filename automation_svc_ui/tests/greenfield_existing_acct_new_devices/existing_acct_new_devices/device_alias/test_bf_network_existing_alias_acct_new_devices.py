import logging

import allure
import pytest

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.tests.greenfield_existing_acct_new_devices.existing_acct_new_devices.brnf_network_existing_acct_new_devices import (
    WfExistingAcctNewDevices,
)

log = logging.getLogger(__name__)


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Greenfield network devices - service_centric_ui")
@allure.sub_suite("Greenfield existing account with alias new network devices")
@pytest.mark.skipif("polaris" in ExistingUserAcctDevices.login_page_url,
                    reason="Not supported on polaris: service-centric UI account needed.")
@pytest.mark.skipif("pavo" in ExistingUserAcctDevices.login_page_url,
                    reason="Not supported on pavo: service-centric UI account needed.")
@pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url,
                    reason="Not supported on triton-lite: service-centric UI account needed.")
class TestExistingAccountAliasNewDevicesSvc:
    @pytest.mark.testrail(id=1220580)
    @pytest.mark.order(1)
    @pytest.mark.Regression
    def test_brnf_autoclaim_order_iap_devices_c1220580(self, brnf_autoclaim_order_iap_devices):
        """
        ===== Create IAP device on Activate order process ======
        1. Run AOP API manufacturing API to create IAP network device
        """
        assert brnf_autoclaim_order_iap_devices

    @pytest.mark.order(2)
    @pytest.mark.Regression
    def test_brnf_user_login_load_account_c1220622(self, brnf_sa_user_login_load_account):
        """
        ===== User login to the account using user API for other tests to run user api ======
        1. User login to the account using new user and password
        2. User load the pcid account for other tests to run user api for other subsequent test cases
        """
        assert brnf_sa_user_login_load_account

    @pytest.mark.testrail(id=1220626)
    @pytest.mark.order(3)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_verify_claim_c1220626(self, brnf_sa_user_login_load_account, brnf_autoclaim_order_iap_devices):
        """
        ===== Verify devices were claimed into account and verify auto assignment ======
        1. Using the login session
        2. Verify device is added into account (claimed)
        """
        assert brnf_autoclaim_order_iap_devices, "No device to claim: IAP device was not created."
        device_order = [*brnf_autoclaim_order_iap_devices.values()][0]
        create_test = WfExistingAcctNewDevices()
        assert create_test.verify_device_claimed(device_order, brnf_sa_user_login_load_account)

    @pytest.mark.order(4)
    @pytest.mark.Regression
    def test_assign_iap_device(self, brnf_autoclaim_order_iap_devices,
                               brnf_sa_user_login_load_account):
        """
         ===== Assign IAP-device to application ======
         1. Using the login session, assign device to the application and check it's successful.
         """
        assert brnf_autoclaim_order_iap_devices, "No device to assign: IAP device was not created."
        create_test = WfExistingAcctNewDevices()
        device_type = "IAP"
        devices_details = [brnf_autoclaim_order_iap_devices]
        assert create_test.wf_new_device_app_assignment(device_type,
                                                        devices_details,
                                                        brnf_sa_user_login_load_account)

    @pytest.mark.testrail(id=1220666)
    @pytest.mark.order(5)
    @pytest.mark.Regression
    def test_subs_iap_evals_license_c1220666(self,
                                             brnf_autoclaim_order_iap_devices,
                                             brnf_sa_user_login_load_account
                                             ):
        """
        ===== Assign eval license to IAP ======
        1. Using the login session
        2. Manually assign license to IAP
        3. Verify the license is assigned correctly
        """
        assert brnf_autoclaim_order_iap_devices, "No device to assign: IAP device was not created."
        create_test = WfExistingAcctNewDevices()
        device_type = "IAP"
        assert create_test.wf_assign_subs_eval(
            device_type, brnf_autoclaim_order_iap_devices, brnf_sa_user_login_load_account
        )

    @pytest.mark.testrail(id=1220635)
    @pytest.mark.order(6)
    @pytest.mark.Regression
    def test_get_audit_log_sm_details_c1220635(self, browser_instance,
                                               logged_in_storage_state,
                                               brnf_autoclaim_order_iap_devices,
                                               brnf_sa_user_login_load_account):
        create_test = WfExistingAcctNewDevices()
        assert create_test.wf_sm_audit_log_info(browser_instance,
                                                logged_in_storage_state,
                                                [brnf_autoclaim_order_iap_devices],
                                                brnf_sa_user_login_load_account)
