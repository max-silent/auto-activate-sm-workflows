import logging

from automation_svc_ui.conftest import ExistingUserAcctDevices, NewUserAcctDevices
from hpe_glcp_automation_lib.libs.aop.helpers.aop_order_device_helper import NewDeviceOrder
from hpe_glcp_automation_lib.libs.aop.helpers.aop_payload_constants import AOPDeviceConstants
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)


class ManufactureDevicesHelper:
    def __init__(self, client_id, client_secret, dev_constants):
        log.info("Initialize New device creation class.")
        """Step #0: Create Test constants and variables like sn, mac, system under test, device_category, device_type"""
        self.end_username = RandomGenUtils.random_string_of_chars(7)
        self.cluster = ExistingUserAcctDevices.login_page_url
        self.app_api_hostname = ExistingUserAcctDevices.app_api_hostname
        self.dev_constants = dev_constants
        self.client_id = client_id
        self.client_secret = client_secret

    def create_device_of_type(self, device_type, devices_count=1, **kw):
        """Create a device of given type in the account
           :param device_type: type of device to be created (IAP, STORAGE, SWITCH, COMPUTE, GATEWAY)
           :param devices_count: count of devices to be added to returned dictionary.
           :param kw: optional key-word arguments; list of currently supported names:
               - end_username: value to be set into corresponding property of created device
                   instead of 'self.end_username' used by default.
               - lic_devices: device details - serial and material numbers. [{"serial":"SERABC", "material":"MATABC"}]
               example of usage - automation_svc_ui/local_libs/subscription_mgmt/sm_assignments_by_api.py:135
           :return: Dictionary with details of created devices in following format:
               {"device_<device_type><index>" :
                   {"device_type": "<device_type>", "serial_no": "<serial>", "mac": "<mac-address>"}
               }
        """

        device_info = {}
        device_list = []
        lic_devices = kw.get("lic_devices")
        baas = kw.get("baas")
        for num in range(0, devices_count):
            AOPDeviceConstants.add_device_of_type(self.dev_constants, device_type)
            device_index = len(self.dev_constants[device_type + "_serial"]) - 1
            serial = self.dev_constants[device_type + "_serial"][device_index]
            if lic_devices:
                serial = lic_devices[0]['serial']
            mac = self.dev_constants[device_type + "_mac"][device_index]
            aop_sso_url = ExistingUserAcctDevices.test_data["sso_host"]
            if device_type in ("STORAGE", "DHCI_STORAGE"):
                device_category = self.dev_constants["device_category_storage"]
                init_new_device_order = NewDeviceOrder(
                    self.app_api_hostname,
                    device_category,
                    device_type,
                    serial,
                    mac,
                    self.cluster,
                    kw.get("end_username") or self.end_username,
                    aop_sso_url,
                    self.client_id,
                    self.client_secret,
                )
                init_new_device_order.create_platform(mode="STORAGE")
                if device_type == "DHCI_STORAGE":
                    part = init_new_device_order.create_part_name(part_category="DHCI_STORAGE")
                else:
                    part = init_new_device_order.create_part_name(baas=baas)
                if lic_devices:
                    part = lic_devices[0]['material']
            elif device_type == "COMPUTE":
                device_category = self.dev_constants["device_category_compute"]
                init_new_device_order = NewDeviceOrder(
                    self.app_api_hostname,
                    device_category,
                    device_type,
                    serial,
                    mac,
                    self.cluster,
                    kw.get("end_username") or self.end_username,
                    aop_sso_url,
                    self.client_id,
                    self.client_secret,
                )
                init_new_device_order.create_platform()
                part = init_new_device_order.create_part_name()
            elif device_type == "IAP":
                device_category = self.dev_constants["device_category_nw"]
                part = self.dev_constants["DEFAULT_PART_MAP"]["IAP"]
                init_new_device_order = NewDeviceOrder(
                    self.app_api_hostname,
                    device_category,
                    device_type,
                    serial,
                    mac,
                    self.cluster,
                    kw.get("end_username") or self.end_username,
                    aop_sso_url,
                    self.client_id,
                    self.client_secret,
                )
            elif device_type == "SWITCH":
                device_category = self.dev_constants["device_category_nw"]
                part = self.dev_constants["DEFAULT_PART_MAP"]["SWITCH"]
                init_new_device_order = NewDeviceOrder(
                    self.app_api_hostname,
                    device_category,
                    device_type,
                    serial,
                    mac,
                    self.cluster,
                    kw.get("end_username") or self.end_username,
                    aop_sso_url,
                    self.client_id,
                    self.client_secret,
                )
            else:
                device_category = self.dev_constants["device_category_nw"]
                if device_type == "GATEWAY":
                    part = self.dev_constants["DEFAULT_PART_MAP"]["GATEWAY"]
                else:
                    part = self.dev_constants["DEFAULT_PART_MAP"]["CONTROLLER"]
                mac = self.dev_constants[device_type + "_mac"][device_index]
                init_new_device_order = NewDeviceOrder(
                    self.app_api_hostname,
                    device_category,
                    device_type,
                    serial,
                    mac,
                    self.cluster,
                    kw.get("end_username") or self.end_username,
                    aop_sso_url,
                    self.client_id,
                    self.client_secret,
                )
            mfr_device = init_new_device_order.create_manufacturing(part, baas=baas)
            if not mfr_device:
                log.error("not able to manufacture the device")
                return False
            init_new_device_order.create_pos_order()
            init_new_device_order.create_sds_order(part)
            device_info["device_" + str(device_type) + str(device_index)] = {}
            device_info["device_" + str(device_type) + str(device_index)]["device_type"] = device_type
            device_info["device_" + str(device_type) + str(device_index)]["serial_no"] = serial
            device_info["device_" + str(device_type) + str(device_index)]["mac"] = mac
            if device_type in ("STORAGE", "DHCI_STORAGE"):
                if not lic_devices:
                    storage_lic_key = init_new_device_order.create_lic_order(part)
                    device_info["device_" + str(device_type) + str(device_index)][
                        "lic_key"
                    ] = storage_lic_key
                device_info["device_" + str(device_type) + str(device_index)]["part_num"] = part
            if device_type == "COMPUTE":
                init_new_device_order.create_lic_order(part)
                device_info["device_" + str(device_type) + str(device_index)]["part_num"] = part
            device_list.append(device_info)
        log.info(f"List of created devices: {device_list}")
        if len(device_list) != devices_count:
            log.info("Not able to create devices in AOP")
            return False
        else:
            NewUserAcctDevices.iap_device_list = device_info
            log.info(device_info)
            return device_info
