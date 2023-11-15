import logging

import allure
import pytest

from automation.conftest import ExistingUserAcctDevices

log = logging.getLogger(__name__)


@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield network devices")
@pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
@pytest.mark.skipif("pavo" in ExistingUserAcctDevices.login_page_url, reason="Not supported on pavo.")
@allure.sub_suite("Existing account - Existing network devices")
class TestExistingDevicesAppApi:
    @pytest.mark.order(1)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220655)
    def test_update_app_instance_endpoint_c1220655(self, adi_app_api_session, adi_app_api_helper):
        """
        :param adi_app_api_session: Api Session to make API calls
         - Testing the API to Update the application instance endpoint.
        """

        app_instance_id = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_instance_id"]
        username = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_username"]
        pcid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_pcid"] 



        first_response = adi_app_api_session.get_info_application_instance(app_instance_id).json()
        log.debug(first_response)
        original_endpoint = ""
        for info in first_response['provisioning_info']:
            if info['device_family'] == 'IAP':
                original_endpoint = info['device_endpoint_url']
                break
        new_endpoint = f"{original_endpoint}.modified"
        log.debug(original_endpoint)

        provision_info = [
            {
                "device_family": "IAP",
                "device_endpoint_url": new_endpoint
            }
        ]

        modified_respone = adi_app_api_helper.application_instance_upgrade_helper(
            platform_customer_id = pcid,
            username = username,
            provisioning_data = provision_info,
            application_instance_id = app_instance_id,
            device_types = ["AP"]
            )
        log.debug(modified_respone.json())
        assert modified_respone.status_code == 200, "Couldn't modify the endpoint.."

        response_after_modify = adi_app_api_session.get_info_application_instance(app_instance_id).json()
        log.debug(response_after_modify)

        for info in response_after_modify['provisioning_info']:
            if info['device_family'] == 'IAP':
                modified_endpoint = info['device_endpoint_url']
                break
        assert new_endpoint == modified_endpoint

        #Revert back the changed endpoint to original.

        provision_info_final = [
            {
                "device_family": "IAP",
                "device_endpoint_url": original_endpoint
            }
        ]

        adi_app_api_helper.application_instance_upgrade_helper(
            platform_customer_id = pcid,
            username = username,
            provisioning_data = provision_info_final,
            application_instance_id = app_instance_id,
            device_types = ["AP"])

        final_response = adi_app_api_session.get_info_application_instance(app_instance_id).json()

        log.debug(final_response)
        final_endpoint = ""
        for info in final_response['provisioning_info']:
            if info['device_family'] == 'IAP':
                final_endpoint = info['device_endpoint_url']
                break
        
        log.debug(original_endpoint)
        log.debug(final_endpoint)
        assert original_endpoint == final_endpoint, "Could not change device_endpoint_url.."

        reverted_response = adi_app_api_session.get_info_application_instance(app_instance_id).json()
        log.debug(reverted_response)