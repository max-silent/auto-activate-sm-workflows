import logging

import allure
import pytest

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.local_libs.subscription_mgmt.sm_assignments_by_api import SMAssignments

log = logging.getLogger(__name__)


@pytest.mark.nonsvc
@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield SM network devices - service_centric_ui")
@allure.sub_suite("Brownfield SM existing account existing network devices")
class TestSMExistingAccountExistingDevicesSvc:
    @pytest.mark.order(1)
    @pytest.mark.Regression
    def test_brnf_user_login_load_account(self, brnf_sa_user_login_load_account):
        """
        ===== User login to the account using user API for other tests to run user api ======
        1. User login to the account using new user and password
        2. User load the pcid account for other tests to run user api for other subsequent test cases
        """
        assert brnf_sa_user_login_load_account

    @pytest.mark.order(2)
    @pytest.mark.testrail(id=1220603)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_subs_iap_new_subscription_key_c1220603(self, brnf_sa_new_brim_subs_iap, brnf_sa_user_login_load_account,
                                                       device_type="IAP"):
        """
          ===== Assign eval license to IAP ======
          1. Using the login session
          2. Manually unassign app
          3. Manually assign app
          4. Assign license to IAP
          3. Verify the license is assigned correctly
          """
        if brnf_sa_user_login_load_account:
            assert SMAssignments.wf_create_new_subscription_assign_to_device(device_type, brnf_sa_new_brim_subs_iap,
                                                                             brnf_sa_user_login_load_account)

    @pytest.mark.order(3)
    @pytest.mark.testrail(id=1220604)
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_subs_switch_new_subscription_key_c1220604(self, brnf_sa_new_brim_subs_switch,
                                                          brnf_sa_user_login_load_account,
                                                          device_type="SWITCH"):
        """
          ===== Assign eval license to IAP ======
          1. Using the login session
          2. Manually unassign app
          3. Manually assign app
          4. Assign license to IAP
          3. Verify the license is assigned correctly
          """
        if brnf_sa_user_login_load_account:
            assert SMAssignments.wf_create_new_subscription_assign_to_device(device_type, brnf_sa_new_brim_subs_switch,
                                                                             brnf_sa_user_login_load_account)

    @pytest.mark.order(4)
    @pytest.mark.testrail(id=1220605)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_subs_gateway_new_subscription_key_c1220605(self, brnf_sa_new_brim_subs_gw_70xx,
                                                           brnf_sa_user_login_load_account,
                                                           device_type="GATEWAY"):
        """
          ===== Assign eval license to IAP ======
          1. Using the login session
          2. Manually unassign app
          3. Manually assign app
          4. Assign license to IAP
          3. Verify the license is assigned correctly
          """
        if brnf_sa_user_login_load_account:
            assert SMAssignments.wf_create_new_subscription_assign_to_device(device_type, brnf_sa_new_brim_subs_gw_70xx,
                                                                             brnf_sa_user_login_load_account)

    @pytest.mark.order(5)
    @pytest.mark.testrail(id=1220612)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_subs_iap_update_subs_qty_c1220612(self, brnf_sa_new_brim_subs_iap, brnf_sa_user_login_load_account):
        """
          ===== Assign eval license to IAP ======
          1. Update the quantity of licence keys
          """
        qty = "50.00"
        if brnf_sa_user_login_load_account:
            lic_key, lic_quote = brnf_sa_new_brim_subs_iap
            log.info("lic_key, {}, lic_quote: {}".format(lic_key, lic_quote))
            assert SMAssignments.wf_update_qty_existing_subs_iap(quote=lic_quote, qty=qty)

    @pytest.mark.order(6)
    @pytest.mark.testrail(id=1220615)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_subs_tier_upgrade_subs_iap_c1220615(self, brnf_sa_new_brim_subs_iap, brnf_sa_user_login_load_account):
        """
          ===== Assign eval license to IAP ======
          1. Upgrade the subscription tier of licence
          """
        if brnf_sa_user_login_load_account:
            lic_key, lic_quote = brnf_sa_new_brim_subs_iap
            log.info("lic_key, {}, lic_quote: {}".format(lic_key, lic_quote))
            assert SMAssignments.wf_upgrade_subs_tier_existing_subs_iap(upgrade_quote=lic_quote)

    @pytest.mark.order(7)
    @pytest.mark.testrail(id=1220611)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url,
                        reason="Not supported on triton-lite.")
    def test_sm_subs_tier_downgrade_subs_iap_c1220611(self, brnf_sa_new_brim_subs_iap, brnf_sa_user_login_load_account):
        """
          ===== Assign eval license to IAP ======
          1. Downgrade the subscription tier of licence
          """
        if brnf_sa_user_login_load_account:
            lic_key, lic_quote = brnf_sa_new_brim_subs_iap
            log.info("lic_key, {}, lic_quote: {}".format(lic_key, lic_quote))
            assert SMAssignments.wf_downgrade_subs_tier_existing_subs_iap(downgrade_quote=lic_quote)

    @pytest.mark.order(8)
    @pytest.mark.testrail(id=1220613)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_subs_iap_update_orig_qty_c1220613(self, brnf_sa_new_brim_subs_iap, brnf_sa_user_login_load_account):
        """
          1. Update the quantity of licence keys to original value
          """
        qty = "100.00"
        if brnf_sa_user_login_load_account:
            lic_key, lic_quote = brnf_sa_new_brim_subs_iap
            log.info("lic_key, {}, lic_quote: {}".format(lic_key, lic_quote))
            assert SMAssignments.wf_update_qty_existing_subs_iap(quote=lic_quote, qty=qty)

    @pytest.mark.order(9)
    @pytest.mark.testrail(id=1220620)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_subs_iap_update_to_expired_c1220620(self, brnf_sa_new_brim_subs_iap,
                                                    brnf_sa_user_login_load_account, sm_app_api_session):
        """
          1. Update the licence key to expired
          """
        if brnf_sa_user_login_load_account:
            lic_key, lic_quote = brnf_sa_new_brim_subs_iap
            log.info("lic_key, {}, lic_quote: {}".format(lic_key, lic_quote))
            assert SMAssignments.wf_existing_subs_to_expire(quote=lic_quote, sm_app_api=sm_app_api_session)

    @pytest.mark.order(10)
    @pytest.mark.testrail(id=1220616)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_subs_iap_update_expired_to_extended_c1220616(self, brnf_sa_new_brim_subs_iap,
                                                             brnf_sa_user_login_load_account,
                                                             sm_app_api_session):
        """
          1. Extend the licence key
          """
        serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_serial_subs_mgmt']
        pcid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_pcid']
        acid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_acid']

        if brnf_sa_user_login_load_account:
            lic_key, lic_quote = brnf_sa_new_brim_subs_iap
            log.info("lic_key, {}, lic_quote: {}".format(lic_key, lic_quote))
            # extend the expired license by 1 year
            extend_sec = 60 * 60 * 24 * 365

            # extend subscription
            assert SMAssignments.wf_extend_existing_subs_key(extend_quote=lic_quote, extend_by_sec=extend_sec)
            log.info("\nSubscription key extension succeeded\n")

            # assign the subscription to device
            assert SMAssignments.wf_unassign_subs_key_to_device(pcid=pcid, acid=acid,
                                                                serial=serial, sm_app_api=sm_app_api_session)
            log.info("\nCurrent subscription key unassiged from IAP device\n")

            assert SMAssignments.wf_assign_subs_key_to_device(pcid=pcid, acid=acid, serial=serial, subs_key=lic_key,
                                                              sm_app_api=sm_app_api_session)
            log.info("\nCurrent subscription key assiged from IAP device\n")

    @pytest.mark.order(11)
    @pytest.mark.testrail(id=1220617)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_subs_iap_terminate_c1220617(self, brnf_sa_new_brim_subs_iap,
                                            brnf_sa_user_login_load_account, sm_app_api_session):
        """
          1. Terminate the licence
          """
        if brnf_sa_user_login_load_account:
            lic_key, lic_quote = brnf_sa_new_brim_subs_iap
            log.info("lic_key, {}, lic_quote: {}".format(lic_key, lic_quote))
            assert SMAssignments.wf_existing_subs_to_terminate(quote=lic_quote, sm_app_api=sm_app_api_session)

    @pytest.mark.order(12)
    @pytest.mark.testrail(id=1220616)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_subs_iap_update_terminated_to_extended_c1220616(self, brnf_sa_new_brim_subs_iap,
                                                                brnf_sa_user_login_load_account,
                                                                sm_app_api_session):
        """
          1. Update the quantity of licence keys to original value
          """
        serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_serial_subs_mgmt']
        pcid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_pcid']
        acid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_acid']

        if brnf_sa_user_login_load_account:
            lic_key, lic_quote = brnf_sa_new_brim_subs_iap
            log.info("lic_key, {}, lic_quote: {}".format(lic_key, lic_quote))
            # extend the expired license by 1 year
            extend_sec = 60 * 60 * 24 * 365

            # extend subscription
            assert SMAssignments.wf_extend_existing_subs_key(extend_quote=lic_quote, extend_by_sec=extend_sec)
            log.info("\nSubscription key extension succeeded\n")

            # assign the subscription to device
            assert SMAssignments.wf_unassign_subs_key_to_device(pcid=pcid, acid=acid,
                                                                serial=serial, sm_app_api=sm_app_api_session)
            log.info("\nCurrent subscription key unassiged from IAP device\n")

            assert SMAssignments.wf_assign_subs_key_to_device(pcid=pcid, acid=acid, serial=serial, subs_key=lic_key,
                                                              sm_app_api=sm_app_api_session)
            log.info("\nCurrent subscription key assiged from IAP device\n")

    @pytest.mark.order(13)
    @pytest.mark.testrail(id=1220621)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_cancel_subscription_iap_c1220621(self, brnf_sa_new_brim_subs_iap, brnf_sa_user_login_load_account):
        """
          Update licence keys - Cancel
          """
        if brnf_sa_user_login_load_account:
            lic_key, lic_quote = brnf_sa_new_brim_subs_iap
            log.info("lic_key, {}, lic_quote: {}".format(lic_key, lic_quote))
            assert SMAssignments.wf_existing_subs_to_cancel(quote=lic_quote)

    @pytest.mark.order(14)
    @pytest.mark.testrail(id=1337757)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_new_aruba_skus_iap_C1337757(self, brnf_sa_user_login_load_account, sm_app_api_session,
                                            device_type="IAP"):
        """
          1. Update the quantity of licence keys to original value
          """
        if brnf_sa_user_login_load_account:
            assert SMAssignments.wf_unassign_assign_new_aruba_skus_iap(sm_app_api=sm_app_api_session,
                                                                       device_type=device_type)

    @pytest.mark.order(15)
    @pytest.mark.testrail(id=1220606)
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_combined_sub_ap_sw_gw_C1220606(self, brnf_sa_new_brim_combined_subs_ap_sw_gw,
                                               brnf_sa_user_login_load_account,
                                               sm_app_api_session):
        """
          1. Update the quantity of licence keys to original value
          """
        ap_serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_serial_subs_mgmt']
        sw_serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_sw_serial_subs_mgmt']
        gw_serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_gw_serial_subs_mgmt']
        pcid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_pcid']
        acid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_acid']

        if brnf_sa_user_login_load_account:
            assert SMAssignments.wf_create_new_combined_subscription_ap_sw_gw(brnf_sa_new_brim_combined_subs_ap_sw_gw,
                                                                              brnf_sa_user_login_load_account)

            ap_key, sw_key, gw_key, lic_quote = brnf_sa_new_brim_combined_subs_ap_sw_gw
            log.info("ap_key, {}, sw_key, {}, gw_key, {}, lic_quote: {}".format(ap_key, sw_key, gw_key, lic_quote))

            # assign the subscription to IAP device
            assert SMAssignments.wf_unassign_subs_key_to_device(pcid=pcid, acid=acid,
                                                                serial=ap_serial, sm_app_api=sm_app_api_session)
            log.info("\nCurrent subscription key unassigned from IAP device\n")
            assert SMAssignments.wf_assign_subs_key_to_device(pcid=pcid, acid=acid, serial=ap_serial, subs_key=ap_key,
                                                              sm_app_api=sm_app_api_session)
            log.info("\nCurrent subscription key assigned from IAP device\n")

            # assign the subscription to SW device
            assert SMAssignments.wf_unassign_subs_key_to_device(pcid=pcid, acid=acid,
                                                                serial=sw_serial, sm_app_api=sm_app_api_session)
            log.info("\nCurrent subscription key unassigned from Switch device\n")
            assert SMAssignments.wf_assign_subs_key_to_device(pcid=pcid, acid=acid, serial=sw_serial, subs_key=sw_key,
                                                              sm_app_api=sm_app_api_session)
            log.info("\nCurrent subscription key assigned from Switch device\n")

            # assign the subscription to GW device
            assert SMAssignments.wf_unassign_subs_key_to_device(pcid=pcid, acid=acid,
                                                                serial=gw_serial, sm_app_api=sm_app_api_session)
            log.info("\nCurrent subscription key unassigned from GW device\n")
            assert SMAssignments.wf_assign_subs_key_to_device(pcid=pcid, acid=acid, serial=gw_serial, subs_key=gw_key,
                                                              sm_app_api=sm_app_api_session)
            log.info("\nCurrent subscription key assigned from GW device\n")

    @pytest.mark.order(16)
    @pytest.mark.testrail(id=1220612)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_combined_subs_update_subs_qty_c1220612(self, brnf_sa_new_brim_combined_subs_ap_sw_gw,
                                                       brnf_sa_user_login_load_account):
        """
          ===== Assign eval license to IAP ======
          1. Update the quantity of licence keys
          """
        qty = "10.00"
        if brnf_sa_user_login_load_account:
            ap_key, sw_key, gw_key, lic_quote = brnf_sa_new_brim_combined_subs_ap_sw_gw
            log.info("lic_keys, {}, {}, {}, lic_quote: {}".format(ap_key, sw_key, gw_key, lic_quote))
            assert SMAssignments.wf_update_qty_existing_subs_iap(quote=lic_quote, qty=qty)

    @pytest.mark.order(17)
    @pytest.mark.testrail(id=1220613)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_combined_subs_update_orig_qty_c1220613(self, brnf_sa_new_brim_combined_subs_ap_sw_gw,
                                                       brnf_sa_user_login_load_account):
        """
          1. Update the quantity of licence keys to original value
          """
        qty = "2.00"
        if brnf_sa_user_login_load_account:
            ap_key, sw_key, gw_key, lic_quote = brnf_sa_new_brim_combined_subs_ap_sw_gw
            log.info("lic_keys, {}, {}, {}, lic_quote: {}".format(ap_key, sw_key, gw_key, lic_quote))
            assert SMAssignments.wf_update_qty_existing_subs_iap(quote=lic_quote, qty=qty)

    @pytest.mark.order(18)
    @pytest.mark.testrail(id=1220610)
    @pytest.mark.Regression
    @pytest.mark.xfail
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_subs_vgw_new_subscription_key_c1220610(self, brnf_sa_new_brim_subs_vgw,
                                                       brnf_sa_user_login_load_account, sm_app_api_session,
                                                       adi_app_api_session, device_type="GATEWAY"):
        """
          ===== Assign eval license to IAP ======
          1. Using the login session
          2. Manually unassign app
          3. Manually assign app
          4. Assign license to VGW
          3. Verify the license is assigned correctly
          """
        if brnf_sa_user_login_load_account:
            assert SMAssignments.wf_create_new_vgw_subscription_assign_to_device(device_type, brnf_sa_new_brim_subs_vgw,
                                                                                 brnf_sa_user_login_load_account,
                                                                                 sm_app_api=sm_app_api_session,
                                                                                 app_adi=adi_app_api_session)

    @pytest.mark.order(19)
    @pytest.mark.Regression
    def test_brnf_msp_login_load_account(self, brnf_sa_msp_login_load_account):
        """
        ===== User login to the account using user API for other tests to run user api ======
        1. User login to the account using new user and password
        2. User load the pcid account for other tests to run user api for other subsequent test cases
        """
        assert brnf_sa_msp_login_load_account

    @pytest.mark.order(20)
    @pytest.mark.testrail(id=1220673)
    @pytest.mark.testrail(id=1220670)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_msp_iap_eval_subs_C1220670_C1220673(self,
                                                    brnf_sa_msp_login_load_account, sm_app_api_session,
                                                    adi_app_api_session, device_type="IAP"):
        """
          ===== Assign eval license to IAP ======
          1. Using the login session
          2. Manually unassign app
          3. Manually device to tenant 1 and assign app
          4. Assign license to device
          3. Verify the license is assigned correctly
          """
        if brnf_sa_msp_login_load_account:
            tenant_acid = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"][
                "tenant1_acid_network"]
            assert SMAssignments.wf_msp_unassign_and_assign_appl_subs_assign_to_device(device_type,
                                                                                       tenant_acid=tenant_acid,
                                                                                       sm_app_api=sm_app_api_session,
                                                                                       app_adi=adi_app_api_session)

    @pytest.mark.order(21)
    @pytest.mark.testrail(id=1220673)
    @pytest.mark.testrail(id=1220670)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_msp_switch_eval_subs_C1220670_C1220673(self,
                                                       brnf_sa_msp_login_load_account, sm_app_api_session,
                                                       adi_app_api_session, device_type="SWITCH"):
        """
          ===== Assign eval license to SWITCH ======
          1. Using the login session
          2. Manually unassign app
          3. Manually device to tenant 1 and assign app
          4. Assign license to device
          3. Verify the license is assigned correctly
          """
        if brnf_sa_msp_login_load_account:
            tenant_acid = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"][
                "tenant2_acid_network"]
            assert SMAssignments.wf_msp_unassign_and_assign_appl_subs_assign_to_device(device_type,
                                                                                       tenant_acid=tenant_acid,
                                                                                       sm_app_api=sm_app_api_session,
                                                                                       app_adi=adi_app_api_session)

    @pytest.mark.order(22)
    @pytest.mark.testrail(id=1220673)
    @pytest.mark.testrail(id=1220670)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_sm_msp_gateway_eval_subs_C1220670_C1220673(self,
                                                        brnf_sa_msp_login_load_account, sm_app_api_session,
                                                        adi_app_api_session, device_type="GATEWAY"):
        """
          ===== Assign eval license to GATEWAY ======
          1. Using the login session
          2. Manually unassign app
          3. Manually device to tenant 1 and assign app
          4. Assign license to device
          3. Verify the license is assigned correctly
          """
        if brnf_sa_msp_login_load_account:
            tenant_acid = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"][
                "tenant3_acid_network"]
            assert SMAssignments.wf_msp_unassign_and_assign_appl_subs_assign_to_device(device_type,
                                                                                       tenant_acid=tenant_acid,
                                                                                       sm_app_api=sm_app_api_session,
                                                                                       app_adi=adi_app_api_session)
