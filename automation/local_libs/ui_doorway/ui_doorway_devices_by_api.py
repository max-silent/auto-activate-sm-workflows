import logging
import time

from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway

log = logging.getLogger(__name__)

ALLOWED_DEVICE_TYPES = "STORAGE", "DHCI_STORAGE", "COMPUTE", "IAP", "SWITCH", "CONTROLLER", "GATEWAY"


class UiDoorwayDevices:
    @staticmethod
    def claim_app_assignment(device_type, ordered_devices, sa_user_login_load_account: UIDoorway):
        """Claim ordered devices with app assignment via ui-doorway.

        :param device_type: devices type. Allowed values: "STORAGE", "COMPUTE", "IAP", "SWITCH", "GATEWAY".
        :param ordered_devices: dictionary with ordered devices details (serial number, mac-address, licence key, etc).
        :param sa_user_login_load_account: UIDoorway instance for user API-calls.
        :return: response from add_device_activate_inventory() call if successful or False otherwise.
        """
        if device_type not in ALLOWED_DEVICE_TYPES:
            raise ValueError(f"Not supported device type: '{device_type}'")
        time.sleep(9)
        """adding delay for app provisioning to add application customer id
        Activate services for auto assignments"""
        device_list_di = {"devices": []}
        try:
            if device_type in ("STORAGE", "DHCI_STORAGE"):
                for idx in range(0, len(ordered_devices)):
                    device_list_di["devices"].append(
                        {
                            "serial_number": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["serial_no"],
                            "entitlement_id": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["lic_key"],
                            "app_category": "STORAGE",
                        }
                    )
            elif device_type == "COMPUTE":
                for idx in range(0, len(ordered_devices)):
                    device_list_di["devices"].append(
                        {
                            "serial_number": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["serial_no"],
                            "part_number": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["part_num"],
                            "app_category": device_type,
                        }
                    )
            else:
                for idx in range(0, len(ordered_devices)):
                    device_list_di["devices"].append(
                        {
                            "serial_number": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["serial_no"],
                            "mac_address": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["mac"],
                            "app_category": "NETWORK",
                        }
                    )
        except Exception as e:
            log.warning(e)

        verify_claim_devices = sa_user_login_load_account.add_device_activate_inventory(
            device_list_di
        )
        if "OK" in verify_claim_devices:
            return verify_claim_devices
        else:
            return False

    @staticmethod
    def claim_app_assignment_iaas_hciaas(device_type, ordered_devices, sa_user_login_load_account: UIDoorway):
        """Claim ordered devices with app assignment via ui-doorway.

        :param device_type: devices type. Allowed values: "STORAGE", "COMPUTE", "IAP", "SWITCH", "GATEWAY".
        :param ordered_devices: dictionary with ordered devices details (serial number, mac-address, licence key, etc).
        :param sa_user_login_load_account: UIDoorway instance for user API-calls.
        :return: response from add_device_activate_inventory() call if successful or False otherwise.
        """
        if device_type not in ALLOWED_DEVICE_TYPES:
            raise ValueError(f"Not supported device type: '{device_type}'")
        time.sleep(9)
        """adding delay for app provisioning to add application customer id
        Activate services for auto assignments"""
        device_list_di = {"devices": []}
        try:
            if device_type == "STORAGE":
                for idx in range(0, len(ordered_devices)):
                    device_list_di["devices"].append(
                        {
                            "serial_number": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["serial_no"],
                            "part_number": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["part_num"],
                            "app_category": device_type,
                        }
                    )
            elif device_type == "COMPUTE":
                for idx in range(0, len(ordered_devices)):
                    device_list_di["devices"].append(
                        {
                            "serial_number": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["serial_no"],
                            "part_number": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["part_num"],
                            "app_category": device_type,
                        }
                    )
            else:
                for idx in range(0, len(ordered_devices)):
                    device_list_di["devices"].append(
                        {
                            "serial_number": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["serial_no"],
                            "mac_address": ordered_devices[
                                "device_" + device_type + str(idx)
                                ]["mac"],
                            "app_category": "NETWORK",
                        }
                    )
        except Exception as e:
            log.warning(e)

        verify_claim_devices = sa_user_login_load_account.add_device_activate_inventory(
            device_list_di
        )
        if "OK" in verify_claim_devices:
            return verify_claim_devices
        else:
            return False

    @staticmethod
    def get_subscription_key(device_type, serial_no, part_no, sa_user_login_load_account: UIDoorway):
        """

        :param device_type: device type.
        :param serial_no: device's serial number.
        :param part_no: device's part number.
        :param sa_user_login_load_account: UIDoorway instance for user API-calls.
        :return: subscription key assigned to device or None.
        """
        if device_type not in ALLOWED_DEVICE_TYPES:
            raise ValueError(f"Not supported device type: '{device_type}'")
        payload = {
            "device_type": device_type,
            "serial_number": serial_no,
            "part_number": part_no
        }
        try:
            resp = sa_user_login_load_account.filter_devices(payload)

            return resp["devices"][0].get("subscription_key")
        except Exception as e:
            log.warning(e)
        return None

    @staticmethod
    def delete_folder(folder_name: str, logged_in_user: UIDoorway, target_pcid: str = None, ignore_non_existing=True):
        """Delete customer devices 'folder_name' folder of specified (if pcid not None) or current customer.
        Note: call with specified 'target_pcid' supposed to be performed by TAC-user.

        :param folder_name: name of folder to be deleted.
        :param logged_in_user: UIDoorway instance used to call deletion request.
        :param target_pcid: pcid of customer, whose folder should be deleted.
        :param ignore_non_existing: do not throw error if folder requested for deletion does not exist already.
        """
        log.info(f"Deleting device folder with name '{folder_name}'.")
        folder_id = None
        folders_dict = logged_in_user.get_folders(target_pcid)
        for folder in folders_dict.get("folders", []):
            if folder["folder_name"] == folder_name:
                folder_id = folder["folder_id"]
                break
        if folder_id:
            rules_dict = logged_in_user.get_folder_rules(target_pcid)
            for rule in rules_dict.get("rules", []):
                if rule["folder_id"] == folder_id:
                    logged_in_user.delete_folder_rule(rule["rule_id"], target_pcid)
            logged_in_user.delete_folder(folder_id, target_pcid)
        elif not ignore_non_existing:
            raise ValueError(f"Device Folder with name '{folder_name}' does not exist for current user.")

    @staticmethod
    def delete_alias(alias_name: str, logged_in_user: UIDoorway, target_pcid: str, ignore_non_existing=True):
        """Delete customer alias of specified customer.
        Note: Supposed to be performed by TAC-user (passed via 'logged_in_user' argument).

        :param alias_name: name of alias to be deleted.
        :param logged_in_user: UIDoorway instance used to call deletion request.
        :param target_pcid: pcid of customer, whose alias should be deleted.
        :param ignore_non_existing: do not throw error if alias requested for deletion does not exist already.
        """
        log.info(f"Deleting alias with name '{alias_name}'.")
        try:
            logged_in_user.delete_cm_activate_alias(alias_name, target_pcid)
        except Exception as ex:
            if not ignore_non_existing:
                raise ValueError(f"Alias with name '{alias_name}' does not exist for current user. Error: \n{ex}")
