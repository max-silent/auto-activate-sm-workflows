import logging

log = logging.getLogger(__name__)
class ExistingAccountExistingNetworkDeviceHelper:    

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
            log.info(f"Error while searching for device: {e}")
            return False