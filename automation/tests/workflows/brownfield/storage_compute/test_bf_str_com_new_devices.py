import pytest
import allure
from automation.conftest import ExistingUserAcctDevices

@pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield storage compute devices")
@allure.sub_suite("Brownfield existing account new storage compute devices")
class TestClaimDeviceBetweenAccts:
    @pytest.mark.Regression
    @pytest.mark.Plv
    @pytest.mark.order(1)
    @pytest.mark.testrail(id=1220631)
    def test_claim_device_acc1_acc2_c1220631(self, brnf_app_api_session, adi_app_api_helper, order_sc_compute_devices):
        """
            ===== Manually create a compute device and claim in account 1 and account 2======
            1. Using the app api session
            2. Manually create COMPUTE device and claim from account 1
            3. Verify the device is claimed from account 1
            4. Use account 2
            5. Claim COMPUTE device from account2
            6. Verify the device is claimed from account 2

            args:
                create_compute_device - Fixture to create compute device
        """
        mac = order_sc_compute_devices['device_COMPUTE0']['mac']
        device_serial_number = order_sc_compute_devices['device_COMPUTE0']['serial_no']
        created_part_num = order_sc_compute_devices['device_COMPUTE0']['part_num']
        response_data = {}
        # claiming the device in account 1
        resp1 = brnf_app_api_session.claim_device_app_api(device_category='COMPUTE',
                                                          serial=device_serial_number,
                                                          platform_id=
                                                          ExistingUserAcctDevices.test_data[
                                                              "brownfield_account_with_one_network_app"]
                                                          ["pcid"],
                                                          username=
                                                          ExistingUserAcctDevices.test_data[
                                                              'brownfield_account_with_one_network_app'][
                                                              'username'],
                                                          part_num=created_part_num,
                                                          mac=mac)

        response_data['account1_claim_status_code'] = resp1.json()['status']
        assert response_data['account1_claim_status_code'] == 200
        assert brnf_app_api_session.verify_device_claimed_by_pcid(ExistingUserAcctDevices.test_data
                                                                  ["brownfield_account_with_one_network_app"]["pcid"],
                                                                  device_serial_number)

        #if device is provisioned, then unprovision the device
        is_device_provisioned = adi_app_api_helper.is_device_provisioned_to_pcid(platform_customer_id=ExistingUserAcctDevices.test_data[
                                                              "brownfield_account_with_one_network_app"]
                                                          ["pcid"], serial_number=device_serial_number)
        if is_device_provisioned:
            payload = {
                "serial_number": device_serial_number,
                "part_number": created_part_num
            }
            unassign_response = brnf_app_api_session.unprovision_device_from_application(payload=payload, platform_customer_id=ExistingUserAcctDevices.test_data[
                                                              "brownfield_account_with_one_network_app"]
                                                          ["pcid"])
            assert unassign_response.status_code == 200

        # claiming the device in account 2
        resp2 = brnf_app_api_session.claim_device_app_api(device_category='COMPUTE',
                                                          serial=device_serial_number,
                                                          platform_id=ExistingUserAcctDevices.test_data[
                                                              "brownfield_account_with_all_app_types"]
                                                          ["pcid"],
                                                          username=ExistingUserAcctDevices.test_data[
                                                              'brownfield_account_with_all_app_types'][
                                                              'username'],
                                                          part_num=created_part_num,
                                                          mac=mac)

        response_data['account2_claim_status_code'] = resp2.json()['status']
        assert response_data['account2_claim_status_code'] == 200
        assert brnf_app_api_session.verify_device_claimed_by_pcid(ExistingUserAcctDevices.test_data
                                                                  ["brownfield_account_with_all_app_types"]["pcid"],
                                                                  device_serial_number)


    @pytest.mark.Regression
    @pytest.mark.order(2)
    @pytest.mark.testrail(id=1220653)
    def test_iap_assigned_claim_batch_verify_status_C1220653(self, brnf_app_api_session, brnf_sa_order_iap_devices,
                                                             order_sc_storage_legacy_devices,
                                                             order_sc_compute_devices):
        """
            ===== Claims activate:App Api to get batch verify claim status  ======
            1. Create IAP assigned device/ Create storage assigned device/create compute unassigned device
            2. Submit a get device list by acid
            3. find newly created device in the list
            4. Run post_batch_verify_status api and validate the status of the device

            Args:
                create_iap_device, create_storage_device, create_compute_device - Fixture to create iap/ storage/ compute devices
                app_api_session - An instance of the AppAPISession class used to interact with the API.
        """
        # creating the iap device
        iap_mac = brnf_sa_order_iap_devices['device_IAP0']['mac']
        iap_serial_number = brnf_sa_order_iap_devices['device_IAP0']['serial_no']

        # claiming the iap device in account
        resp1 = brnf_app_api_session.claim_device_app_api(device_category='NETWORK',
                                                          serial=iap_serial_number,
                                                          platform_id=
                                                          ExistingUserAcctDevices.test_data[
                                                              "brownfield_account_with_all_app_types"]
                                                          ["pcid"],
                                                          username=
                                                          ExistingUserAcctDevices.test_data[
                                                              'brownfield_account_with_all_app_types'][
                                                              'username'],
                                                          mac=iap_mac)

        device_data = {'serial_number': iap_serial_number, 'mac_address': iap_mac, 'device_type': "AP"}

        desired_acid = ExistingUserAcctDevices.test_data["brownfield_account_with_one_network_app"]["acid_network"]
        desired_pcid = ExistingUserAcctDevices.test_data["brownfield_account_with_all_app_types"]["pcid"]
        desired_username = ExistingUserAcctDevices.test_data["brownfield_account_with_all_app_types"]["username"]

        # checks if device is not assigned
        device_list = brnf_app_api_session.get_devices_by_pcid(platform_customer_id=
                                                               ExistingUserAcctDevices.test_data[
                                                                   "brownfield_account_with_all_app_types"]["pcid"])
        if not iap_serial_number in device_list.json()['devices']:
            # assigning the iap device
            resp = brnf_app_api_session.provision_dev_acid(desired_acid, [device_data],
                                                           platform_customer_id=desired_pcid,
                                                           username=desired_username)

        # creates storage device
        storage_mac = order_sc_storage_legacy_devices['device_STORAGE0']['mac']
        storage_serial_number = order_sc_storage_legacy_devices['device_STORAGE0']['serial_no']
        storage_part_number = order_sc_storage_legacy_devices['device_STORAGE0']['part_num']
        storage_entitlement_id = order_sc_storage_legacy_devices['device_STORAGE0']['lic_key']

        # claiming the storage device in account 1
        resp1 = brnf_app_api_session.claim_device_app_api(device_category='STORAGE',
                                                          serial=storage_serial_number,
                                                          platform_id=
                                                          ExistingUserAcctDevices.test_data[
                                                              "brownfield_account_with_all_app_types"]
                                                          ["pcid"],
                                                          username=
                                                          ExistingUserAcctDevices.test_data[
                                                              'brownfield_account_with_all_app_types'][
                                                              'username'],
                                                          entitlement_id=storage_entitlement_id)

        device_data = {'serial_number': storage_serial_number, 'mac_address': storage_mac,
                       'entitlement_id': storage_entitlement_id, 'device_type': "STORAGE"}

        desired_acid = ExistingUserAcctDevices.test_data["brownfield_account_with_all_app_types"]["acid_network"]
        desired_pcid = ExistingUserAcctDevices.test_data["brownfield_account_with_all_app_types"]["pcid"]
        desired_username = ExistingUserAcctDevices.test_data["brownfield_account_with_all_app_types"]["username"]

        # checks if device is not assigned

        device_list = brnf_app_api_session.get_devices_by_pcid(platform_customer_id=
                                                               ExistingUserAcctDevices.test_data[
                                                                   "brownfield_account_with_all_app_types"]["pcid"])
        if not storage_serial_number in device_list.json()['devices']:
            # assigning the storage device
            resp = brnf_app_api_session.provision_dev_acid(desired_acid, [device_data],
                                                           platform_customer_id=desired_pcid,
                                                           username=desired_username)

        # creates compute device
        compute_mac = order_sc_compute_devices['device_COMPUTE0']['mac']
        compute_serial_number = order_sc_compute_devices['device_COMPUTE0']['serial_no']
        compute_part_num = order_sc_compute_devices['device_COMPUTE0']['part_num']

        # claiming the compute device in account 1
        resp1 = brnf_app_api_session.claim_device_app_api(device_category='COMPUTE',
                                                          serial=compute_serial_number,
                                                          platform_id=
                                                          ExistingUserAcctDevices.test_data[
                                                              "brownfield_account_with_all_app_types"]
                                                          ["pcid"],
                                                          username=
                                                          ExistingUserAcctDevices.test_data[
                                                              'brownfield_account_with_all_app_types'][
                                                              'username'],
                                                          part_num=compute_part_num,
                                                          mac=compute_mac)

        pcid = ExistingUserAcctDevices.test_data["brownfield_account_with_all_app_types"]["pcid"]
        device_list = brnf_app_api_session.get_devices_by_pcid(platform_customer_id=pcid)

        device_data = []
        for device in device_list.json()['devices']:
            if device['serial_number'] in [iap_serial_number, storage_serial_number, compute_serial_number]:
                device_data.append(device)

        resp = brnf_app_api_session.batch_verify_claim(device_data)
        response_data = {'response': resp.json(), 'status_code': resp.status_code, 'device_data': device_data}
        assert response_data['status_code'] == 200
        for device in response_data['device_data']:
            if device['device_type'] in ['AP', 'STORAGE']:
                assert response_data['response']['responses'][0]['response_message'] == 'device already assigned to ' \
                                                                                        'that customer'
                assert response_data['response']['responses'][0]['application_customer_id'] == device[
                    'application_customer_id']
            elif device['device_type'] in ['COMPUTE']:
                assert response_data['response']['responses'][0]['response_message'] == 'claimable'
                assert response_data['response']['responses'][0]['application_customer_id'] is None
