import logging
import json
from automation.conftest import ExistingUserAcctDevices

log = logging.getLogger(__name__)


class AdiTestHelper:
    """
     - Common Helper class for all the test cases
    """            
    @staticmethod
    def is_device_provisioned_to_acid_for_pcid(adi_app_api_session, pcid, acid, serial_number) -> bool:
        """
        Search for a device with the given serial number among the devices associated with the specified PCID and ACID.
        :param adi_app_api_session: A session object to make API calls.
        :param pcid: Platform customer ID.
        :param acid: Application customer ID.
        :param serial_number: The serial number of the device to be searched for.
        :return: True if the device is claimed and provisioned; False otherwise.
        """
        try:
            # Call the API method to get devices associated with the given PCID and ACID
            new_device_list = adi_app_api_session.get_devices_by_pcid_acid(
                platform_customer_id=pcid,
                application_customer_id=acid
            ).json()

            # Iterate over the list of devices to find the device with the given serial number
            for device in new_device_list["devices"]:
                if device["serial_number"] == serial_number:
                    log.info(f"Device {serial_number} Is Claimed and Provisioned..")
                    return True

            # If the device is not found, log a message and return False
            log.info(f"Device {serial_number} Is Not Provisioned..")
            return False

        # Catch any exceptions that may occur while making API calls or iterating over the device list
        except Exception as e:
            log.error(f"Error while searching for device: {e}")
            return False
    

    @staticmethod
    def find_archived_device_in_get_devices_by_pcid(adi_app_api_session, pcid, serial_number):
        """
        Search for a device with the given serial number among the archived devices associated with the specified PCID.
        :param app_api_session: A session object to make API calls.
        :param pcid: Platform customer ID.
        :param serial_number: The serial number of the device to be searched for.
        :return: True if the device is found in the archived list; False otherwise.
        """
        try:
            # Call the API method to get archived devices associated with the given PCID
            archived_devices_list = adi_app_api_session.get_devices_by_pcid(
                platform_customer_id=pcid,
                archived_only="ARCHIVED_ONLY"
            ).json()
            log.info(archived_devices_list)

            # Iterate over the list of archived devices to find the device with the given serial number
            device_found_in_archived_list = False
            for device in archived_devices_list["devices"]:
                if device["serial_number"] == serial_number:
                    device_found_in_archived_list = True
                    return device_found_in_archived_list

            # If the device is not found, return False
            return device_found_in_archived_list

        # Catch any exceptions that may occur while making API calls or iterating over the device list
        except Exception as e:
            log.info(f"Error while searching for device in archived list: {e}")
            return False
        
    def claim_vgw_device(self, adi_app_api_session):
        """
        ====== Creates the vgw device ========
        - Using is_device_provisioned_to_acid_for_pcid fucntion.
        - Verify if it is claimed.
        - Check if the device is provisioned.

        """

        pcid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_pcid"]
        username = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_username"] 
        acid = ExistingUserAcctDevices.test_data["brnf_existing_acct_existing_devices_acid"]
        

        response = adi_app_api_session.create_virtual_device(
            application_customer_id = acid, 
            platform_customer_id = pcid,
            username = username,
            part_number = "MC-VA"
            ).json()
        serial_number = response["serial_number"]
        if  response:
            log.info(serial_number)
            found_device = adi_app_api_session.verify_device_claimed_by_pcid(pcid, serial_number)
            log.info(found_device)

            if found_device:
                is_device_provisioned = self.is_device_provisioned_to_acid_for_pcid(
                    adi_app_api_session = adi_app_api_session,
                    pcid = pcid,
                    acid = acid,
                    serial_number = serial_number
                )
                log.info(is_device_provisioned)
                return is_device_provisioned

        else:
            return False

    @staticmethod
    def device_claim_with_app_api(platform_cust_id, username, device_type, device_data, brnf_app_api_session):
        """
        Workflow to claim one or more devices of the same type using an app api
        :param device_type: Type of device to be claimed
        :param ordered_devices: device to be claimed
        :param brnf_app_api_session: Authorization bearer token
        :return: True is response status code is 200, else False
        """

        try:
            for idx in range(0, len(device_data)):
                serial_number = device_data[f"device_{device_type}{idx}"]["serial_no"]
                mac_address = device_data[f"device_{device_type}{idx}"]["mac"]
                verify_claim_devices = \
                    brnf_app_api_session.claim_device_app_api("NETWORK",
                                                              serial_number,
                                                              platform_cust_id,
                                                              username,
                                                              mac_address)
                if json.loads(verify_claim_devices.content).get('status') == 200:
                    # if the API response is 200, verify is the device is found in the customers account using
                    # get_devices_by_pcid call
                    if brnf_app_api_session.verify_device_claimed_by_pcid(platform_cust_id, serial_number):
                        log.info("Device {} is claimed by PCID {}".format(serial_number, platform_cust_id))
                    else:
                        raise ValueError("Device {} is Not claimed by PCID {}".format(serial_number, platform_cust_id))
                else:
                    raise ValueError(f"Device '{serial_number}' was not claimed. "
                                     f"Response: '{verify_claim_devices.content}'.")

        except Exception as e:
            log.warning(e)
            return False
        return True
