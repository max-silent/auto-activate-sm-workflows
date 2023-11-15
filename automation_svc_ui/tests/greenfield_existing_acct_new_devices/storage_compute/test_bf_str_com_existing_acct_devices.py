import logging
import os
import time

import allure
import pytest

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.conftest import get_add_device_expected_responses
from automation_svc_ui.local_libs.subscription_mgmt.sm_assignments_by_api import SMAssignments
from automation_svc_ui.tests.greenfield_existing_acct_new_devices.storage_compute \
    .brnf_str_com_existing_acct_devices import WfScExistingAcctDevices

log = logging.getLogger(__name__)

expected_response_data = get_add_device_expected_responses()


@pytest.mark.skipif("polaris" in ExistingUserAcctDevices.login_page_url, reason="Not supported on polaris.")
@pytest.mark.skipif("pavo" in ExistingUserAcctDevices.login_page_url, reason="Not supported on pavo.")
@pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
@allure.parent_suite("activate-sm-workflows")
@allure.suite("Greenfield storage compute devices - service_centric_ui")
@allure.sub_suite("Greenfield existing account new storage compute devices")
class TestBrownfieldStorageComputeNewDevicesSvc:
    @pytest.mark.order(1)
    @pytest.mark.testrail(id=1220581)
    @pytest.mark.Plv
    @pytest.mark.Regression
    def test_sc_storage_legacy_devices_c1220581(self, order_sc_storage_legacy_devices):
        """
        ===== Create Storage device on Activate order process ======
        1. Run AOP API manufacturing API to create Storage device
        """
        assert order_sc_storage_legacy_devices

    @pytest.mark.order(2)
    @pytest.mark.testrail(id=1220582)
    @pytest.mark.Regression
    def test_sc_compute_devices_c1220582(self, order_sc_compute_devices):
        """
        ===== Create Gateway device on Activate order process ======
        1. Run AOP API manufacturing API to create Gateway network device
        """
        assert order_sc_compute_devices

    @pytest.mark.order(3)
    @pytest.mark.Plv
    @pytest.mark.Regression
    def test_brnf_sc_user_login_load_account(self, brnf_sa_sc_user_login_load_account):
        """
        ===== User login to the account using user API for other tests to run user api ======
        1. User login to the account using new user and password
        2. User load the pcid account for other tests to run user api for other subsequent test cases
        """
        assert brnf_sa_sc_user_login_load_account

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.order(4)
    @pytest.mark.testrail(id=1313769)
    @pytest.mark.Regression
    def test_storage_dev_prov_fail_prov_no_rule_c1313769(self, brnf_sa_sc_storage_prov):
        """
        ===== Using device provisioning Api call to verify devices can  get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail_prov_no_rule'
        """
        response = brnf_sa_sc_storage_prov
        assert response.status_code == expected_response_data["storage_negative"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["storage_negative"]["X-Status-Code"]

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.order(5)
    @pytest.mark.testrail(id=1313770)
    @pytest.mark.Regression
    def test_dhci_storage_dev_prov_fail_prov_no_rule_c1313770(self, brnf_sa_sc_dhci_storage_prov):
        """
        ===== Using device provisioning Api call to verify devices can  get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail_prov_no_rule'
        """
        response = brnf_sa_sc_dhci_storage_prov
        assert response.status_code == expected_response_data["storage_negative"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["storage_negative"]["X-Status-Code"]

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.order(6)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1313771)
    def test_compute_dev_prov_fail_prov_no_rule_c1313771(self, brnf_sa_sc_compute_prov):
        """
        ===== Using device provisioning Api call to verify devices can  get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to  the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail_prov_no_rule'
        """
        response = brnf_sa_sc_compute_prov
        assert response.status_code == expected_response_data["compute_negative"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["compute_negative"]["X-Status-Code"]

    @pytest.mark.order(7)
    @pytest.mark.testrail(id=1220624)
    @pytest.mark.Plv
    @pytest.mark.Regression
    def test_brnf_sc_manual_storage_claim_c220624(self,
                                                  brnf_sa_sc_manual_claim_storage_device,
                                                  brnf_sa_sc_user_login_load_account
                                                  ):
        """
        ===== Manually add IAP into account and verify auto assignment ======
        1. Using the login session
        2. Manually add IAP into account and verify auto assignment
        3. Verify the IAP is added to the account and assign to the application correctly
        """
        if brnf_sa_sc_user_login_load_account:
            assert brnf_sa_sc_manual_claim_storage_device

    @pytest.mark.order(8)
    @pytest.mark.testrail(id=1220636)
    @pytest.mark.Regression
    def test_brnf_sc_manual_compute_ui_csv_claim_c1220636(self,
                                                          browser_instance,
                                                          logged_in_storage_state,
                                                          order_sc_compute_devices,
                                                          brnf_sa_sc_user_login_load_account,
                                                          get_device_csv
                                                          ):
        """
        ===== Using UI claim device by uploading CSV file======
        1. Login to GLCP via UI
        2. Go to Device Inventory page
        3. Pick CSV file as source of device to be claimed
        4. Verify device was claimed by getting (via API and UI) list of customers' devices and searching devices' and
        verify devices have uploaded tags
        """
        create_test = WfScExistingAcctDevices()
        device_order1 = [*order_sc_compute_devices.values()][0]
        assert create_test.wf_ui_add_compute_csv_device(browser_instance, logged_in_storage_state, get_device_csv)
        assert create_test.verify_device_claimed(device_order1, brnf_sa_sc_user_login_load_account), \
            f"Failure! Device was not claimed."
        assert create_test.wf_ui_verify_device_tag(browser_instance, logged_in_storage_state, device_order1)

    @pytest.mark.order(9)
    @pytest.mark.testrail(id=1220583)
    @pytest.mark.Regression
    def test_brnf_sc_get_devices_by_acid_c1220583(self, brnf_sa_sc_user_login_load_account):
        """
        ===== Using App Api verify devices assigned to application customer ID======
        1. Using the App Api client and secret
        2. Make get devices by acid
        3. verify there are devices shown in response
        """
        create_test = WfScExistingAcctDevices()
        assert create_test.wf_sc_adi_get_devices_by_acid(brnf_sa_sc_user_login_load_account)

    @pytest.mark.order(10)
    @pytest.mark.testrail(id=1220584)
    @pytest.mark.Regression
    def test_brnf_sc_get_devices_by_pcid_c1220584(self, brnf_sa_sc_user_login_load_account):
        """
        ===== Using App Api verify devices assigned to platform customer ID======
        1. Using the App Api client and secret
        2. Make get devices by pcid
        3. verify there are devices shown in response
        """
        create_test = WfScExistingAcctDevices()
        assert create_test.wf_sc_adi_get_devices_by_pcid(brnf_sa_sc_user_login_load_account)

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.order(11)
    @pytest.mark.testrail(id=1220684)
    @pytest.mark.Regression
    def test_storage_dev_prov_c1220684(self, brnf_sa_sc_storage_prov):
        """
        ===== Using device provisioning Api call to verify devices can get get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_sc_storage_prov
        assert response.status_code == expected_response_data["st_com_prov_positive"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["st_com_prov_positive"]["X-Status-Code"]
        assert response.headers["X-Athena-Url"] is not None
        assert response.headers["X-Mode"] == expected_response_data["st_com_prov_positive"]["X-Mode_Stor"]
        assert response.headers["X-Activation-Key"] is not None

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.order(12)
    @pytest.mark.testrail(id=1220685)
    @pytest.mark.Regression
    def test_dhci_storage_dev_prov_c1220685(self, brnf_sa_sc_dhci_storage_prov,
                                            brnf_sa_sc_manual_claim_dhci_storage_device):
        """
        ===== Using device provisioning Api call to verify devices can get get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        assert brnf_sa_sc_manual_claim_dhci_storage_device
        response = brnf_sa_sc_dhci_storage_prov
        assert response.status_code == expected_response_data["st_com_prov_positive"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["st_com_prov_positive"]["X-Status-Code"]
        assert response.headers["X-Athena-Url"] is not None
        assert response.headers["X-Mode"] == expected_response_data["st_com_prov_positive"]["X-Mode_Stor"]
        assert response.headers["X-Activation-Key"] is not None

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.order(13)
    @pytest.mark.testrail(id=1220686)
    @pytest.mark.Regression
    def test_compute_dev_prov_c1220686(self, brnf_sa_sc_compute_prov):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        log.info("Add delay for the device to be claimed in account and assign to application")
        time.sleep(10)
        response = brnf_sa_sc_compute_prov
        log.info(response)
        assert response.status_code == expected_response_data["st_com_prov_positive"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["st_com_prov_positive"]["X-Status-Code"]
        assert response.headers["X-Athena-Url"] is not None
        assert response.headers["X-Mode"] == expected_response_data["st_com_prov_positive"]["X-Mode_Comp"]
        assert "message" in response.text

    @pytest.mark.order(14)
    @pytest.mark.testrail(id=1220607)
    @pytest.mark.Regression
    def test_sm_subs_compute_new_subscription_key_c1220607(self, brnf_sa_new_brim_subs_compute_iaas,
                                                           brnf_sa_sc_user_login_load_account,
                                                           device_type="COMPUTE"):
        """
          ===== Assign BRIM license to COMPUTE device ======
          1. Using the login session
          2. Manually unassign app
          3. Manually assign app
          4. Assign license to COMPUTE device
          3. Verify the license is assigned correctly
          """
        if brnf_sa_sc_user_login_load_account:
            assert SMAssignments.wf_create_new_subscription_assign_to_device(
                device_type=device_type, brnf_sa_new_brim_subs_device=brnf_sa_new_brim_subs_compute_iaas,
                brnf_sa_user_login_load_account=brnf_sa_sc_user_login_load_account)

    @pytest.mark.order(15)
    @pytest.mark.testrail(id=1220608)
    @pytest.mark.Regression
    def test_sm_subs_storage_new_subscription_key_c1220608(self, brnf_sa_new_brim_subs_storage_baas,
                                                           brnf_sa_sc_user_login_load_account,
                                                           device_type="STORAGE"):
        """
          ===== Assign BRIM license to COMPUTE device ======
          1. Using the login session
          2. Manually unassign app
          3. Manually assign app
          4. Assign license to STORAGE device
          3. Verify the license is assigned correctly
          """
        if brnf_sa_sc_user_login_load_account:
            assert SMAssignments.wf_create_new_subscription_assign_to_device(
                device_type=device_type, brnf_sa_new_brim_subs_device=brnf_sa_new_brim_subs_storage_baas,
                brnf_sa_user_login_load_account=brnf_sa_sc_user_login_load_account)

    @pytest.mark.order(16)
    @pytest.mark.Regression
    def test_sm_subs_compute_new_gecko_subscription_key(self, brnf_sa_new_brim_subs_compute_gecko,
                                                        brnf_sa_sc_user_login_load_account,
                                                        device_type="COMPUTE"):
        """
          ===== Assign Gecko device to it's subscription ======
          1. Create Gecko Subscription
          2. Create the devices in the subscription
          3. Using the login session
          4. Manually claim the subscription
          5. Manually claim the device
          6. Manually un-assign the app from the device
          7. Manually assign the app to the device
          8. Assign Gecko subscription to its device
          9. Verify subscription assignment to the device
        """
        if brnf_sa_sc_user_login_load_account:
            assert SMAssignments.wf_create_new_gecko_subscription_assign_to_device(
                device_type=device_type, brnf_sa_new_brim_subs_device=brnf_sa_new_brim_subs_compute_gecko,
                brnf_sa_user_login_load_account=brnf_sa_sc_user_login_load_account)

    @pytest.mark.order(17)
    @pytest.mark.testrail(id=1220609)
    @pytest.mark.Regression
    def test_sm_subs_hciaas_new_subscription_key_c1220609(self, brnf_sa_new_brim_subs_hciaas_baas,
                                                          brnf_sa_sc_user_login_load_account,
                                                          device_type="STORAGE"):
        """
          ===== Assign BRIM license to COMPUTE device ======
          1. Using the login session
          2. Create new subscription for HCIaaS, with devices, add new sub to account
          3. Create new device with the same name as in new subscription
          4. Manually unassign app. Manually assign app
          5. Claim device and assign license to STORAGE new device
          6. Verify the license is assigned correctly
          """
        if brnf_sa_sc_user_login_load_account:
            assert SMAssignments.wf_create_new_gecko_subscription_assign_to_device(
                device_type=device_type, brnf_sa_new_brim_subs_device=brnf_sa_new_brim_subs_hciaas_baas,
                brnf_sa_user_login_load_account=brnf_sa_sc_user_login_load_account)

    @pytest.mark.order(18)
    @pytest.mark.testrail(id=1220646)
    @pytest.mark.Regression
    def test_add_tag_to_list_of_devices_c1220646(self,
                                                 browser_instance,
                                                 logged_in_storage_state,
                                                 order_sc_gw_devices,
                                                 order_sc_compute_devices,
                                                 order_sc_storage_legacy_devices,
                                                 brnf_sa_sc_manual_claim_storage_device,
                                                 brnf_sa_sc_manual_claim_gw_device,
                                                 brnf_sa_sc_user_login_load_account,
                                                 ):
        """
          ===== Add tag to 3 types of devices and verify it======
          1. Using the login session
          2. Create new GATEWAY, COMPUTE, STORAGE device
          3. Claim devices to account
          5. Add generic tag to each of device (via UI)
          6. Verify the tag is assigned correctly (via API)
          """
        test = WfScExistingAcctDevices()
        device_orders = [
            *order_sc_compute_devices.values(),
            *order_sc_storage_legacy_devices.values(),
            *order_sc_gw_devices.values()
        ]
        devices_serials = [_.get("serial_no") for _ in device_orders]
        tag_name = device_orders[0].get("serial_no")
        tag_value = device_orders[0].get("mac")
        assert test.wf_add_tag_to_device(
            browser_instance, logged_in_storage_state, device_orders, tag_name, tag_value
        ), "Failed: Could not add tag to device(s)"
        assert test.api_verify_device_tag(tag_name, tag_value, devices_serials, brnf_sa_sc_user_login_load_account), \
            "Failed: Device(s) is not in the devices list for corresponding tag"

    @pytest.mark.order(19)
    @pytest.mark.testrail(id=1221611)
    @pytest.mark.Regression
    def test_order_storage_baas_devices_c1221611(self, order_sc_storage_baas_devices):
        """
        ===== Create Storage device on Activate order process ======
        1. Run AOP API manufacturing API to create BaaS Storage device
        """
        assert order_sc_storage_baas_devices

    @pytest.mark.order(20)
    @pytest.mark.testrail(id=1221611)
    @pytest.mark.Regression
    def test_claim_storage_baas_devices_c1221611(self, browser_instance,
                                                 logged_in_storage_state,
                                                 order_sc_storage_baas_devices):
        """
        ===== Create Storage device on Activate order process ======
        1. Claim BaaS Storage device using UI.
        """
        create_test = WfScExistingAcctDevices()
        assert create_test.wf_ui_claim_storage_device(browser_instance,
                                                      logged_in_storage_state,
                                                      [order_sc_storage_baas_devices])
