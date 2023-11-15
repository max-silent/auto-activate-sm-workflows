import logging
import os
import time

import pytest
from automation.conftest import get_add_device_expected_responses
import allure
from automation.conftest import ExistingUserAcctDevices
from automation.tests.workflows.brownfield.storage_compute.brnf_str_com_existing_acct_devices import (
    WfScExistingAcctDevices,
)

log = logging.getLogger(__name__)

expected_response_data = get_add_device_expected_responses()

@allure.parent_suite("activate-sm-workflows")
@pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
@pytest.mark.skipif("pavo" in ExistingUserAcctDevices.login_page_url, reason="Not supported on pavo.")
@allure.suite("Brownfield Idev Ldev compute device provision")
@pytest.mark.Plv
class TestBrownfieldComputeIdevLdev:

    @pytest.mark.order(1)
    @pytest.mark.Regression
    @pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
    def test_brnf_sc_user_login_load_account(self, brnf_sa_sc_user_login_load_account):
        """
        ===== User login to the account using user API for other tests to run user api ======
        1. User login to the account using new user and password
        2. User load the pcid account for other tests to run user api for other subsequent test cases
        """
        assert brnf_sa_sc_user_login_load_account


    @pytest.mark.order(2)
    @pytest.mark.Regression
    @pytest.mark.parametrize('serial, part, certs', [("STCOMNONEXTN", "STCOMPT1", "idev_ldev_non_existent_comp_certs")])
    def test_compute_dev_non_existent_C1337691(self, brnf_idev_ldev_compute_prov, serial, part, certs):
        """
        ===== Idev Ldev provision call made with non-existent device ======
        1. Using the device App Api make the header, and add the DNS entry to  the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail_prov_no_device'
        """
        response = brnf_idev_ldev_compute_prov
        assert response.status_code == expected_response_data["compute_provision_no_device"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["compute_provision_no_device"]["X-Status-Code"]

    @pytest.mark.order(3)
    @pytest.mark.Regression
    def test_unassign_comp_device(self,brnf_unassign_comp_devices_to_app, brnf_sa_sc_user_login_load_account):
        """
         ===== Manually unassign device from application ======
         1. Using the login session
         2. Manually unassign the application
         3. Verify COMPUTE device is unassigned from the application correctly
         """
        if brnf_sa_sc_user_login_load_account:
            assert brnf_unassign_comp_devices_to_app
        time.sleep(10)

    @pytest.mark.order(4)
    @pytest.mark.Regression
    @pytest.mark.parametrize('serial, part, certs', [("STCOMSER1", "STCOMPT1", "idev_ldev_success_certs")])
    def test_compute_dev_fail_prov_no_rule_C1337692(self, brnf_idev_ldev_compute_prov, serial, part, certs):
        """
        ===== Idev Ldev provision call made before application assignment ======
        1. Using the device App Api make the header, and add the DNS entry to  the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail_prov_no_rule'
        """
        response = brnf_idev_ldev_compute_prov
        log.info("Headers: {}, text: {}".format(response.headers, response.text))
        assert response.status_code == expected_response_data["compute_provision_no_rule"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["compute_provision_no_rule"]["X-Status-Code"]
        assert "message" in response.text

    @pytest.mark.order(5)
    @pytest.mark.Regression
    def test_assign_comp_device(self, brnf_assign_comp_devices_to_app, brnf_sa_sc_user_login_load_account):
        """
         ===== Manually assign assign device to application ======
         1. Using the login session
         2. Manually assign the application
         3. Verify COMPUTE device is assigned to the application correctly
         """
        if brnf_sa_sc_user_login_load_account:
            assert brnf_assign_comp_devices_to_app
        time.sleep(10)

    @pytest.mark.Regression
    @pytest.mark.parametrize('serial, part, certs', [
        pytest.param("STCOMSER1", "STCOMPT1", "idev_ldev_success_certs", marks=pytest.mark.order(6), id='success_scenario_C1337693'),
        pytest.param("STTFHIK", "STCOMPGYG", "idev_ldev_success_certs", marks=pytest.mark.order(7), id='correct_cert_incorrect_apinfo_C1337694'),
        pytest.param("STCOMSER1", "STCOMPT1", "idev_ldev_non_existent_comp_certs", marks=pytest.mark.order(8), id='incorrect_cert_correct_ap_info_C1337695'),
        # pytest.param("noapinfo", "", "idev_ldev_success_certs", marks=pytest.mark.order(9), id='correct_cert_no_apinfo_C1337696'),
        pytest.param("STCOMSER1", "STCOMPT1", "idev_ldev_incorrect_serial_certs", marks=pytest.mark.order(10), id='incorrect_serial_correct_apinfo_C1337702')])
    def test_compute_dev_success(self, brnf_idev_ldev_compute_prov, serial, part, certs):
        """
        ===== Idev Ldev provision success call made with existent device======
        1. Using the device App Api make the header, and add the DNS entry to  the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'success'
        """
        response = brnf_idev_ldev_compute_prov
        log.info("Headers: {}, text: {}".format(response.headers, response.text))
        assert response.status_code == expected_response_data["st_com_prov_positive"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["st_com_prov_positive"]["X-Status-Code"]
        assert response.headers["X-Athena-Url"] is not None
        assert response.headers["X-Mode"] == expected_response_data["st_com_prov_positive"]["X-Mode_Comp"]
        assert "message" in response.text


    @pytest.mark.order(11)
    @pytest.mark.Regression
    @pytest.mark.parametrize('serial, part, certs', [("", "STCOMPT1", "idev_ldev_non_existent_comp_certs")])
    def test_compute_dev_no_serial_cert_and_apinfo_C1337698(self, brnf_idev_ldev_compute_prov, serial, part, certs):
        """
        ===== Idev Ldev provision call made with missing serial number in both cert and X-ap-info ======
        1. Using the device App Api make the header, and add the DNS entry to  the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail_no_serial'
        """
        response = brnf_idev_ldev_compute_prov
        log.info("Headers: {}, text: {}".format(response.headers, response.text))
        assert response.status_code == expected_response_data["compute_provision_no_serial"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["compute_provision_no_serial"][
            "X-Status-Code"]
        assert "message" in response.text

    @pytest.mark.order(12)
    @pytest.mark.Regression
    @pytest.mark.parametrize('serial, part, certs', [("STCOMSER1", "", "idev_ldev_without_part_certs")])
    def test_compute_dev_no_part_cert_and_apinfo_C1337699(self, brnf_idev_ldev_compute_prov, serial, part, certs):
        """
        ===== Idev Ldev provision call made with missing part number in both cert and X-ap-info ======
        1. Using the device App Api make the header, and add the DNS entry to  the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail_no_part'
        """
        response = brnf_idev_ldev_compute_prov
        log.info("Headers: {}, text: {}".format(response.headers, response.text))
        assert response.status_code == expected_response_data["compute_provision_no_part"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["compute_provision_no_part"][
            "X-Status-Code"]
        assert "message" in response.text

    @pytest.mark.Regression
    @pytest.mark.parametrize('serial, part, certs', [
        # pytest.param("noapinfo", "", "idev_ldev_non_existent_comp_certs", marks=pytest.mark.order(13),id='incorrect_cert_no_apinfo_C1337697'),
        pytest.param("STCOMSER1", "STCOMPTUNK1", "idev_ldev_incorrect_part_certs", marks=pytest.mark.order(14), id='correct_serial_and_incorrect_part_C1337701'),
        pytest.param("STCOMSERUNK1", "STCOMPT1", "idev_ldev_incorrect_serial_certs", marks=pytest.mark.order(15), id='incorrect_serial_and_correct_part_C1337700')])
    def test_compute_device_not_found(self, brnf_idev_ldev_compute_prov, serial, part, certs):
        """
        # Idev Ldev provision call made with incorrect cert but without X-ap-info header
        # Idev Ldev provision call made with correct serial and incorrect part in both cert and X-ap-info
        # Idev Ldev provision call made with incorrect serial and correct part in both cert and X-ap-info

        1. Using the device App Api make the header, and add the DNS entry to  the hosts file
        2. Make device provisioning call
        3. verify the call has 'X-Status-Code': 'fail_prov_no_device'
        """
        response = brnf_idev_ldev_compute_prov
        log.info("Headers: {}, text: {}".format(response.headers, response.text))
        assert response.status_code == expected_response_data["compute_provision_no_device"]["response_code"]
        assert response.headers["X-Status-Code"] == expected_response_data["compute_provision_no_device"][
            "X-Status-Code"]
        assert "message" in response.text