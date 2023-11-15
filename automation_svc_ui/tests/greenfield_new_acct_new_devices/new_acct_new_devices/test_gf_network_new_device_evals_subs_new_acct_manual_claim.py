import logging
import os

import allure
import pytest

from automation_svc_ui.conftest import get_add_device_expected_responses, ExistingUserAcctDevices
from automation_svc_ui.tests.greenfield_new_acct_new_devices.new_acct_new_devices \
    .wf_session_new_user_acct_first_order_auto_claim import WfNewDeviceNewUserSignupCreateAcct

log = logging.getLogger(__name__)

expected_response_data = get_add_device_expected_responses()


@pytest.mark.nonsvc
@pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
@pytest.mark.skipif("pavo" in ExistingUserAcctDevices.login_page_url, reason="Not supported on pavo. Need TAC account.")
@allure.parent_suite("activate-sm-workflows")
@allure.suite("Greenfield New Account New devices - service_centric_ui")
class TestGreenfieldNewAccountNewDevicesSvc:
    @pytest.mark.testrail(id=1220580)
    @pytest.mark.Regression
    @pytest.mark.order(1)
    def test_iap_devices_c1220580(self, order_iap_devices):
        """
        ===== Create IAP device on Activate order process ======
        1. Run AOP API manufacturing API to create IAP network device
        """
        assert order_iap_devices

    @pytest.mark.testrail(id=1220580)
    @pytest.mark.Regression
    @pytest.mark.order(2)
    def test_sw_devices_c1220580(self, order_sw_devices):
        """
        ===== Create Switch device on Activate order process ======
        1. Run AOP API manufacturing API to create Switch network device
        """
        assert order_sw_devices

    @pytest.mark.testrail(id=1220580)
    @pytest.mark.Regression
    @pytest.mark.order(3)
    def test_gw_devices_c1220580(self, order_gw_devices):
        """
        ===== Create Gateway device on Activate order process ======
        1. Run AOP API manufacturing API to create Gateway network device
        """
        assert order_gw_devices

    @pytest.mark.order(4)
    @pytest.mark.Regression
    def test_create_user_create_account(self, create_user_create_account):
        """
        ===== Create user and Create accounts workflow steps ======
        1. User navigates to CCS  and to initiate the user registration process.
        2. User enters the first name last name and new email address
        3. User select the country at the signup page and click checkbox to agree and click on signup
        4. Verify the url goes to email has been sent.
        5. Verify the user receives the email for verifying the account creation.
        6. User click on the invitation email the user is presented with user login option create password.
        7. Verify the user is able to land on customer account creation page
        8. User is able to create customer with customer name, address, Country and create
        9. User is able to land on the customer page after the account is created and able to see his first name
        """
        assert create_user_create_account

    @pytest.mark.order(5)
    @pytest.mark.Regression
    def test_new_user_login_load_account(self, new_user_login_load_account):
        """
        ===== User login to the account using user API for other tests to run user api ======
        1. User login to the account using new user and password
        2. User load the pcid account for other tests to run user api for other subsequent test cases
        """
        assert new_user_login_load_account

    @pytest.mark.order(6)
    @pytest.mark.Regression
    def test_prov_app_new_acct(self, new_user_login_load_account):
        """
        ===== Provision App to the new signup account ======
        1. Using the login session
        2. Provision the app and verify the app is provisioned successfully
        """
        log.info("running test_prov_app_new_acct")
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        assert create_test.wf_prov_app_fn(new_user_login_load_account)

    @pytest.mark.order(7)
    @pytest.mark.testrail(id=1221585)
    @pytest.mark.Regression
    def test_verify_account_eval_subs_c1221585(self, new_user_login_load_account):
        """
        ===== Verifying the start time and count of EVAL subscriptions for the new signup account ======
        1. Using the login session
        2. Get account's subscriptions and verify that the start timestamp is today.
        3. Get account's subscriptions and verify that the number of them is not less than 14.
        """
        log.info("Verifying the number of EVAL subscriptions for the new signup account")
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        create_test.verify_eval_subs(new_user_login_load_account)

    @pytest.mark.testrail(id=1220625)
    @pytest.mark.order(8)
    @pytest.mark.Regression
    def test_create_alias_new_acct_c1220625(self,
                                            tac_user_login_load_account,
                                            new_user_login_load_account):
        """
        ===== Added alias to the new signup account ======
        1. Using the login session
        2. Add alias and verify it was successfully
        """
        log.info("running test_create_alias_new_acct")
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        assert create_test.wf_create_activate_verified_alias(tac_user_login_load_account, new_user_login_load_account)

    @pytest.mark.testrail(id=1220625)
    @pytest.mark.order(9)
    @pytest.mark.Regression
    @pytest.mark.parametrize("fixture_name", [
        "order_iap_devices",
        "order_sw_devices",
        "order_gw_devices",
    ])
    def test_verify_claim_c1220625(self,
                                   new_user_login_load_account,
                                   request,
                                   fixture_name):
        """
        ===== Verify devices were claimed into account and verify auto assignment ======
        1. Using the login session
        2. Verify device is added into account (claimed)
        """
        device_order = [*request.getfixturevalue(fixture_name).values()][0]
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        create_test.verify_device_claimed(device_order, new_user_login_load_account)

    @pytest.mark.testrail(id=1220666)
    @pytest.mark.order(10)
    @pytest.mark.Regression
    def test_subs_iap_evals_license_c1220666(self,
                                             order_iap_devices,
                                             new_user_login_load_account):
        """
        ===== Assign eval license to IAP ======
        1. Using the login session
        2. Manually assign license to IAP
        3. Verify the license is assigned correctly
        """
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        device_type = "IAP"
        assert create_test.wf_assign_subs_eval(
            device_type, order_iap_devices, new_user_login_load_account
        )

    @pytest.mark.testrail(id=1220666)
    @pytest.mark.order(11)
    @pytest.mark.Regression
    def test_subs_sw_evals_license_c1220666(self,
                                            order_sw_devices,
                                            new_user_login_load_account):
        """
        ===== Assign eval license to Switch ======
        1. Using the login session
        2. Manually assign license to Switch
        3. Verify the license is assigned correctly
        """
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        device_type = "SWITCH"
        assert create_test.wf_assign_subs_eval(
            device_type, order_sw_devices, new_user_login_load_account
        )

    @pytest.mark.testrail(id=1220666)
    @pytest.mark.order(12)
    @pytest.mark.Regression
    def test_subs_gw_evals_license_c1220666(self,
                                            order_gw_devices,
                                            new_user_login_load_account):
        """
        ===== Assign eval license to Gateway ======
        1. Using the login session
        2. Manually assign license to Gateway
        3. Verify the license is assigned correctly
        """
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        device_type = "GATEWAY"
        assert create_test.wf_assign_subs_eval(
            device_type, order_gw_devices, new_user_login_load_account
        )

    @pytest.mark.order(13)
    @pytest.mark.Regression
    def test_get_devices_by_acid(self, new_user_login_load_account):
        """
        ===== Using App Api verify devices assigned to application customer ID======
        1. Using the App Api client and secret
        2. Make get devices by acid
        3. verify there are 3 devices shown in response
        """
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        assert create_test.wf_adi_get_devices_by_acid(new_user_login_load_account)

    @pytest.mark.testrail(id=1220651)
    @pytest.mark.order(14)
    @pytest.mark.Regression
    def test_get_devices_by_pcid_c1220651(self, new_user_login_load_account):
        """
        ===== Using App Api verify devices assigned to platform customer ID======
        1. Using the App Api client and secret
        2. Make get devices by pcid
        3. verify there are 3 devices shown in response
        """
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        assert create_test.wf_adi_get_devices_by_pcid(new_user_login_load_account)

    @pytest.mark.testrail(id=1220667)
    @pytest.mark.order(15)
    @pytest.mark.Regression
    def test_get_sm_by_acid_c1220667(self, new_user_login_load_account):
        """
        ===== Using App Api verify subscriptions assigned to application customer ID======
        1. Using the App Api client and secret
        2. Make get subscriptions by acid
        3. verify there are 3 devices shown in response
        """
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        assert create_test.wf_sm_app_subscription_info_acid(new_user_login_load_account)

    @pytest.mark.testrail(id=1220667)
    @pytest.mark.order(16)
    @pytest.mark.Regression
    def test_get_sm_by_pcid_c1220667(self, new_user_login_load_account):
        """
        ===== Using App Api verify subscriptions assigned to platform customer ID======
        1. Using the App Api client and secret
        2. Make get subscriptions by pcid
        3. verify there are 3 devices shown in response
        """
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        assert create_test.wf_sm_app_subscription_info_pcid(new_user_login_load_account)

    @pytest.mark.order(17)
    @pytest.mark.Regression
    def test_get_audit_log_sm_details(self,
                                      browser_instance,
                                      logged_in_storage_state,
                                      order_iap_devices,
                                      order_sw_devices,
                                      order_gw_devices,
                                      new_user_login_load_account):
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        devices_details = order_iap_devices, order_sw_devices, order_gw_devices
        assert create_test.wf_sm_audit_log_info(browser_instance, logged_in_storage_state, devices_details,
                                                new_user_login_load_account)

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.order(18)
    @pytest.mark.Regression
    def test_new_iap_dev_prov(self, brnf_sa_new_iap_prov):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_new_iap_prov
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
    @pytest.mark.order(19)
    @pytest.mark.Regression
    def test_new_sw_dev_prov(self, brnf_sa_new_sw_prov):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_new_sw_prov
        assert response.headers.get('X-Status-Code') == "success"

    @pytest.mark.skipif(
        not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container"
    )
    @pytest.mark.order(20)
    @pytest.mark.Regression
    def test_new_gw_dev_prov(self, brnf_sa_new_gw_prov):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_new_gw_prov
        assert response.headers.get('X-Status-Code') == "success"

    @pytest.mark.order(21)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220627)
    def test_remove_alias_from_one_and_add_to_another_c1220627(
            self,
            order_gw_devices,
            order_sw_devices,
            new_user_login_load_account,
            login_second_user_create_account,
            tac_user_login_load_account
    ):
        """
        ===== Claims activate:ZTP remove alias from the account, from activate TAC, Device already claim should not
        be removed. Create the same alias name as deleted above on another account======
        Steps:
        1. Create two accounts:
         - one with alias
         - second without alias
        2. Create two devices and verify that:
         - Device1 is in claimed state (not assigned to any application)
         - Device2 is in assigned state (claimed and assigned to app)
        3. CCS Manager:
         - Delete alias from account1
         - Create alias for Account2 (same name)
        4. Verify Device1 and Device2 remain in Account1.
        5. Verify Account2 does not have Device1 and Device2
        """
        create_test = WfNewDeviceNewUserSignupCreateAcct()
        alias_name = new_user_login_load_account.user.split("@")[0].split("+")[1]
        pcid1 = new_user_login_load_account.pcid
        pcid2 = login_second_user_create_account.pcid
        devices = [
            *order_gw_devices.values(),
            *order_sw_devices.values()
        ]
        assert create_test.grnf_device_app_unassignment(devices[0], new_user_login_load_account), \
            "Failed: Unable to unassign device from application"
        assert tac_user_login_load_account.delete_cm_activate_alias(alias_name, pcid1), \
            "Failed: Unable to delete alias for account."
        assert tac_user_login_load_account.add_cm_activate_alias(alias_name, pcid2).get("response"), \
            "Failed: Unable to add alias to the account"
        for device in devices:
            create_test.verify_device_claimed(device, new_user_login_load_account)
            create_test.verify_device_not_claimed(device, login_second_user_create_account)
