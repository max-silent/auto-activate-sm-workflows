import logging
import os
import time
import pytest
import copy

from automation.conftest import ExistingUserAcctDevices, NewUserAcctDevices
from automation.local_libs.activate_inventory.activate_inventory_ui_utils import ActivateInventoryVerifier
from automation.local_libs.activate_inventory.activate_inventory_ui_utils import DeviceInventoryHelper
from automation.local_libs.activate_orders.activate_orders_utils import ActivateOrdersHelper
from automation.local_libs.audit_logs.audit_logs_ui_utils import AuditLogsVerifier
from automation.local_libs.subscription_mgmt.sm_ui_utils import SmVerifier
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.choose_account_page import ChooseAccount
from hpe_glcp_automation_lib.libs.add.device_calls.device_prov import (
    NetworkStorageComputeDeviceProvisionHelper,
)
from automation.conftest import ExistingUserAcctDevices
from hpe_glcp_automation_lib.libs.adi.app_api.adi_app_api import ActivateInventory
from hpe_glcp_automation_lib.libs.adi.ui.dev_inventory_page import DevicesInventory
from hpe_glcp_automation_lib.libs.aop.helpers.aop_order_device_helper import (
    NewDeviceOrder,
)
from hpe_glcp_automation_lib.libs.aop.helpers.aop_payload_constants import (
    AOPDeviceConstants,
)
from hpe_glcp_automation_lib.libs.app_prov.ui.my_applications_page import MyApplications
from hpe_glcp_automation_lib.libs.authn.ui.login_page import Login
from hpe_glcp_automation_lib.libs.commons.ui.manage_account_page import ManageAccount
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import (
    browser_page,
    browser_stop,
)
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils
from hpe_glcp_automation_lib.libs.sm.app_api.sm_app_api import SubscriptionManagementApp

log = logging.getLogger(__name__)


def check_payload_inclusion(out_data, in_data):
    try:
        for i in in_data.keys():
            if type(in_data[i]) == str:
                if out_data[i].casefold() != in_data[i].casefold():
                    return False
        return True
    except Exception as e:
        log.info(e)
        return False


class aopFlows():
    def __init__(self, end_username=False, pcid= None):
        log.info("Initialize new_device_existing_user.")
        """Step #0: Create Test constants and variables like sn, mac, system under test, device_category, device_type"""
        init_dev_constants = AOPDeviceConstants()
        if not end_username:
            self.end_username = RandomGenUtils.random_string_of_chars(7)
        else:
            self.end_username = pytest.globalvar['runtime_testdata']['end_username']
            self.unv_end_username = pytest.globalvar['runtime_testdata']['unv_end_username']
        if not pcid:
            self.pcid = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_pcid1"]
        else:
            self.pcid = pcid
        self.acid = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_app_cid"]
        self.username = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_username"]
        self.cluster = ExistingUserAcctDevices.login_page_url
        self.email_IdRand = "hcloud203+" + str(self.end_username) + "@gmail.com"
        self.app_api_hostname = ExistingUserAcctDevices.app_api_hostname
        self.dev_constants = init_dev_constants.new_mfr_device_constants()
        self.aop_sso_url = ExistingUserAcctDevices.test_data["sso_host"]
        self.aop_client = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_id"]
        self.aop_secret = ExistingUserAcctDevices.test_data["brnf_existing_acct_new_devices_client_secret"]
        self.adi = ActivateInventory(host=self.app_api_hostname,
                                     sso_host=ExistingUserAcctDevices.sso_hostname, client_id=self.aop_client,
                                     client_secret=self.aop_secret)

    def make_order(self,dev_type=None, part_cat=None ):
        if dev_type in ["IAP", "SWITCH", "GATEWAY", "AP", "IAP"]:
            device_category = "NETWORK"
        elif dev_type in ["STORAGE", "DHCI_STORAGE"]:
            device_category = "STORAGE"
        elif dev_type in ["COMPUTE", "DHCI_COMPUTE", "SERVER"]:
            device_category = "COMPUTE"
        self.part_cat = part_cat
        device_type = dev_type
        rand_string_details = {"length": 5, "lowercase": False, "uppercase": True, "digits": True}
        serial = RandomGenUtils.random_string_of_chars(**rand_string_details)
        mac = RandomGenUtils.generate_random_MAC_address()
        self.init_new_device_order = NewDeviceOrder(
        self.app_api_hostname,
        device_category,
        device_type,
        serial,
        mac,
        self.cluster,
        self.end_username,
        self.aop_sso_url,
        self.aop_client,
        self.aop_secret,
    )
        return self.init_new_device_order

    def create_device_of_type(self, device_type=None, MinParams=False, part_category=None):
        """Create a device of given type in the account
           :param device_type: type of device to be created (IAP, STORAGE, SWITCH, COMPUTE, GATEWAY)
           :param devices_count: count of devices to be added to returned dictionary.
        """
        self.order = self.make_order(device_type)
        platform_name = RandomGenUtils.generate_random_alphanumeric_string(5)
        self.order.create_platform(mode=self.order.deviceCategory, name=platform_name)
        part = self.order.create_part_name(platform=platform_name, part_category=part_category)

        if MinParams:
            mfr_device = self.order.create_manufacturing(part, MinParams=True)
        else:
            mfr_device = self.order.create_manufacturing(part)
        return mfr_device, part

    def create_oaas_of_type(self, device_type):
        """Create an oaas device of given type in the account
           :param device_type: type of device to be created (STORAGE,NETWORK,COMPUTE
        """
        self.order = self.make_order(device_type)
        platform_name = RandomGenUtils.generate_random_alphanumeric_string(5)
        self.order.create_platform(mode=self.order.deviceCategory, name = platform_name)
        part = self.order.create_part_name(platform=platform_name)
        #part = self.order.create_part_name( platform=platform_name, part_category=part_category)
        oaas_objkey = self.order.create_oaas(part, device_type)
        res = self.order.get_oaas_bykey(oaas_objkey)
        return res, part

    def update_manufacturing(self, dev_type, newvals):
        """Create a device of given type in the account
           :param original payload
           :param devices_count: count of devices to be added to returned dictionary.
        """
        payload = self.order.order.manufacturingdata['manufacturing_data_list'][0]['parent_device']
        for i in newvals.keys():
            payload[i] = newvals[i]
        update_manufacture_res =  self.order.update_manufacturing(dev_type, payload)
        return check_payload_inclusion(update_manufacture_res[1], payload)

    def update_manufacturing_addchild(self, dev_type):
        """Create a device of given type in the account
           :param original payload
           :param devices_count: count of devices to be added to returned dictionary.
        """
        payload = self.order.order.manufacturingdata['manufacturing_data_list'][0]['parent_device']
        parentObjkey = payload['obj_key']
        child_payload = copy.deepcopy(payload)
        del(child_payload['eth_mac'])
        child_payload['serial_number'] = 'C' + child_payload['serial_number']
        child_payload['obj_key'] = child_payload['obj_key'] + '_CHILD'
        child = {'parent_device': child_payload}
        new_payload = {'parent_device': payload, 'child_devices': [child]}
        update_manufacture_res = self.order.update_manufacturing(dev_type, new_payload, child=parentObjkey)
        return update_manufacture_res[0]


    def update_Sds(self, dev_type, newvals):
        """Update sales direct order
          :param device type
           :param values to be updated
        """
        payload = self.order.order.sales_order_data['sales_direct_shipment_data_list'][0]
        for i in newvals.keys():
            payload[i] = newvals[i]
        obj_key = payload['obj_key']
        update_sds_res = self.order.update_Sds_order(payload,obj_key,dev_type=dev_type)[1]
        return check_payload_inclusion(update_sds_res, payload)

    def update_Pos(self, dev_type, newvals):
        """Update point of sales order
           :param device type
           :param values to be updated
        """
        payload = self.order.order.point_ofsales_order_data['point_of_sales_data_list'][0]
        for i in newvals.keys():
            payload[i] = newvals[i]
        obj_key = payload['obj_key']
        update_pos_res = self.order.update_pos_order(payload, obj_key, dev_type=dev_type)[1]
        return check_payload_inclusion(update_pos_res, payload)

    def update_Lic(self, dev_type, newvals,add_lic=False):
        """Update License order
           :param device type
           :param values to be updated
        """
        payload = self.order.order.lic_order_data
        GTL = None
        for i in newvals.keys():
            if 'GT_' in newvals[i]:
                GTL = True
            if i == 'po':
                payload['activate']['po'] = newvals[i]
            else:
                payload[i] = newvals[i]
        if add_lic:
            licenses = payload['entitlements'][0]['licenses']
            new_lic = copy.deepcopy(licenses[0])
            new_lic['subscription_key'] = 'NEW' + new_lic['subscription_key']
            new_lic['device_serial_number'] = 'NEW' + new_lic['device_serial_number']
            licenses.append(new_lic)
        obj_key = payload['obj_key']
        update_pos_res = self.order.update_lic_order(payload, obj_key, dev_type=dev_type)[1]
        if GTL:
            return True
        return check_payload_inclusion(update_pos_res, payload)

    def traverseOaas(self, node_list, dev, printall= False):
        this_node = {k: dev[k] for k in dev.keys() - {'child_devices'}}
        node_list.append(this_node)
        if 'child_devices' in dev:
            for child in dev['child_devices']:
                self.traverseOaas(node_list, child)
        if printall:
            log.info(f"Serial numbers of the device config:  ")
            position = 0
            for node in node_list:
                log.info(f"Preorder position in the device config: {position} : {node['serial_number']} ")
                position += 1
        return node_list
