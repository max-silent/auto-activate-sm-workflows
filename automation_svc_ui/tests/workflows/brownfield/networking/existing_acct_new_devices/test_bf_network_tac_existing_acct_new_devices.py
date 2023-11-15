import logging
import time

import allure
import pytest

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.tests.workflows.brownfield.networking.existing_acct_new_devices.brnf_network_existing_acct_new_devices \
    import WfExistingAcctNewDevices

log = logging.getLogger(__name__)

create_test = WfExistingAcctNewDevices()


@pytest.mark.skipif("polaris" in ExistingUserAcctDevices.login_page_url, reason="Not supported on polaris.")
@pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
@pytest.mark.skipif("pavo" in ExistingUserAcctDevices.login_page_url, reason="Not supported on pavo.")
@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices service_centric_ui")
@allure.sub_suite("Brownfield TAC existing account new network devices")
class TestTacExistingAccountNewDevicesSvc:
    @pytest.mark.testrail(id=1220580)
    @pytest.mark.order(1)
    @pytest.mark.Regression
    @pytest.mark.parametrize("device_order",
                             ["brnf_sa_order_iap_devices", "brnf_sa_order_sw_devices", "brnf_sa_order_gw_devices"])
    def test_brnf_sa_order_devices_c1220580(self, request, device_order):
        """
        ===== Create network device on Activate order process ======
        1. Run AOP manufacturing API to create network device
        """
        devices_details = request.getfixturevalue(device_order)
        assert devices_details

    @pytest.mark.order(2)
    @pytest.mark.Regression
    def test_brnf_user_login_load_account_c1220622(self, brnf_sa_user_login_load_account):
        """
        ===== User login to the account using user API for other tests to run user api ======
        1. User login to the account using new user and password
        2. User load the pcid account for other tests to run user api for other subsequent test cases
        """
        assert brnf_sa_user_login_load_account

    @pytest.mark.testrail(id=1220622)
    @pytest.mark.order(3)
    @pytest.mark.Regression
    @pytest.mark.parametrize("device_order",
                             ["brnf_sa_order_iap_devices", "brnf_sa_order_sw_devices", "brnf_sa_order_gw_devices"])
    def test_brnf_manual_claim_ui_c1220622(self, request, device_order, browser_instance, logged_in_storage_state):
        log.info("Running test_brnf_manual_claim_ui_c1220622")
        devices_details = [request.getfixturevalue(device_order)]
        assert create_test.wf_ui_add_device(browser_instance, logged_in_storage_state, devices_details)

    @pytest.mark.order(4)
    @pytest.mark.Regression
    @pytest.mark.parametrize("device_type, device_order",
                             [("IAP", "brnf_sa_order_iap_devices"),
                              ("SWITCH", "brnf_sa_order_sw_devices"),
                              ("GATEWAY", "brnf_sa_order_gw_devices")])
    def test_assign_device(self, request, device_type, device_order, brnf_sa_user_login_load_account):
        """
         ===== Manually add device into account and verify auto assignment ======
         1. Using the login session
         2. Manually add device into account and verify auto assignment
         3. Verify the device is added to the account and assigned to the application correctly
         """
        log.info("Running test_assign_device")
        time.sleep(7)
        devices_details = [request.getfixturevalue(device_order)]
        assert create_test.wf_new_device_app_assignment(device_type, devices_details, brnf_sa_user_login_load_account)

    @pytest.mark.testrail(id=1220666)
    @pytest.mark.order(5)
    @pytest.mark.Regression
    @pytest.mark.parametrize("device_type, device_order, subscription",
                             [("IAP", "brnf_sa_order_iap_devices", "brnf_sa_iap_subscription"),
                              ("SWITCH", "brnf_sa_order_sw_devices", "brnf_sa_sw_subscription"),
                              ("GATEWAY", "brnf_sa_order_gw_devices", "brnf_sa_gw_subscription")])
    def test_subs_evals_license_c1220666(self,
                                         request,
                                         device_type,
                                         device_order,
                                         subscription,
                                         brnf_sa_user_login_load_account):
        """
        ===== Assign eval license to device ======
        1. Using the login session
        2. Manually assign license to network device
        3. Verify the license is assigned correctly
        """
        log.info("Running test_subs_evals_license_c1220666")
        devices_details = request.getfixturevalue(device_order)
        subscr_key = request.getfixturevalue(subscription).get("key")

        subs_assign_resp = False
        for i in range(2):
            subs_assign_resp = create_test.assign_subs_eval_by_key(device_type,
                                                                   devices_details,
                                                                   subscr_key,
                                                                   brnf_sa_user_login_load_account)
            if subs_assign_resp:
                break
            time.sleep(3)
        assert subs_assign_resp
        assert subs_assign_resp[0]["subscription_key"] == subscr_key

    @pytest.mark.order(6)
    @pytest.mark.testrail(id=1221583)
    @pytest.mark.Regression
    @pytest.mark.parametrize("subscription",
                             ["brnf_sa_iap_subscription", "brnf_sa_sw_subscription", "brnf_sa_gw_subscription"])
    def test_expire_subscription_ui_c1221583(self,
                                             request,
                                             subscription,
                                             browser_instance,
                                             tac_logged_in_storage_state):
        log.info("Running test_expire_subscription_ui_c1221583")
        subscription = request.getfixturevalue(subscription)
        assert create_test.wf_expire_subscription(browser_instance, tac_logged_in_storage_state, subscription)

    @pytest.mark.order(7)
    @pytest.mark.testrail(id=1221583)
    @pytest.mark.Regression
    @pytest.mark.xfail(reason="GLCP-130289")
    @pytest.mark.parametrize("device_order, subscription",
                             [("brnf_sa_order_iap_devices", "brnf_sa_iap_subscription"),
                              ("brnf_sa_order_sw_devices", "brnf_sa_sw_subscription"),
                              ("brnf_sa_order_gw_devices", "brnf_sa_gw_subscription")])
    def test_check_device_with_expired_subscription_ui_c1221583(self,
                                                                request,
                                                                device_order,
                                                                subscription,
                                                                browser_instance,
                                                                logged_in_storage_state):
        log.info("Running test_check_device_with_expired_subscription_ui_c1221583")
        device_details = [request.getfixturevalue(device_order)]
        subscription = request.getfixturevalue(subscription)
        assert create_test.verify_expired_subscr_detach(browser_instance,
                                                        logged_in_storage_state,
                                                        device_details,
                                                        subscription)

    @pytest.mark.order(8)
    @pytest.mark.testrail(id=1221583)
    @pytest.mark.Regression
    @pytest.mark.parametrize("device_order, subscription",
                             [("brnf_sa_order_iap_devices", "brnf_sa_iap_subscription"),
                              ("brnf_sa_order_sw_devices", "brnf_sa_sw_subscription"),
                              ("brnf_sa_order_gw_devices", "brnf_sa_gw_subscription")])
    def test_check_reassign_expired_subscription_ui_c1221583(self,
                                                             request,
                                                             device_order,
                                                             subscription,
                                                             browser_instance,
                                                             logged_in_storage_state):
        log.info("Running test_check_reassign_expired_subscription_ui_c1221583")
        device_details = [request.getfixturevalue(device_order)]
        subscription = request.getfixturevalue(subscription)
        assert create_test.verify_reassign_to_expired_subscription(browser_instance,
                                                                   logged_in_storage_state,
                                                                   device_details,
                                                                   subscription)

    @pytest.mark.order(9)
    @pytest.mark.Regression
    @pytest.mark.parametrize("devices, cust2_target_folder", [
        pytest.param(["brnf_sa_order_iap_devices", "brnf_sa_order_sw_devices"],
                     "default", marks=pytest.mark.testrail(id=1225448)),
        pytest.param(["brnf_sa_order_gw_devices"], "customfolder145", marks=pytest.mark.testrail(id=1225449))])
    def test_tac_move_devices_between_customers_athena_f_to_valid_folder(self,
                                                                         browser_instance,
                                                                         tac_logged_in_storage_state,
                                                                         request,
                                                                         devices,
                                                                         cust2_target_folder):

        """
        Test goes to TAC account 'Devices' page, tries to move 3 existing devices at athena-f folder
        to other customer's default/custom folder and verifies moving completed successfully.
        Steps:
        1. Login to GLCP with TAC user credentials
        2. Open CCS manager menu
        3. Open Devices page
        4. Try to move existing devices from athena-f folder of customer1 to default/custom folder of customer2
        5. Verify devices moved successfully.
        """
        cust1_athena_f_folder = \
            ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1_athena_f_folder"]
        athena_f_devices = [request.getfixturevalue(device) for device in devices]
        assert create_test.wf_tac_move_devices_between_customers_from_athena_f(browser_instance,
                                                                               tac_logged_in_storage_state,
                                                                               athena_f_devices,
                                                                               cust1_athena_f_folder,
                                                                               cust2_target_folder)
