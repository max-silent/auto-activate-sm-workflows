import json
import logging
import os
import time

import allure
import pytest
from hpe_glcp_automation_lib.libs.commons.utils.humio.humio_utils import HumioHelper

from automation.conftest import ExistingUserAcctDevices, get_add_device_expected_responses
from automation.local_libs.activate_inventory.verify_by_api import VerifyByApi
from automation.tests.workflows.brownfield.networking.existing_acct_existing_devices. \
    brnf_network_existing_acct_existing_devices import WfExistingAcctExistingDevices

log = logging.getLogger(__name__)
expected_response_data = get_add_device_expected_responses()
test = WfExistingAcctExistingDevices()


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices")
@allure.sub_suite("Brownfield existing account existing network devices")
@pytest.mark.Plv
class TestExistingAccountExistingDevices:
    @pytest.mark.order(1)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1441433)
    def test_brnf_user_login_load_account(self, brnf_sa_user_login_load_account):
        """
        ===== User login to the account using user API for other tests to run user api ======
        1. User login to the account using new user and password
        2. User load the pcid account for other tests to run user api for other subsequent test cases
        """
        assert brnf_sa_user_login_load_account

    @pytest.mark.order(2)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220622)
    def test_assign_iap_device(self, brnf_assign_iap_devices_to_app, brnf_sa_user_login_load_account):
        """
         ===== Manually add IAP into account and verify auto assignment ======
         1. Using the login session
         2. Manually add IAP into account and verify auto assignment
         3. Verify the IAP is added to the account and assign to the application correctly
         """
        time.sleep(7)
        if brnf_sa_user_login_load_account:
            assert brnf_assign_iap_devices_to_app

    @pytest.mark.order(3)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220622)
    def test_assign_gw_device(self, brnf_assign_sw_devices_to_app, brnf_sa_user_login_load_account):
        """
         ===== Manually add Switch into account and verify auto assignment ======
         1. Using the login session
         2. Manually add Switch into account and verify auto assignment
         3. Verify the Switch is added to the account and assign to the application correctly
         """
        if brnf_sa_user_login_load_account:
            assert brnf_assign_sw_devices_to_app

    @pytest.mark.order(4)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220622)
    def test_assign_sw_device(self, brnf_assign_gw_devices_to_app, brnf_sa_user_login_load_account):
        """
         ===== Manually add Gateway into account and verify auto assignment ======
         1. Using the login session
         2. Manually add Gateway into account and verify auto assignment
         3. Verify the Gateway is added to the account and assign to the application correctly
         """
        if brnf_sa_user_login_load_account:
            assert brnf_assign_gw_devices_to_app

    @pytest.mark.testrail(id=1220665)
    @pytest.mark.order(5)
    @pytest.mark.Regression
    def test_subs_iap_evals_license_c1220665(self, brnf_sa_manual_evals_subs_iap, brnf_sa_user_login_load_account):
        """
          ===== Assign eval license to IAP ======
          1. Using the login session
          2. Manually assign license to IAP
          3. Verify the license is assigned correctly
          """
        if brnf_sa_user_login_load_account:
            assert brnf_sa_manual_evals_subs_iap

    @pytest.mark.testrail(id=1220665)
    @pytest.mark.order(6)
    @pytest.mark.Regression
    def test_subs_sw_evals_license_c1220665(self, brnf_sa_manual_evals_subs_sw, brnf_sa_user_login_load_account):
        """
          ===== Assign eval license to IAP ======
          1. Using the login session
          2. Manually assign license to IAP
          3. Verify the license is assigned correctly
          """
        if brnf_sa_user_login_load_account:
            assert brnf_sa_manual_evals_subs_sw

    @pytest.mark.testrail(id=1220665)
    @pytest.mark.order(7)
    @pytest.mark.Regression
    def test_subs_gw_evals_license_c1220665(self, brnf_sa_manual_evals_subs_gw, brnf_sa_user_login_load_account):
        """
          ===== Assign eval license to IAP ======
          1. Using the login session
          2. Manually assign license to IAP
          3. Verify the license is assigned correctly
          """
        if brnf_sa_user_login_load_account:
            assert brnf_sa_manual_evals_subs_gw

    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    @pytest.mark.testrail(id=1220652)
    @pytest.mark.order(8)
    @pytest.mark.Regression
    @pytest.mark.parametrize("device_serial", ["brnf_existing_acct_existing_devices_iap_sn",
                                               "brnf_existing_acct_existing_devices_sw_sn",
                                               "brnf_existing_acct_existing_devices_gw_sn"])
    # Independently running test
    def test_get_devices_by_acid_c1220652(self, brnf_sa_user_login_load_account,
                                          adi_app_api_session,
                                          device_serial):
        """
        ===== Using App Api verify devices assigned to application customer ID======
        1. Using the App Api client and secret
        2. Make get devices by acid
        3. verify there are 3 devices shown in response
        """
        device_serial = ExistingUserAcctDevices.test_data[device_serial]
        app_cust_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_acid']
        assert VerifyByApi.verify_get_devices_by_acid(brnf_sa_user_login_load_account,
                                                      adi_app_api_session,
                                                      device_serial,
                                                      app_cust_id)

    @pytest.mark.order(9)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220652)
    @pytest.mark.parametrize("device_serial", ["brnf_existing_acct_existing_devices_iap_sn",
                                               "brnf_existing_acct_existing_devices_sw_sn",
                                               "brnf_existing_acct_existing_devices_gw_sn"])
    # Independently running test
    def test_get_devices_by_pcid(self, brnf_sa_user_login_load_account,
                                 adi_app_api_session,
                                 device_serial):
        """
        ===== Using App Api verify devices assigned to application customer ID======
        1. Using the App Api client and secret
        2. Make get devices by acid
        3. verify there are 3 devices shown in response
        """
        device_serial = ExistingUserAcctDevices.test_data[device_serial]
        platform_cust_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_pcid']
        assert VerifyByApi.verify_get_devices_by_pcid(brnf_sa_user_login_load_account,
                                                      adi_app_api_session,
                                                      device_serial,
                                                      platform_cust_id)

    @pytest.mark.order(10)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220622)
    @pytest.mark.parametrize("device_serial", ["brnf_existing_acct_existing_devices_iap_sn",
                                               "brnf_existing_acct_existing_devices_sw_sn",
                                               "brnf_existing_acct_existing_devices_gw_sn"])
    # Independently running test
    def test_get_subs_by_acid(self, brnf_sa_user_login_load_account,
                              sm_app_api_session,
                              device_serial):
        """
        ===== Using App Api verify devices assigned to application customer ID======
        1. Using the App Api client and secret
        2. Make get devices by acid
        3. verify there are 3 devices shown in response
        """
        device_serial = ExistingUserAcctDevices.test_data[device_serial]
        app_cust_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_acid']
        platform_cust_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_pcid']
        assert VerifyByApi.verify_app_subscription_info_acid(brnf_sa_user_login_load_account,
                                                             sm_app_api_session,
                                                             device_serial,
                                                             app_cust_id,
                                                             platform_cust_id)

    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    @pytest.mark.order(11)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220622)
    @pytest.mark.parametrize("device_serial", ["brnf_existing_acct_existing_devices_iap_sn",
                                               "brnf_existing_acct_existing_devices_sw_sn",
                                               "brnf_existing_acct_existing_devices_gw_sn"])
    # Independently running test
    def test_get_subs_by_pcid(self, brnf_sa_user_login_load_account,
                              sm_app_api_session,
                              device_serial):
        """
        ===== Using App Api verify devices assigned to application customer ID======
        1. Using the App Api client and secret
        2. Make get devices by acid
        3. verify there are 3 devices shown in response
        """
        device_serial = ExistingUserAcctDevices.test_data[device_serial]
        platform_cust_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_pcid']
        assert VerifyByApi.verify_app_subscription_info_pcid(brnf_sa_user_login_load_account,
                                                             sm_app_api_session,
                                                             device_serial,
                                                             platform_cust_id)

    @pytest.mark.order(12)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220622)
    def test_get_audit_log_sm_details(self, browser_instance, logged_in_storage_state, brnf_sa_user_login_load_account):
        iap_device_details = {"device_type": "IAP",
                              "serial_no": ExistingUserAcctDevices.test_data[
                                  "brnf_existing_acct_existing_devices_iap_sn"]}
        switch_device_details = {"device_type": "SWITCH",
                                 "serial_no": ExistingUserAcctDevices.test_data[
                                     "brnf_existing_acct_existing_devices_sw_sn"]}
        gateway_device_details = {"device_type": "GATEWAY",
                                  "serial_no": ExistingUserAcctDevices.test_data[
                                      "brnf_existing_acct_existing_devices_gw_sn"]}
        devices_details = iap_device_details, switch_device_details, gateway_device_details
        assert test.wf_sm_audit_log_info(browser_instance, logged_in_storage_state, devices_details,
                                         brnf_sa_user_login_load_account)

    @pytest.mark.testrail(id=1220622)
    @pytest.mark.order(13)
    @pytest.mark.Regression
    def test_check_device_history_sm_details_c1220622(self, browser_instance, logged_in_storage_state):
        iap_device_details = {"device_type": "IAP",
                              "serial_no": ExistingUserAcctDevices.test_data[
                                  "brnf_existing_acct_existing_devices_iap_sn"]}
        switch_device_details = {"device_type": "SWITCH",
                                 "serial_no": ExistingUserAcctDevices.test_data[
                                     "brnf_existing_acct_existing_devices_sw_sn"]}
        gateway_device_details = {"device_type": "GATEWAY",
                                  "serial_no": ExistingUserAcctDevices.test_data[
                                      "brnf_existing_acct_existing_devices_gw_sn"]}
        devices_details = iap_device_details, switch_device_details, gateway_device_details
        assert test.wf_sm_device_history_check(browser_instance, logged_in_storage_state, devices_details)

    @pytest.mark.testrail(id=1220622)
    @pytest.mark.order(14)
    @pytest.mark.Regression
    @pytest.mark.xfail(reason="GLCP-138746: Notification about generated exported report does not appear.")
    # Independently running test
    def test_download_inventory_csv_c1220622(self, browser_instance, logged_in_storage_state):
        assert test.wf_sm_activate_devices_download_csv_check(browser_instance, logged_in_storage_state)

    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.Regression
    @pytest.mark.order(15)
    def test_iap_dev_prov(self, existint_acct_existing_dev_brnf_sa_iap_prov):
        """
          === Using device provisioning Api call to verify devices can get get the provisioning URL======
          1. Using the device App Api make the header, and add the DNS entry to the the hosts file
          2. Make device provisioning call
          3. verify the call has 'X-Status-Code': 'success'
          """
        response = existint_acct_existing_dev_brnf_sa_iap_prov
        assert response.status_code == expected_response_data["iap_fw_prov_positive"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["iap_fw_prov_positive"]["X-Status-Code"]
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()
        assert response.headers["X-Athena-Url"] is not None
        assert response.headers["X-Mode"] == expected_response_data["iap_fw_prov_positive"]["X-Mode"]

    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.Regression
    @pytest.mark.order(16)
    @pytest.mark.testrail(id=1220622)
    def test_sw_dev_prov(self, existint_acct_existing_dev_brnf_sa_sw_prov):
        """
          ===== Using device provisioning Api call to verify devices can get get the provisioning URL======
          1. Using the device App Api make the header, and add the DNS entry to the the hosts file
          2. Make device provisioning call
          3. verify the call has 'X-Status-Code': 'success'
          """
        response = existint_acct_existing_dev_brnf_sa_sw_prov
        assert response.headers.get('X-Status-Code') == "success"
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()
        assert response.headers["X-Athena-Url"] is not None

    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.Regression
    @pytest.mark.order(17)
    @pytest.mark.testrail(id=1220622)
    def test_gw_dev_prov(self, existint_acct_existing_dev_brnf_sa_gw_prov):
        """
          ===== Using device provisioning Api call to verify devices can get get the provisioning URL======
          1. Using the device App Api make the header, and add the DNS entry to the the hosts file
          2. Make device provisioning call
          3. verify the call has 'X-Status-Code': 'success'
          """
        response = existint_acct_existing_dev_brnf_sa_gw_prov
        assert response.headers.get('X-Status-Code') == "success"

    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    @pytest.mark.testrail(id=1220697)
    @pytest.mark.Regression
    @pytest.mark.order(18)
    # Independently running test
    def test_activate_folders_page_create_c1220697(self, browser_instance,
                                                   logged_in_storage_state,
                                                   device_folder_name):
        assert test.wf_folders_page(browser_instance, logged_in_storage_state, device_folder_name)

    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    @pytest.mark.order(19)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220700)
    def test_create_rule_for_folder_c1220700(self, browser_instance, logged_in_storage_state, device_folder_name):
        assert test.wf_sm_activate_folder_add_rule_check(browser_instance, logged_in_storage_state,
                                                         device_folder_name)

    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    @pytest.mark.testrail(id=1220698)
    @pytest.mark.Regression
    @pytest.mark.order(20)
    def test_activate_folders_page_delete_c1220698(self, browser_instance,
                                                   logged_in_storage_state,
                                                   device_folder_name):
        assert test.wf_sm_activate_folder_delete_check(browser_instance, logged_in_storage_state,
                                                       device_folder_name)

    @pytest.mark.Regression
    @pytest.mark.order(21)
    @pytest.mark.skipif("polaris" in ExistingUserAcctDevices.login_page_url, reason="Not supported on polaris.")
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    @pytest.mark.skipif("pavo" in ExistingUserAcctDevices.login_page_url, reason="Not supported on pavo.")
    @pytest.mark.skipif("mira" in ExistingUserAcctDevices.login_page_url, reason="Not supported on mira.")
    def test_humio_msg_iap_prov_event_producer_di_consumer_sm(self, humio_session):
        """
         ===== Manually add IAP into account and verify auto assignment ======
         1. Search humio logs that activate inventory has produced the DEVICE_PROVISION_INTERNAL_EVENT
         2. Verify the event is consumed by subscription management
         """
        iap_sn = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_iap_sn"]
        search_str = '{} AND kafka-producer-network-thread AND DEVICE_PROVISION_INTERNAL_EVENT'.format(iap_sn)
        result_search_str = "Received kafka record: after consume"
        service_name = "subscription-management"
        search_duration_in_ms = 900000
        transaction_id = HumioHelper.get_last_event_transaction_id(humio_session, search_str)
        assert transaction_id
        assert HumioHelper.event_with_transaction_id_exists(humio_session,
                                                            transaction_id,
                                                            service_name,
                                                            result_search_str,
                                                            search_duration_in_ms
                                                            )

    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    @pytest.mark.skipif("pavo" in ExistingUserAcctDevices.login_page_url, reason="Not supported on pavo.")
    @pytest.mark.testrail(id=1302888)
    @pytest.mark.Regression
    @pytest.mark.order(22)
    # Independently running test
    def test_filter_devices_by_tiers_c1302888(self, browser_instance, logged_in_storage_state):
        """
        ===== Using App Api verify devices assigned to application customer ID======
        1. Using UI navigate to Devices Inventory page
        2. Filter devices by Tiers
        3. verify there are only devices with corresponding tiers shown in all rows of table's current page.
        """
        filtering_tiers_lists = ["Foundation AP"], ["Advanced AP"], ["Advanced-70xx/90xx"], [
            "Advanced-Switch-62xx/29xx"]
        assert test.wf_filter_devices_by_subscription_tier(browser_instance, logged_in_storage_state,
                                                           filtering_tiers_lists)

    @pytest.mark.testrail(id=1220632)
    @pytest.mark.order(23)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    # Independently running test
    def test_negative_claim_an_assigned_iap_device_c1220632(
            self, brnf_second_user_login_load_account, brnf_sa_user_login_load_account
    ):
        claimed_iap_serial_no = ExistingUserAcctDevices.test_data[
            "brnf_existing_acct_existing_devices_iap_serial_subs_mgmt"]
        claimed_iap_mac = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_iap_mac_subs_mgmt"]
        acid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_acid"]
        assert test.wf_verify_device_has_app_assignment(brnf_sa_user_login_load_account, claimed_iap_serial_no, acid), \
            "Failed: device not in expected state - it should have app assignment, but it has not"
        result = test.wf_sa_manual_claim_already_claimed_device(
            brnf_second_user_login_load_account,
            claimed_iap_serial_no,
            claimed_iap_mac,
        )
        assert isinstance(result, bytes), "Failed: Unexpected type of response content! Possible reason:" \
                                          " Already claimed device was claimed by another user!"
        response = json.loads(result)
        assert response.get("code") == 'PRECONDITION_FAILURE', \
            f"Failed: Wrong response code: {response.get('code')}"
        assert response.get("detail") == 'All devices are either blocked, invalid, or already added.', \
            f"Failed: Wrong error message: {response.get('detail')}"

    @pytest.mark.testrail(id=1220634)
    @pytest.mark.order(24)
    @pytest.mark.Regression
    # Independently running test
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_negative_claim_assigned_device_via_csv_c1220634(
            self,
            browser_instance,
            second_acc_logged_in_storage_state,
            logged_in_storage_state,
            brnf_sa_user_login_load_account
    ):
        """
        ===== Verify devices assigned to user1/account1 cannot be claimed by user2/account2======
        1. Using UI navigate to Devices Inventory page
        2. Try to add device via CSV file
        3. Search devices and verify there are no device from CSV file.
        """
        claimed_iap_serial_no = ExistingUserAcctDevices.test_data[
            "brnf_existing_acct_existing_devices_iap_serial_subs_mgmt"]
        claimed_sw_serial_no = ExistingUserAcctDevices.test_data[
            "brnf_existing_acct_existing_devices_sw_serial_subs_mgmt"]
        acid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_acid"]
        assert test.wf_verify_device_has_app_assignment(brnf_sa_user_login_load_account, claimed_iap_serial_no, acid), \
            "Failed: device not in expected state - it should have app assignment, but it has not"
        assert test.wf_verify_device_has_app_assignment(brnf_sa_user_login_load_account, claimed_sw_serial_no, acid), \
            "Failed: device not in expected state - it should have app assignment, but it has not"
        assert test.check_already_claimed_device_upload_via_csv(browser_instance, second_acc_logged_in_storage_state), \
            "Failed: Device was claimed, but it was not expected, or claim operation got wrong error message"
        assert test.check_claimed_device_remains_claimed(browser_instance, logged_in_storage_state), \
            "Failed: Device unassigned and no longer in the list of devices for account. Expected result - device " \
            "left claimed and assigned"
