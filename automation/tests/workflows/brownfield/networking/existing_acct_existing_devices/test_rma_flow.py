import json
import logging
import time
import allure
import pytest

from automation.conftest import ExistingUserAcctDevices
from automation.tests.workflows.brownfield.networking.existing_acct_existing_devices. \
    brnf_network_existing_acct_existing_devices import WfExistingAcctExistingDevices
from automation.local_libs.subscription_mgmt.sm_assignments_by_api import SMAssignments
from automation.conftest import SkipTest

log = logging.getLogger(__name__)
username = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_username"]
pcid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_pcid']
acid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_acid']
create_test = WfExistingAcctExistingDevices()


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices")
@allure.sub_suite("Existing account - RMA device flows")
class TestRmaDeviceFlows:

    @pytest.mark.order(1)
    @pytest.mark.Regression
    def test_brnf_user_login_load_account_c1220622(self, brnf_sa_user_login_load_account):
        """
        ===== User login to the account using user API for other tests to run user api ======
        1. User login to the account using new user and password
        2. User load the pcid account for other tests to run user api for other subsequent test cases
        """
        assert brnf_sa_user_login_load_account

    @pytest.mark.order(2)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1431670)
    def test_remove_rma_device_with_application_assigned(self, rma_app_api_session, adi_app_api_helper):
        """
        Remove a device with application assigned from customer account > claim and device back >
        make a device provisioning call
        :param rma_app_api_session: Authorization bearer token with scope rma
        :param adi_app_api_helper : Helper class to interact with the App API
        """
        assigned_device_list = adi_app_api_helper.get_multiple_device_data_for_rma(device_number=1,
                                                                                   device_status="provisioned",
                                                                                   platform_customer_id=pcid,
                                                                                   device_type='AP')

        # RMA API call to move the device to AFS
        log.info(f"Devices in provisioned state: {assigned_device_list[0]}")
        rma_response = adi_app_api_helper.remove_rma_devices_from_customer_account(rma_app_api_session,
                                                                                   device_category="NETWORK",
                                                                                   device_list=assigned_device_list)
        assert rma_response.status_code == 200
        assert rma_response.json()['message'] == "All devices Moved to Factory-Stock"

        # Claim a device back to customer account from AFS
        claim_response = adi_app_api_helper.claim_multiple_devices(assigned_device_list, pcid,
                                                                   username, app_category="NETWORK",
                                                                   acid=assigned_device_list[0][
                                                                       "application_customer_id"])
        log.info("Claim response:{}.".format(claim_response.text))
        json_response = json.loads(claim_response.text)
        assert claim_response.status_code == 200
        # claimed field will return empty if we attempt to claim the already existing device
        assert json_response["meta"]["claimed"] is not None
        log.info(f"Claim successful for serial: {assigned_device_list[0]['serial_number']}")

        # make a provision call - Success in the response
        response = create_test.brnf_nw_device_prov(assigned_device_list[0]['serial_number'],
                                                   assigned_device_list[0]['mac_address'], "IAP",
                                                   assigned_device_list[0]['part_number'])

        log.info(f"Provisioning response: {response.headers}")
        assert response.status_code == 200
        assert response.headers.get('X-Status-Code') == "success"

    @pytest.mark.order(3)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1431671)
    def test_remove_rma_device_with_subscription_assigned(self, rma_app_api_session, adi_app_api_helper,
                                                           brnf_sa_new_brim_combined_subs_ap_sw_gw,
                                                           brnf_sa_user_login_load_account, sm_app_api_session):
        """
        Remove a device with application and subscription assigned from customer account > claim and device back to
        customer account
        :param rma_app_api_session: Authorization bearer token with scope rma
        :param adi_app_api_helper : Helper class to interact with the App API
        """
        assigned_device_list = adi_app_api_helper.get_multiple_device_data_for_rma(device_number=1,
                                                                                   device_status="provisioned",
                                                                                   platform_customer_id=pcid,
                                                                                   device_type='AP')
        assert brnf_sa_user_login_load_account, "'brnf_sa_user_login_load_account' not defined"

        assert SMAssignments.wf_create_new_combined_subscription_ap_sw_gw(brnf_sa_new_brim_combined_subs_ap_sw_gw,
                                                                          brnf_sa_user_login_load_account)
        ap_key, sw_key, gw_key, lic_quote = brnf_sa_new_brim_combined_subs_ap_sw_gw

        # assign subscription
        serial = assigned_device_list[0]['serial_number']
        assert SMAssignments.wf_existing_device_subscription_assignment(pcid, acid, serial, ap_key, sm_app_api_session)

        # make RMA call and move the device to Aruba Factory Stock
        rma_response = adi_app_api_helper.remove_rma_devices_from_customer_account(rma_app_api_session,
                                                                                   device_category="NETWORK",
                                                                                   device_list=assigned_device_list)
        assert rma_response.status_code == 200
        assert rma_response.json()['message'] == "All devices Moved to Factory-Stock"

        # After doing RMA, check that the device is not found in the customer account
        time.sleep(3)
        found_device = adi_app_api_helper.verify_device_claimed_by_pcid(pcid, serial)
        log.info(f"Found device: {found_device}")
        assert found_device == False

        # ADD device back to customer account with previous status(claim and assigned application) - subscription should
        # not be assigned
        claim_response = adi_app_api_helper.claim_multiple_devices(assigned_device_list, pcid,
                                                                   username, app_category="NETWORK",
                                                                   acid=assigned_device_list[0][
                                                                       "application_customer_id"])
        log.info("Claim response:{}.".format(claim_response.text))
        json_response = json.loads(claim_response.text)
        assert claim_response.status_code == 200
        # claimed field will return empty if we attempt to claim the already existing device
        assert json_response["meta"]["claimed"] is not None
        log.info(f"Claim successful for serial: {assigned_device_list[0]['serial_number']}")
