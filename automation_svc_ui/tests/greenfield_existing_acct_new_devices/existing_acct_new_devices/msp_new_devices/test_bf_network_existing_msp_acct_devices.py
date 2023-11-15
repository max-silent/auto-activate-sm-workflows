import logging
import os

import allure
import pytest

from automation_svc_ui.conftest import get_add_device_expected_responses, ExistingUserAcctDevices
from automation_svc_ui.tests.greenfield_existing_acct_new_devices.existing_acct_new_devices \
    .brnf_network_existing_acct_new_devices import WfExistingAcctNewDevices

log = logging.getLogger(__name__)
expected_response_data = get_add_device_expected_responses()

create_test = WfExistingAcctNewDevices()


@pytest.mark.skipif("pavo" in ExistingUserAcctDevices.login_page_url,
                    reason="MSP-user with service-centric UI needed.")
@pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url,
                    reason="TAC-user needed. MSP-user with service-centric UI needed.")
@allure.parent_suite("activate-sm-workflows")
@allure.suite("Greenfield network devices - service_centric_ui")
@allure.sub_suite("Greenfield existing msp account new network devices")
class TestExistingMspAccountNewDevicesSvc:
    @pytest.mark.testrail(id=1220580)
    @pytest.mark.order(1)
    @pytest.mark.Regression
    def test_brnf_msp_order_iap_devices_c1220580(self, brnf_msp_sa_order_iap_devices):
        """
        ===== Create IAP device on Activate order process ======
        1. Run AOP API manufacturing API to create IAP network device.
        """
        assert brnf_msp_sa_order_iap_devices

    @pytest.mark.order(2)
    @pytest.mark.Regression
    def test_brnf_msp_order_switch_devices(self, brnf_msp_sa_order_switch_devices):
        """
        ===== Create SWITCH device on Activate order process ======
        1. Run AOP API manufacturing API to create SWITCH network device.
        """
        assert brnf_msp_sa_order_switch_devices

    @pytest.mark.order(3)
    @pytest.mark.Regression
    def test_brnf_msp_order_cntrl_devices(self, brnf_msp_sa_order_cntrl_devices):
        """
        ===== Create CONTROLLER device on Activate order process ======
        1. Run AOP API manufacturing API to create CONTROLLER network device.
        """
        assert brnf_msp_sa_order_cntrl_devices

    @pytest.mark.testrail(id=1220629)
    @pytest.mark.order(4)
    @pytest.mark.Regression
    def test_create_alias_msp_acct_c1220629(self,
                                            tac_user_login_load_account,
                                            brnf_msp_user_login_load_account,
                                            end_username_msp_alias):
        """
        ===== Added alias to MSP account ======
        1. Using the login session, add alias and verify it's successful.
        """
        log.info("Running test_create_alias_msp_acct_c1220629")
        assert create_test.wf_create_activate_verified_alias(tac_user_login_load_account,
                                                             end_username_msp_alias,
                                                             brnf_msp_user_login_load_account)

    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.order(5)
    @pytest.mark.testrail(id=1313772)
    @pytest.mark.Regression
    def test_iap_dev_prov_msp_fail_prov_no_rule_c1313772(self, brnf_sa_iap_prov_msp):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail-prov-no-rule'
        """
        response = brnf_sa_iap_prov_msp
        assert response.status_code == expected_response_data["iap_provision_no_rule"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["iap_provision_no_rule"]["X-Status-Code"]
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()

    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.Regression
    @pytest.mark.parametrize('api_path, x_type', [
        pytest.param("hpe-provision", "provision-update", marks=[pytest.mark.C1313773, pytest.mark.order(6)],
                     id='ftpm_provision_C1313773'),
        pytest.param("hpe-provision-rtpm", "provision-update", marks=[pytest.mark.C1342982, pytest.mark.order(7)],
                     id='rtpm_provision_C1342982'),
        pytest.param("cx-provision", "provision-update", marks=[pytest.mark.C1313775, pytest.mark.order(8)],
                     id='cx-provision_C1313775')])
    def test_sw_dev_prov_msp_no_rule(self, brnf_sa_sw_prov_msp, api_path, x_type):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail-prov-no-rule'
        """
        response = brnf_sa_sw_prov_msp
        assert response.status_code == expected_response_data['switch_provision_no_rule']['response_code']
        assert response.headers["X-Status-Code"] == expected_response_data['switch_provision_no_rule'][
            'X-Status-Code']
        assert response.headers["X-Activation-Key"] is not None
        assert len(response.headers["X-Activation-Key"]) == 8

    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1313774)
    @pytest.mark.order(9)
    def test_cntrl_dev_prov_no_rule(self, brnf_sa_cntrl_prov_msp):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail-prov-no_rule  '
        """
        response = brnf_sa_cntrl_prov_msp
        assert response.status_code == expected_response_data["controller_provision_no_rule"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["controller_provision_no_rule"][
            "X-Status-Code"]
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()

    @pytest.mark.testrail(id=1220629)
    @pytest.mark.order(10)
    @pytest.mark.Regression
    def test_check_device_at_msp_acct_c1220629(self,
                                               browser_instance,
                                               msp_logged_in_storage_state,
                                               brnf_msp_sa_order_iap_devices,
                                               brnf_msp_sa_order_switch_devices,
                                               brnf_msp_sa_order_cntrl_devices
                                               ):
        """
        ===== Auto-claimed device at MSP account ======
        1. Using the login session, verify devices are present at MSP account.
        2. Assign devices to tenant and check it's successful.
        3. Archive devices via UI.
        """

        log.info("Running test_check_device_at_msp_acct_c1220629")
        assert create_test.wf_check_device_at_msp_info(browser_instance,
                                                       msp_logged_in_storage_state,
                                                       [brnf_msp_sa_order_iap_devices, brnf_msp_sa_order_switch_devices]
                                                       )

    @pytest.mark.testrail(id=1220659)
    @pytest.mark.order(11)
    @pytest.mark.Regression
    def test_assign_archived_device_msp_c1220659(self,
                                                 browser_instance,
                                                 msp_logged_in_storage_state,
                                                 brnf_msp_sa_order_iap_devices
                                                 ):
        """
        ===== Assigning archived devices to tenant ======
        1. Using the login session, try to assign archived devices to tenant. Verify it's not possible.
        """

        log.info("Running test_assign_archived_device_msp_c1220659")
        assert create_test.wf_assign_archived_device_at_msp(browser_instance,
                                                            msp_logged_in_storage_state,
                                                            [brnf_msp_sa_order_iap_devices])

    @pytest.mark.testrail(id=1220660)
    @pytest.mark.order(12)
    @pytest.mark.Regression
    def test_assign_unarchived_device_msp_c1220660(self,
                                                   browser_instance,
                                                   msp_logged_in_storage_state,
                                                   brnf_msp_sa_order_iap_devices,
                                                   brnf_msp_sa_order_switch_devices,
                                                   brnf_msp_sa_order_cntrl_devices
                                                   ):
        """
        ===== Assigning unarchived devices to tenant ======
        1. Using the login session, unarchive device.
        2. Assign unarchived device to tenant and check it's successful.
        """

        log.info("Running test_assign_unarchived_device_msp_c1220660")
        assert create_test.wf_assign_unarchived_device_at_msp(browser_instance,
                                                              msp_logged_in_storage_state,
                                                              [brnf_msp_sa_order_iap_devices,
                                                               brnf_msp_sa_order_switch_devices])

    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.Regression
    @pytest.mark.parametrize("endpoint, x_type, fw_version", [
        pytest.param("/firmware", "firmware-check", "8.4.0.0-8.4.0.0_70043",
                     marks=[pytest.mark.C1313788, pytest.mark.order(13)], id="firmware-check_C1313788"),
        pytest.param("/firmware", "firmware-baseversion-iap", "8.5.0.5-8.5.0.5_73491",
                     marks=[pytest.mark.C1313790, pytest.mark.order(14)], id="firmware-baseversion-iap_C1313790"),
        pytest.param("/firmware", "firmware-baseversion-gateway", "8.5.0.5-8.5.0.5_73491",
                     marks=[pytest.mark.C1313791, pytest.mark.order(15)],
                     id="firmware-baseversion-gateway_C1313791"),
        pytest.param("/firmware", "firmware-upgrade", "8.4.0.0-8.4.0.0_70043",
                     marks=[pytest.mark.C1313789, pytest.mark.order(16)], id="firmware-upgrade_C1313789")])
    def test_iap_dev_msp_firmware(self, brnf_msp_sa_order_iap_devices, endpoint, x_type, fw_version):
        """
        ===== Using device firmware Api call to verify devices can get the firmware URL======
            :param endpoint: firmware endpoint for IAP device
            :param x_type: firmware request for firmware checks, upgrade, base firmware version for IAP device
            :param fw_version: firmware version for IAP device
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device firmware call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = create_test.brnf_sa_nw_device_firmware(
            brnf_msp_sa_order_iap_devices, "IAP", endpoint, x_type, fw_version
        )
        assert response.status_code == expected_response_data["iap_fw_prov_positive"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["iap_fw_prov_positive"][
            "X-Status-Code"]
        assert response.headers.get('X-alternative-image-server-list') is not None
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()
        assert response.headers["X-Mode"] == expected_response_data["iap_fw_prov_positive"]["X-Mode"]
        assert "http://" in response.text

    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.Regression
    @pytest.mark.order(17)
    @pytest.mark.testrail(id=1220687)
    def test_iap_dev_prov_msp_c1220687(self, brnf_sa_iap_prov_msp):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_iap_prov_msp
        assert response.status_code == expected_response_data["iap_fw_prov_positive"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["iap_fw_prov_positive"]["X-Status-Code"]
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()
        assert response.headers["X-Athena-Url"] is not None
        assert response.headers["X-Mode"] == expected_response_data["iap_fw_prov_positive"]["X-Mode"]

    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.Regression
    @pytest.mark.parametrize('api_path, x_type', [
        pytest.param("hpe-provision", "provision-update", marks=[pytest.mark.C1220688, pytest.mark.order(18)],
                     id='ftpm_provision_C1220688'),
        pytest.param("hpe-provision-rtpm", "provision-update", marks=[pytest.mark.C1342983, pytest.mark.order(19)],
                     id='rtpm_provision_C1342983'),
        pytest.param("cx-provision", "provision-update", marks=[pytest.mark.C1220690, pytest.mark.order(20)],
                     id='cx-provision_C1220690')])
    def test_sw_dev_prov_msp_success(self, brnf_sa_sw_prov_msp, api_path, x_type):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_sw_prov_msp
        assert response.status_code == expected_response_data['switch_provision_success']['response_code']
        assert response.headers["X-Status-Code"] == expected_response_data['switch_provision_success'][
            'X-Status-Code']
        assert response.headers["X-Activation-Key"] is not None
        assert len(response.headers["X-Activation-Key"]) == 8
        if api_path != "cx-provision":
            assert response.headers["X-Athena-Url"] is not None

    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.Regression
    @pytest.mark.parametrize('api_path, x_type', [
        pytest.param("hpe-firmware", "firmware-check", marks=[pytest.mark.C1313792, pytest.mark.order(21)],
                     id='ftpm_firmware_check_C1313792'),
        pytest.param("hpe-firmware-rtpm", "firmware-check", marks=[pytest.mark.C1314054, pytest.mark.order(22)],
                     id='rtpm_firmware_check_C1314054')])
    def test_sw_dev_msp_firmware(self, brnf_sa_sw_prov_msp, api_path, x_type):
        """
        ===== Using firmware Api call to verify devices can get the firmware URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device firmware call
        3. verify the call has 'X-Status-Code': 'success' +  firmware urls in the response
        """
        response = brnf_sa_sw_prov_msp
        assert response.status_code == expected_response_data['switch_firmware_response']['response_code']
        assert response.headers["X-Status-Code"] == expected_response_data['switch_firmware_response'][
            'X-Status-Code']
        assert response.headers["X-Activation-Key"] is not None
        assert len(response.headers["X-Activation-Key"]) == 8
        assert "http://" in response.text

    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220689)
    @pytest.mark.order(23)
    @pytest.mark.xfail(reason="GLCP-128478")
    def test_cntrl_dev_prov_C1220689(self, brnf_sa_cntrl_prov_msp):
        """
        ===== Using device provisioning Api call to verify devices can get the provisioning URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_sa_cntrl_prov_msp
        assert response.status_code == expected_response_data["controller_provision_success"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["controller_provision_success"][
            "X-Status-Code"]
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()

    @pytest.mark.Regression
    @pytest.mark.skipif(not os.getenv("KUBERNETES_SERVICE_HOST"), reason="it will run only inside container")
    @pytest.mark.parametrize("endpoint, x_type, fw_version", [
        pytest.param("/firmware", "firmware-baseversion-iap", "8.5.0.5-8.5.0.5_73491",
                     marks=[pytest.mark.C1313794, pytest.mark.order(24)], id="firmware-baseversion-iap_C1313794"),
        pytest.param("/firmware", "firmware-baseversion-gateway", "8.5.0.5-8.5.0.5_73491",
                     marks=[pytest.mark.C1313795, pytest.mark.order(25)],
                     id="firmware-baseversion-gateway_C1313795")])
    def test_cntrl_dev_msp_firmware(self, brnf_msp_sa_order_cntrl_devices, endpoint, x_type, fw_version):
        """
        ===== Using device firmware Api call to verify devices can get the firmware URL======
            :param endpoint: firmware endpoint for IAP device
            :param x_type: firmware request for firmware checks, upgrade, base firmware version for IAP device
            :param fw_version: firmware version for IAP device
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device firmware call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = create_test.brnf_sa_nw_device_firmware(
            brnf_msp_sa_order_cntrl_devices, "CONTROLLER", endpoint, x_type, fw_version
        )
        assert response.status_code == expected_response_data["controller_firmware_response"]["response_code"]
        assert response.headers.get('X-Status-Code') == expected_response_data["controller_firmware_response"][
            "X-Status-Code"]
        assert response.headers.get('X-alternative-image-server-list') is not None
        assert response.headers.get('X-Session-Id') is not None
        assert len(response.headers.get('X-Activation-Key')) == 8
        assert response.headers.get('X-Activation-Key').isupper()
        assert "http://" in response.text

    @pytest.mark.testrail(id=1220647)
    @pytest.mark.order(26)
    @pytest.mark.Regression
    def test_add_tag_to_device_msp_c1220647(self,
                                            browser_instance,
                                            msp_logged_in_storage_state,
                                            brnf_msp_sa_order_iap_devices
                                            ):
        """
        ===== Adding tag to unarchived devices ======
        1. Using the login session, add tag to unarchived device and check it's successful.
        """

        log.info("Running test_add_tag_to_device_msp_c1220647")
        assert create_test.wf_add_tag_to_device_at_msp(browser_instance,
                                                       msp_logged_in_storage_state,
                                                       [brnf_msp_sa_order_iap_devices])

    @pytest.mark.testrail(id=1220658)
    @pytest.mark.order(27)
    @pytest.mark.Regression
    def test_archive_device_api_msp_c1220658(self, brnf_msp_user_login_load_account, brnf_msp_sa_order_iap_devices):
        """
        ===== Archiving auto-claimed device via API ======
        1. Using API, archive device and check it's successful.
        """

        log.info("Running test_archive_device_api_msp_c1220658")
        device_archiving_result = create_test \
            .wf_archive_device_api_at_msp(brnf_msp_user_login_load_account, [brnf_msp_sa_order_iap_devices])[0]
        assert device_archiving_result, "Device archiving failed."
        devices_count = len(device_archiving_result)
        assert devices_count == 1, f"Unexpected count of filtered devices: '{devices_count}'."
        assert device_archiving_result[0].get("archived") is True, "Device is not marked as archived."
        assert device_archiving_result[0].get("account_name") == "", "Device account_name unexpectedly assigned."

    @pytest.mark.testrail(id=1220644)
    @pytest.mark.order(28)
    @pytest.mark.Regression
    def test_check_manual_claim_device_at_msp_acct_c1220644(self,
                                                            browser_instance,
                                                            msp_logged_in_storage_state,
                                                            brnf_msp_user_login_load_account,
                                                            brnf_sa_order_iap_devices,
                                                            brnf_sa_order_sw_devices,
                                                            brnf_sa_order_gw_devices
                                                            ):
        """
        ===== Manually claimed devices at MSP account ======
        1. Using the login session, manually claim ordered device at MSP account.
        2. Assign devices to tenant and check it's successful.
        3. Assign subscription to device and check it's successful.
        4. Check that events related to device claim, assign and subscription are present in Audit Logs.
        """

        log.info("Running test_check_manual_claim_device_at_msp_acct_c1220644")
        devices_details = [brnf_sa_order_iap_devices, brnf_sa_order_sw_devices, brnf_sa_order_gw_devices]
        assert all(devices_details), f"Ordering of some devices failed. Devices ordering result: '{devices_details}'."
        assert create_test.wf_check_manual_claimed_device_at_msp_info(browser_instance,
                                                                      msp_logged_in_storage_state,
                                                                      brnf_msp_user_login_load_account,
                                                                      devices_details)

    @pytest.mark.testrail(id=1220645)
    @pytest.mark.order(29)
    @pytest.mark.Regression
    def test_reassign_device_to_other_tenant_msp_c1220645(self,
                                                          browser_instance,
                                                          msp_logged_in_storage_state,
                                                          brnf_msp_user_login_load_account,
                                                          msp_iap_subscription,
                                                          brnf_sa_order_iap_devices):
        """
        ===== Unassigning device from tenant 1 and assigning it to tenant 2 ======
        1. Using the login session, remove assignment of device from tenant 1.
        2. Assign device to tenant 2 and check it's successful.
        3. Apply subscription.
        4. Check audit logs for unassign, assign and subscription log events.
        """

        log.info("Running test_reassign_device_to_other_tenant_msp_c1220645")
        assert msp_iap_subscription, "Available AP Advanced subscriptions were not found."
        assert create_test.wf_reassign_device_to_other_tenant_msp(browser_instance,
                                                                  msp_logged_in_storage_state,
                                                                  brnf_msp_user_login_load_account,
                                                                  msp_iap_subscription,
                                                                  [brnf_sa_order_iap_devices])
