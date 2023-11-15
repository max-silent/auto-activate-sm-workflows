import csv
import logging

log = logging.getLogger(__name__)


class ActivateOrdersHelper:
    """
    Activate Orders helper class.
    """

    @staticmethod
    def get_dev_details_per_dev_type(dev_groups_list):
        """Get list with details of ordered devices for each first device within each item of dev_groups_list.

        :param dev_groups_list: list of dicts, where key is assigned to devices type
             and value is list of dicts with details of the devices, belonging to this type.
        :return: list of dicts with devices details.
        """
        devices_details = []
        for grouped_devices_details in dev_groups_list:
            devices_details.append(list(grouped_devices_details.values())[0])
        return devices_details

    @staticmethod
    def generate_device_csv(devices: list, filename: str = "devices.csv"):
        """ Generated a new CSV file for corresponding device(s), for claiming via file upload

        :param devices: A list of dicts with devices info. E.g.: serial number, mac, tags
        :param filename: name of the file to be created. Defaults to 'devices.csv'
        :return: Name of newly created CSV file.
        """
        network_devices = ["IAP", "SWITCH", "GATEWAY", "NETWORK"]
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if devices[0].get("device_type") in network_devices:
                fieldnames = ["Serial_No", "MAC_Address", "tag:name1", "tag:name2"]
                writer.writerow(fieldnames)
                for device in devices:
                    row = [device["serial_no"], device["mac"], device["device_type"], "_"]
                    writer.writerow(row)
            else:
                fieldnames = ["Serial_No", "Product_ID", "tag:name1", "tag:name2"]
                writer.writerow(fieldnames)
                for device in devices:
                    row = [device["serial_no"], device["part_num"], device["mac"], "_"]
                    writer.writerow(row)
        return filename
