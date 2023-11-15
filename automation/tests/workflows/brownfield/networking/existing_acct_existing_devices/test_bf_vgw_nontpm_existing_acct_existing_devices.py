import json
import logging

import allure
import pytest

from automation.conftest import get_add_device_expected_responses

log = logging.getLogger(__name__)
expected_response_data = get_add_device_expected_responses()


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield_network_devices")
@allure.sub_suite("Brownfield_existing_account_existing_network_devices")
@pytest.mark.Plv
class TestExistingAccountExistingDevicesEst:

    @pytest.mark.testrail(id=1343739)
    @pytest.mark.order(1)
    @pytest.mark.Regression
    def test_brnf_sa_vgw_est_provision(self, brnf_sa_vgw_est_prov):
        """
        ===== Test case to make /estprovision call ======
        1.Make a POST call to /estprovision with X-Identity in the header
        Expected: Returns certificate and gets EST server url
        """
        res = json.loads(brnf_sa_vgw_est_prov.text)
        assert brnf_sa_vgw_est_prov.status_code == expected_response_data["est_provision_success"]["response_code"]
        assert res.get('cert') is not None
        assert res.get('estUrl') is not None
        assert brnf_sa_vgw_est_prov.headers.get('X-Status-Code') == expected_response_data["est_provision_success"]["X-Status-Code"]
        assert brnf_sa_vgw_est_prov.headers.get('X-Authenticated') == expected_response_data["est_provision_success"][
            "X-Authenticated"]

    @pytest.mark.testrail(id=1220682)
    @pytest.mark.Regression
    @pytest.mark.order(2)
    def test_brnf_sa_vgw_verify_est_provision(self, brnf_sa_vgw_verify_est):
        """
        ===== Test case to make /verifyestchallenge call =====
        1.Make a POST call to /verifyestchallenge with serial_number as a query parameter
        Expected: Should return X-Authenticated: authenticated in the header
        """
        res = json.loads(brnf_sa_vgw_verify_est.text)
        assert brnf_sa_vgw_verify_est.status_code == expected_response_data["est_provision_success"]["response_code"]
        assert brnf_sa_vgw_verify_est.headers.get('X-Status-Code') == expected_response_data["est_provision_success"]["X-Status-Code"]
        assert brnf_sa_vgw_verify_est.headers.get('X-Authenticated') == expected_response_data["est_provision_success"][
            "X-Authenticated"]
        assert res.get("success") == expected_response_data["est_provision_success"]["success"]

    @pytest.mark.testrail(id=1343739)
    @pytest.mark.order(3)
    @pytest.mark.Regression
    def test_brnf_sa_nontpm_est_provision(self, brnf_sa_nontpm_est_prov):
        """
        ===== Test case to make /estprovision call ======
        1.Make a POST call to /estprovision with X-Identity in the header
        Expected: Returns certificate and gets EST server url
        """
        res = json.loads(brnf_sa_nontpm_est_prov.text)
        assert brnf_sa_nontpm_est_prov.status_code == expected_response_data["est_provision_success"]["response_code"]
        assert res.get('cert') is not None
        assert res.get('estUrl') is not None
        assert brnf_sa_nontpm_est_prov.headers.get('X-Status-Code') == expected_response_data["est_provision_success"]["X-Status-Code"]
        assert brnf_sa_nontpm_est_prov.headers.get('X-Authenticated') == expected_response_data["est_provision_success"][
            "X-Authenticated"]

    @pytest.mark.testrail(id=1343741)
    @pytest.mark.Regression
    @pytest.mark.order(4)
    def test_brnf_sa_nontpm_verify_est_provision(self, brnf_sa_nontpm_verify_est):
        """
        ===== Test case to make /verifyestchallenge call =====
        1.Make a POST call to /verifyestchallenge with serial_number as a query parameter
        Expected: Should return X-Authenticated: authenticated in the header
        """
        res = json.loads(brnf_sa_nontpm_verify_est.text)
        assert brnf_sa_nontpm_verify_est.status_code == expected_response_data["est_provision_success"]["response_code"]
        assert brnf_sa_nontpm_verify_est.headers.get('X-Status-Code') == expected_response_data["est_provision_success"]["X-Status-Code"]
        assert brnf_sa_nontpm_verify_est.headers.get('X-Authenticated') == expected_response_data["est_provision_success"][
            "X-Authenticated"]
        assert res.get("success") == expected_response_data["est_provision_success"]["success"]

    @pytest.mark.testrail(id=1220679)
    @pytest.mark.Regression
    @pytest.mark.order(5)
    def test_brnf_sa_nontpm_device_provision_success(self, brnf_sa_nontpm_prov):
        """ Test case for nontpm device provision call on /hpe-nontpm
        Steps: POST request to /hpe-nontpm
        Expected result: if device assigned to application should return x-status-code as success else fail-prov-no-rule in response header
        """
        assert brnf_sa_nontpm_prov.status_code == expected_response_data["switch_provision_success"]["response_code"]
        assert brnf_sa_nontpm_prov.headers['X-Status-Code'] in (expected_response_data["switch_provision_success"]["X-Status-Code"],
                                                                expected_response_data["switch_provision_no_rule"]["X-Status-Code"])
        assert brnf_sa_nontpm_prov.headers['X-Activation-Key'] is not None
        assert len(brnf_sa_nontpm_prov.headers["X-Activation-Key"]) == 8

    @pytest.mark.testrail(id=1313768)
    @pytest.mark.Regression
    @pytest.mark.order(6)
    def test_brnf_sa_nontpm_device_provision_unsuccess(self, brnf_sa_nontpm_prov_invalid_mac):
        """ Test case for nontpm device provision call on /hpe-nontpm
        Steps: POST request to /hpe-nontpm
        Expected result: should return x-status-code as fail-prov-no-device in response header
        """
        assert brnf_sa_nontpm_prov_invalid_mac.status_code == expected_response_data["switch_provision_no_device"]["response_code"]
        assert brnf_sa_nontpm_prov_invalid_mac.headers['X-Status-Code'] == expected_response_data["switch_provision_no_device"]["X-Status-Code"]

    @pytest.mark.Regression
    @pytest.mark.parametrize('api_path, x_type', [
        pytest.param("hpe-firmware-nontpm", "firmware-check",
                     marks=[pytest.mark.testrail(id=1313784), pytest.mark.order(7)],
                     id='nontpm_firmware_check_C1313784')])
    def test_nontpm_sw_dev_firmware(self, existing_acct_existing_dev_brnf_sa_sw_firmware, api_path, x_type):
        """
        ===== Using firmware Api call to verify devices can get the firmware URL======
        1. Using the device App Api make the header, and add the DNS entry to the hosts file
        2. Make device firmware call
        3. verify the call has 'X-Status-Code': 'success' +  firmware urls in the response
        """
        assert existing_acct_existing_dev_brnf_sa_sw_firmware.status_code == expected_response_data['switch_firmware_response']['response_code']
        assert existing_acct_existing_dev_brnf_sa_sw_firmware.headers["X-Status-Code"] == expected_response_data['switch_firmware_response'][
            'X-Status-Code']
        assert existing_acct_existing_dev_brnf_sa_sw_firmware.headers["X-Activation-Key"] is not None
        assert len(existing_acct_existing_dev_brnf_sa_sw_firmware.headers["X-Activation-Key"]) == 8
        assert "http://" in existing_acct_existing_dev_brnf_sa_sw_firmware.text
