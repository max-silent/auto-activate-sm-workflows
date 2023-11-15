import logging
import os
import time

import allure
import pytest

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.conftest import SkipTest, get_add_device_expected_responses
from automation_svc_ui.local_libs.activate_inventory.verify_by_api import VerifyByApi
from automation_svc_ui.local_libs.utils.pytest.pytest_marker import get_pytest_marker
from automation_svc_ui.tests.greenfield_existing_acct_new_devices.existing_acct_new_devices.brnf_network_existing_acct_new_devices \
    import WfExistingAcctNewDevices

log = logging.getLogger(__name__)

expected_response_data = get_add_device_expected_responses()


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Greenfield network devices - service_centric_ui")
@allure.sub_suite("Greenfield existing account new network devices")
@pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
@pytest.mark.skipif("polaris" in ExistingUserAcctDevices.login_page_url, reason="Not supported on polaris.")
@pytest.mark.skipif("pavo" in ExistingUserAcctDevices.login_page_url, reason="Not supported on pavo.")
class TestExistingAccountNewDevicesSvc:
    @pytest.mark.testrail(id=1220580)
    @pytest.mark.order(1)
    @pytest.mark.Regression

    def test_brnf_sa_order_iap_devices_c1220580(self, brnf_sa_order_iap_devices):
        """
        ===== Create IAP device on Activate order process ======
        1. Run AOP API manufacturing API to create IAP network device
        """
        assert brnf_sa_order_iap_devices

    @pytest.mark.testrail(id=1220580)
    @pytest.mark.order(2)
    @pytest.mark.Regression
    def test_brnf_sa_order_sw_devices_c1220580(self, brnf_sa_order_sw_devices):
        """
        ===== Create Switch device on Activate order process ======
        1. Run AOP API manufacturing API to create Switch network device
        """
        assert brnf_sa_order_sw_devices

    @pytest.mark.testrail(id=1220580)
    @pytest.mark.order(3)
    @pytest.mark.Regression
    def test_brnf_sa_order_gw_devices_c1220580(self, brnf_sa_order_gw_devices):
        """
        ===== Create Gateway device on Activate order process ======
        1. Run AOP API manufacturing API to create Gateway network device
        """
        assert brnf_sa_order_gw_devices

    @pytest.mark.order(4)
    @pytest.mark.Synthetic
    @pytest.mark.Regression
    def test_brnf_user_login_load_account_c1220622(self, brnf_sa_user_login_load_account):
        """
        ===== User login to the account using user API for other tests to run user api ======
        1. User login to the account using new user and password
        2. User load the pcid account for other tests to run user api for other subsequent test cases
        """
        assert brnf_sa_user_login_load_account

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.order(5)
    @pytest.mark.testrail(id=1220675)
    @pytest.mark.Regression
    def test_iap_dev_prov_fail_prov_no_rule_c1220675(self, brnf_sa_iap_prov):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail-prov-no-rule'
        """
        SkipTest.skip_if_triton_lite()
        response = brnf_sa_iap_prov
        assert response.status_code == expected_response_data["iap_provision_no_rule"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["iap_provision_no_rule"]["X-Status-Code"]
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    @pytest.mark.parametrize('api_path, x_type', [
        pytest.param("hpe-provision", "provision-update",
                     marks=[pytest.mark.testrail(id=1313766), pytest.mark.order(6)],
                     id='ftpm_provision_C1313766'),
        pytest.param("hpe-provision-rtpm", "provision-update",
                     marks=[pytest.mark.testrail(id=1313767), pytest.mark.order(7)],
                     id='rtpm_provision_C1313767'),
        pytest.param("cx-provision", "provision-update", marks=[pytest.mark.testrail(id=1313855), pytest.mark.order(8)],
                     id='cx-provision_C1313855')])
    def test_sw_dev_prov_no_rule(self, brnf_sa_sw_prov, api_path, x_type):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail-prov-no-rule'
        """
        response = brnf_sa_sw_prov
        assert response.status_code == expected_response_data['switch_provision_no_rule']['response_code']
        assert response.headers["X-Status-Code"] == expected_response_data['switch_provision_no_rule'][
            'X-Status-Code']
        assert response.headers["X-Activation-Key"] is not None
        assert len(response.headers["X-Activation-Key"]) == 8

    @pytest.mark.testrail(id=1220622)
    @pytest.mark.order(9)
    @pytest.mark.Regression
    def test_brnf_manual_ui_claim_iap_c1220622(self, browser_instance,
                                               logged_in_storage_state,
                                               brnf_sa_order_iap_devices,
                                               ):
        create_test = WfExistingAcctNewDevices()
        devices_details = [brnf_sa_order_iap_devices]
        assert create_test.wf_ui_add_device(browser_instance, logged_in_storage_state, devices_details)

    @pytest.mark.testrail(id=1220633)
    @pytest.mark.order(10)
    @pytest.mark.Regression
    def test_brnf_manual_csv_claim_sw_gw_c1220633(self, browser_instance,
                                                  logged_in_storage_state,
                                                  brnf_sa_user_login_load_account,
                                                  brnf_sa_order_sw_devices,
                                                  brnf_sa_order_gw_devices,
                                                  get_device_csv):
        """
        ===== Using UI claim device by uploading CSV file======
        1. Login to GLCP via UI
        2. Go to Device Inventory page
        3. Pick CSV file as source of device to be claimed
        4. Verify device was claimed by getting (via API and UI) list of customers' devices and searching devices' and
        verify devices have uploaded tags
        """
        create_test = WfExistingAcctNewDevices()
        device_order1 = [*brnf_sa_order_gw_devices.values()][0]
        device_order2 = [*brnf_sa_order_sw_devices.values()][0]
        assert create_test.wf_ui_add_network_csv_device(browser_instance, logged_in_storage_state, get_device_csv)
        assert create_test.verify_device_claimed(device_order1, brnf_sa_user_login_load_account), \
            f"Failure! Device was not claimed."
        assert create_test.verify_device_claimed(device_order2, brnf_sa_user_login_load_account), \
            f"Failure! Device was not claimed."
        assert create_test.wf_verify_device_tag(browser_instance, logged_in_storage_state, device_order1)
        assert create_test.wf_verify_device_tag(browser_instance, logged_in_storage_state, device_order2)

    @pytest.mark.order(11)
    @pytest.mark.Regression
    def test_assign_iap_device(self, brnf_sa_order_iap_devices,
                               brnf_sa_user_login_load_account):
        """
         ===== Manually add IAP into account and verify auto assignment ======
         1. Using the login session
         2. Manually add IAP into account and verify auto assignment
         3. Verify the IAP is added to the account and assign to the application correctly
         """
        time.sleep(7)
        device_type = "IAP"
        devices_details = [brnf_sa_order_iap_devices]
        create_test = WfExistingAcctNewDevices()
        assert create_test.wf_new_device_app_assignment(device_type,
                                                        devices_details,
                                                        brnf_sa_user_login_load_account)

    @pytest.mark.order(12)
    @pytest.mark.Regression
    def test_assign_sw_device(self, brnf_sa_order_sw_devices,
                              brnf_sa_user_login_load_account):
        """
         ===== Manually add IAP into account and verify auto assignment ======
         1. Using the login session
         2. Manually add IAP into account and verify auto assignment
         3. Verify the IAP is added to the account and assign to the application correctly
         """
        time.sleep(7)
        device_type = "SWITCH"
        devices_details = [brnf_sa_order_sw_devices]
        create_test = WfExistingAcctNewDevices()
        assert create_test.wf_new_device_app_assignment(device_type,
                                                        devices_details,
                                                        brnf_sa_user_login_load_account)

    @pytest.mark.order(13)
    @pytest.mark.Regression
    def test_assign_gw_device(self, brnf_sa_order_gw_devices,
                              brnf_sa_user_login_load_account):
        """
         ===== Manually add IAP into account and verify auto assignment ======
         1. Using the login session
         2. Manually add IAP into account and verify auto assignment
         3. Verify the IAP is added to the account and assign to the application correctly
         """
        time.sleep(7)
        device_type = "GATEWAY"
        devices_details = [brnf_sa_order_gw_devices]
        create_test = WfExistingAcctNewDevices()
        assert create_test.wf_new_device_app_assignment(device_type,
                                                        devices_details,
                                                        brnf_sa_user_login_load_account)

    @pytest.mark.testrail(id=1220622)
    @pytest.mark.Regression
    @pytest.mark.order(14)
    def test_audit_log_iap_device_claim_c1220622(self, browser_instance,
                                                 logged_in_storage_state,
                                                 brnf_sa_order_iap_devices):
        create_test = WfExistingAcctNewDevices()
        devices_details = [brnf_sa_order_iap_devices]
        dev_audit_logs = False
        for i in range(2):
            dev_audit_logs = create_test.wf_dev_claim_audit_log_info(browser_instance,
                                                                     logged_in_storage_state, devices_details)
            if dev_audit_logs:
                break
            else:
                time.sleep(3)
        assert dev_audit_logs

    @pytest.mark.testrail(id=1220622)
    @pytest.mark.order(15)
    @pytest.mark.Regression
    def test_audit_log_device_claim_c1220622(self, browser_instance,
                                             logged_in_storage_state,
                                             brnf_sa_order_sw_devices,
                                             brnf_sa_order_gw_devices):
        create_test = WfExistingAcctNewDevices()
        devices_details = [brnf_sa_order_sw_devices, brnf_sa_order_gw_devices]
        assert create_test.wf_dev_claim_audit_log_info(browser_instance, logged_in_storage_state, devices_details)

    @pytest.mark.testrail(id=1220666)
    @pytest.mark.order(16)
    @pytest.mark.Regression
    def test_subs_iap_evals_license_c1220666(self,
                                             brnf_sa_order_iap_devices, brnf_sa_user_login_load_account
                                             ):
        """
        ===== Assign eval license to IAP ======
        1. Using the login session
        2. Manually assign license to IAP
        3. Verify the license is assigned correctly
        """
        create_test = WfExistingAcctNewDevices()
        device_type = "IAP"
        subs_assign_logs = False
        for i in range(2):
            subs_assign_logs = create_test.wf_assign_subs_eval(
                device_type, brnf_sa_order_iap_devices, brnf_sa_user_login_load_account
            )
            if subs_assign_logs:
                break
            time.sleep(3)
        assert subs_assign_logs

    @pytest.mark.testrail(id=1220666)
    @pytest.mark.order(17)
    @pytest.mark.Regression
    def test_subs_sw_evals_license_c1220666(self,
                                            brnf_sa_order_sw_devices, brnf_sa_user_login_load_account
                                            ):
        """
        ===== Assign eval license to Switch ======
        1. Using the login session
        2. Manually assign license to Switch
        3. Verify the license is assigned correctly
        """
        create_test = WfExistingAcctNewDevices()
        device_type = "SWITCH"
        assert create_test.wf_assign_subs_eval(
            device_type, brnf_sa_order_sw_devices, brnf_sa_user_login_load_account
        )

    @pytest.mark.testrail(id=1220666)
    @pytest.mark.order(18)
    @pytest.mark.Regression
    def test_subs_gw_evals_license_c1220666(self, brnf_sa_order_gw_devices, brnf_sa_user_login_load_account):
        """
        ===== Assign eval license to Gateway ======
        1. Using the login session
        2. Manually assign license to Gateway
        3. Verify the license is assigned correctly
        """
        create_test = WfExistingAcctNewDevices()
        device_type = "GATEWAY"
        assert create_test.wf_assign_subs_eval(
            device_type, brnf_sa_order_gw_devices, brnf_sa_user_login_load_account
        )

    @pytest.mark.testrail(id=1220635)
    @pytest.mark.Regression
    @pytest.mark.order(19)
    def test_get_devices_by_acid_iap_c1220635(self,
                                              brnf_sa_user_login_load_account,
                                              brnf_app_api_session,
                                              brnf_sa_order_iap_devices,
                                              request
                                              ):
        SkipTest.skip_if_triton_lite()
        Regression_Secondary = get_pytest_marker(request, "Regression_Secondary")
        """
        ===== Using App Api verify devices assigned to application customer ID======
        1. Using the App Api client and secret
        2. Make get devices by acid
        3. verify there are 3 devices shown in response
        """
        app_cid = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_app_cid"]
        device_serial_iap = brnf_sa_order_iap_devices["device_IAP0"]["serial_no"]
        get_devices_by_acid = False
        for i in range(1, 3):
            get_devices_by_acid = VerifyByApi.verify_get_devices_by_acid(brnf_sa_user_login_load_account,
                                                                         brnf_app_api_session,
                                                                         device_serial_iap,
                                                                         app_cid
                                                                         )
            if get_devices_by_acid:
                break
            time.sleep(3)
        assert get_devices_by_acid

        if Regression_Secondary:
            for i in range(1, 3):
                get_devices_by_acid = VerifyByApi.verify_get_devices_by_acid(brnf_sa_user_login_load_account,
                                                                             brnf_app_api_session,
                                                                             device_serial_iap,
                                                                             app_cid,
                                                                             secondary=True
                                                                             )
                if get_devices_by_acid:
                    break
                time.sleep(3)
            assert get_devices_by_acid

    @pytest.mark.testrail(id=1220635)
    @pytest.mark.Regression
    @pytest.mark.order(20)
    def test_get_devices_by_acid_sw_gw_c1220635(self,
                                                brnf_sa_user_login_load_account,
                                                brnf_app_api_session,
                                                brnf_sa_order_sw_devices,
                                                brnf_sa_order_gw_devices
                                                ):
        SkipTest.skip_if_triton_lite()
        """
        ===== Using App Api verify devices assigned to application customer ID======
        1. Using the App Api client and secret
        2. Make get devices by acid
        3. verify there are 3 devices shown in response
        """
        device_serial_sw = brnf_sa_order_sw_devices["device_SWITCH0"]["serial_no"]
        app_cid = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_app_cid"]
        assert VerifyByApi.verify_get_devices_by_acid(brnf_sa_user_login_load_account,
                                                      brnf_app_api_session,
                                                      device_serial_sw,
                                                      app_cid
                                                      )
        device_serial_gw = brnf_sa_order_gw_devices["device_GATEWAY0"]["serial_no"]
        assert VerifyByApi.verify_get_devices_by_acid(brnf_sa_user_login_load_account,
                                                      brnf_app_api_session,
                                                      device_serial_gw,
                                                      app_cid
                                                      )

    @pytest.mark.testrail(id=1220635)
    @pytest.mark.Regression
    @pytest.mark.order(21)
    def test_get_devices_by_pcid_iap_c1220635(self,
                                              brnf_sa_user_login_load_account,
                                              brnf_app_api_session,
                                              brnf_sa_order_iap_devices,
                                              request
                                              ):
        SkipTest.skip_if_triton_lite()
        Regression_Secondary = get_pytest_marker(request, "Regression_Secondary")
        """
        ===== Using App Api verify devices assigned to platform customer ID======
        1. Using the App Api client and secret
        2. Make get devices by pcid
        3. verify there are 3 devices shown in response
        """
        platform_cust_id = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1"]
        device_serial_iap = brnf_sa_order_iap_devices["device_IAP0"]["serial_no"]
        get_devices_by_pcid = False
        for i in range(1, 3):
            get_devices_by_pcid = VerifyByApi.verify_get_devices_by_pcid(brnf_sa_user_login_load_account,
                                                                         brnf_app_api_session,
                                                                         device_serial_iap,
                                                                         platform_cust_id)
            if get_devices_by_pcid:
                log.info(get_devices_by_pcid)
                break
            time.sleep(3)
        assert get_devices_by_pcid

        if Regression_Secondary:
            for i in range(1, 3):
                get_devices_by_pcid = VerifyByApi.verify_get_devices_by_pcid(brnf_sa_user_login_load_account,
                                                                             brnf_app_api_session,
                                                                             device_serial_iap,
                                                                             platform_cust_id,
                                                                             secondary=True)
                if get_devices_by_pcid:
                    log.info(get_devices_by_pcid)
                    break
                time.sleep(3)
            assert get_devices_by_pcid

    @pytest.mark.testrail(id=1220635)
    @pytest.mark.Regression
    @pytest.mark.order(22)
    def test_get_devices_by_pcid_sw_gw_c1220635(self,
                                                brnf_sa_user_login_load_account,
                                                brnf_app_api_session,
                                                brnf_sa_order_sw_devices,
                                                brnf_sa_order_gw_devices):
        SkipTest.skip_if_triton_lite()
        """
        ===== Using App Api verify devices assigned to platform customer ID======
        1. Using the App Api client and secret
        2. Make get devices by pcid
        3. verify there are 3 devices shown in response
        """
        platform_cust_id = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1"]
        device_serial_sw = brnf_sa_order_sw_devices["device_SWITCH0"]["serial_no"]
        assert VerifyByApi.verify_get_devices_by_pcid(brnf_sa_user_login_load_account,
                                                      brnf_app_api_session,
                                                      device_serial_sw,
                                                      platform_cust_id
                                                      )
        device_serial_gw = brnf_sa_order_gw_devices["device_GATEWAY0"]["serial_no"]
        assert VerifyByApi.verify_get_devices_by_pcid(brnf_sa_user_login_load_account,
                                                      brnf_app_api_session,
                                                      device_serial_gw,
                                                      platform_cust_id
                                                      )

    @pytest.mark.testrail(id=1220635)
    @pytest.mark.Regression
    @pytest.mark.order(23)
    def test_get_sm_by_acid_c1220635(self, brnf_sa_user_login_load_account, request):
        Regression_Secondary = get_pytest_marker(request, "Regression_Secondary")
        """
        ===== Using App Api verify subscriptions assigned to application customer ID======
        1. Using the App Api client and secret
        2. Make get subscriptions by acid
        3. verify there are 3 devices shown in response
        """
        create_test = WfExistingAcctNewDevices()
        assert create_test.wf_sm_app_subscription_info_acid(brnf_sa_user_login_load_account)
        if Regression_Secondary:
            assert create_test.wf_sm_app_subscription_info_acid(brnf_sa_user_login_load_account, secondary=True)

    @pytest.mark.testrail(id=1220635)
    @pytest.mark.Regression
    @pytest.mark.order(24)
    def test_get_sm_by_pcid_c1220635(self, brnf_sa_user_login_load_account, request):
        SkipTest.skip_if_triton_lite()
        Regression_Secondary = get_pytest_marker(request, "Regression_Secondary")

        """
        ===== Using App Api verify subscriptions assigned to platform customer ID======
        1. Using the App Api client and secret
        2. Make get subscriptions by pcid
        3. verify there are 3 devices shown in response
        """
        create_test = WfExistingAcctNewDevices()
        assert create_test.wf_sm_app_subscription_info_pcid(brnf_sa_user_login_load_account)
        if Regression_Secondary:
            assert create_test.wf_sm_app_subscription_info_pcid(brnf_sa_user_login_load_account, secondary=True)

    @pytest.mark.testrail(id=1220635)
    @pytest.mark.order(25)
    @pytest.mark.Regression
    def test_get_audit_log_sm_details_c1220635(self, browser_instance,
                                               logged_in_storage_state,
                                               brnf_sa_order_iap_devices,
                                               brnf_sa_order_sw_devices,
                                               brnf_sa_order_gw_devices,
                                               brnf_sa_user_login_load_account):
        create_test = WfExistingAcctNewDevices()
        devices_details = brnf_sa_order_iap_devices, brnf_sa_order_sw_devices, brnf_sa_order_gw_devices
        assert create_test.wf_sm_audit_log_info(
            browser_instance, logged_in_storage_state, devices_details, brnf_sa_user_login_load_account
        )

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.Regression
    @pytest.mark.parametrize("endpoint, x_type, fw_version", [
        pytest.param("/firmware", "firmware-check", "8.4.0.0-8.4.0.0_70043",
                     marks=[pytest.mark.testrail(id=1313776), pytest.mark.order(26)], id="firmware-check_C1313776"),
        pytest.param("/firmware", "firmware-baseversion-iap", "8.5.0.5-8.5.0.5_73491",
                     marks=[pytest.mark.testrail(id=1313778), pytest.mark.order(27)],
                     id="firmware-baseversion-iap_C1313778"),
        pytest.param("/firmware", "firmware-baseversion-gateway", "8.5.0.5-8.5.0.5_73491",
                     marks=[pytest.mark.testrail(id=1313779), pytest.mark.order(28)],
                     id="firmware-baseversion-gateway_C1313779"),
        pytest.param("/firmware", "firmware-upgrade", "8.4.0.0-8.4.0.0_70043",
                     marks=[pytest.mark.testrail(id=1313777), pytest.mark.order(29)], id="firmware-upgrade_C1313777")])
    def test_iap_dev_firmware(self, brnf_sa_iap_firmware, endpoint, x_type, fw_version):
        """
        ===== Using device firmware Api call to verify devices can get the firmware URL======
            :param endpoint: firmware endpoint for IAP device
            :param x_type: firmware request for firmware checks, upgrade, base firmware version for IAP device
            :param fw_version: firmware version for IAP device
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device firmware call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_iap_firmware
        assert response.status_code == expected_response_data["iap_fw_prov_positive"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["iap_fw_prov_positive"]["X-Status-Code"]
        assert response.headers.get('X-alternative-image-server-list') is not None
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()
        assert response.headers["X-Mode"] == expected_response_data["iap_fw_prov_positive"]["X-Mode"]
        assert "http://" in response.text

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.Regression
    @pytest.mark.order(30)
    @pytest.mark.testrail(id=1220674)
    def test_iap_dev_prov_c1220674(self, brnf_sa_iap_prov):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_iap_prov
        assert response.status_code == expected_response_data["iap_fw_prov_positive"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["iap_fw_prov_positive"]["X-Status-Code"]
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()
        assert response.headers["X-Athena-Url"] is not None
        assert response.headers["X-Mode"] == expected_response_data["iap_fw_prov_positive"]["X-Mode"]

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.Regression
    @pytest.mark.parametrize('api_path, x_type', [
        pytest.param("hpe-provision", "provision-update",
                     marks=[pytest.mark.testrail(id=1220677), pytest.mark.order(31)],
                     id='ftpm_provision_C1220677'),
        pytest.param("hpe-provision-rtpm", "provision-update",
                     marks=[pytest.mark.testrail(id=1220678), pytest.mark.order(32)],
                     id='rtpm_provision_C1220678'),
        pytest.param("cx-provision", "provision-update",
                     marks=[pytest.mark.testrail(id=1220681), pytest.mark.order(33)],
                     id='cx-provision_C1220681')])
    def test_sw_dev_prov_success(self, brnf_sa_sw_prov, api_path, x_type):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_sw_prov
        assert response.status_code == expected_response_data['switch_provision_success']['response_code']
        assert response.headers["X-Status-Code"] == expected_response_data['switch_provision_success'][
            'X-Status-Code']
        assert response.headers["X-Activation-Key"] is not None
        assert len(response.headers["X-Activation-Key"]) == 8
        if api_path != "cx-provision":
            assert response.headers["X-Athena-Url"] is not None

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    @pytest.mark.Regression
    @pytest.mark.parametrize('api_path, x_type', [
        pytest.param("hpe-firmware", "firmware-check", marks=[pytest.mark.testrail(id=1313780), pytest.mark.order(34)],
                     id='ftpm_firmware_check_C1313780'),
        pytest.param("hpe-firmware-rtpm", "firmware-check",
                     marks=[pytest.mark.testrail(id=1313782), pytest.mark.order(35)],
                     id='rtpm_firmware_check_C1313782')])
    def test_sw_dev_firmware(self, brnf_sa_sw_prov, api_path, x_type):
        """
        ===== Using firmware Api call to verify devices can get the firmware URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device firmware call
        3. verify the call has 'X-Status-Code': 'success' +  firmware urls in the response
        """
        response = brnf_sa_sw_prov
        assert response.status_code == expected_response_data['switch_firmware_response']['response_code']
        assert response.headers["X-Status-Code"] == expected_response_data['switch_firmware_response'][
            'X-Status-Code']
        assert response.headers["X-Activation-Key"] is not None
        assert len(response.headers["X-Activation-Key"]) == 8
        assert "http://" in response.text

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.Regression
    @pytest.mark.order(36)
    def test_gw_dev_prov(self, brnf_sa_gw_prov):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_gw_prov
        assert response.headers.get('X-Status-Code') == "success"

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.Regression
    @pytest.mark.order(37)
    @pytest.mark.testrail(id=1220680)
    def test_cntrl_dev_prov_c1220680(self, brnf_sa_manual_claim_contrl_device, brnf_sa_cntrl_prov):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        assert brnf_sa_manual_claim_contrl_device
        response = brnf_sa_cntrl_prov
        assert response.status_code == expected_response_data["controller_provision_success"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["controller_provision_success"][
            "X-Status-Code"]
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.Regression
    @pytest.mark.parametrize("endpoint, x_type, fw_version", [
        pytest.param("/firmware", "firmware-baseversion-iap", "10.1.0.0_76785",
                     marks=[pytest.mark.testrail(id=1313786), pytest.mark.order(38)],
                     id="firmware-baseversion-iap_c1313786"),
        pytest.param("/firmware", "firmware-baseversion-gateway", "10.1.0.0_76785",
                     marks=[pytest.mark.testrail(id=1313787), pytest.mark.order(39)],
                     id="firmware-baseversion-gateway_c1313787"), ])
    def test_cntrl_dev_firmware(self, brnf_sa_contrl_firmware, endpoint, x_type, fw_version):
        """
        ===== Using device firmware Api call to verify devices can get the firmware URL======
            :param api_path: firmware endpoint for IAP device
            :param x_type: firmware request for firmware checks, upgrade, base firmware version for IAP device
            :param fw_version: firmware version for IAP device
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device firmware call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_contrl_firmware
        assert response.status_code == expected_response_data["controller_firmware_response"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["controller_firmware_response"][
            "X-Status-Code"]
        assert response.headers.get('X-alternative-image-server-list') is not None
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()
        assert response.headers["X-Mode"] == expected_response_data["controller_firmware_response"]["X-Mode"]
        assert "http://" in response.text

    @pytest.mark.order(40)
    @pytest.mark.Regression
    def test_user_at_users_page(self, browser_instance, logged_in_storage_state):
        create_test = WfExistingAcctNewDevices()
        assert create_test.wf_users_page(browser_instance, logged_in_storage_state)

    @pytest.mark.order(41)
    @pytest.mark.Regression
    def test_search_at_roles_page(self, browser_instance, logged_in_storage_state):
        create_test = WfExistingAcctNewDevices()
        assert create_test.wf_roles_page(browser_instance, logged_in_storage_state)

    @pytest.mark.order(42)
    @pytest.mark.Regression
    def test_search_at_devices_page(self, browser_instance,
                                    logged_in_storage_state,
                                    brnf_sa_order_iap_devices,
                                    brnf_sa_order_sw_devices,
                                    brnf_sa_order_gw_devices):
        create_test = WfExistingAcctNewDevices()
        devices_details = brnf_sa_order_iap_devices, brnf_sa_order_sw_devices, brnf_sa_order_gw_devices
        assert create_test.wf_devices_page(browser_instance, logged_in_storage_state, devices_details)

    @pytest.mark.order(43)
    @pytest.mark.Regression
    def test_heading_at_my_applications_page(self, browser_instance, logged_in_storage_state):
        create_test = WfExistingAcctNewDevices()
        assert create_test.wf_applications_page(browser_instance, logged_in_storage_state)

    @pytest.mark.order(44)
    @pytest.mark.Regression
    def test_subscription_at_dev_subscriptions_page(self, browser_instance,
                                                    logged_in_storage_state,
                                                    brnf_sa_order_iap_devices,
                                                    brnf_sa_order_sw_devices,
                                                    brnf_sa_order_gw_devices):
        create_test = WfExistingAcctNewDevices()
        devices_details = brnf_sa_order_iap_devices, brnf_sa_order_sw_devices, brnf_sa_order_gw_devices
        assert create_test.wf_subscriptions_page(browser_instance, logged_in_storage_state, devices_details)
