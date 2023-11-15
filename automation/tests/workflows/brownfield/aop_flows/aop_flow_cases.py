import logging
import re
import pytest
import copy
import time
from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway

from automation.conftest import ExistingUserAcctDevices
from automation.tests.workflows.brownfield.aop_flows.aop_flow_defs import (
    aopFlows
)
from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway
from hpe_glcp_automation_lib.libs.adi.app_api.adi_app_api import ActivateInventory

log = logging.getLogger(__name__)

end_username = "aop_endusername_harness1"
unv_end_username = "unv_aop_endusername_harness1"

def compare_SN_list(l1, l2):
    if len(l1) != len(l2):
        log.info(f"Mismatched list lengths")
        return False
    for i in range(len( l1 )):
        if l1[i] != l2[i]:
            log.info(f"Mismatched at {l1[i]} and {l2[i]}")
            return False
    return True

def init_global_test_Data():
    pytest.globalvar['runtime_testdata']['end_username'] = end_username
    pytest.globalvar['runtime_testdata']['unv_end_username'] = unv_end_username
    pytest.globalvar['runtime_testdata']['manufactured'] = {}
    pytest.globalvar['runtime_testdata']['Pos'] = {}
    pytest.globalvar['runtime_testdata']['Sds'] = {}
    pytest.globalvar['runtime_testdata']['Lic'] = {'STORAGE':{},'COMPUTE':{}, 'NETWORK':{}}

def Create_oaas_devices(dev_type=None, part_category=None, MinParams=False):
    create_test = aopFlows()
    res, part = create_test.create_oaas_of_type(dev_type)

def Create_devices(dev_type=None, part_category=None, MinParams=False):
    create_test = aopFlows()
    mac = create_test.create_device_of_type(dev_type, part_category=part_category, MinParams=MinParams)[0][1]
    pytest.globalvar['runtime_testdata']['manufactured'][dev_type] = create_test
    if re.match("(\w\w:){5}(\w\w)",mac):
        return True
    else:
        return False

def Update_manufacture(dev_type, newvals):
    create_test = pytest.globalvar['runtime_testdata']['manufactured'][dev_type]
    return create_test.update_manufacturing(dev_type, newvals)

def Update_manufacture_adchild(dev_type, newvals):
    create_test = pytest.globalvar['runtime_testdata']['manufactured'][dev_type]
    return create_test.update_manufacturing_addchild(dev_type)

def Create_Pos(dev_type,MinParams=False,end_username=False):
    create_test = aopFlows(end_username=end_username)
    device,part = create_test.create_device_of_type(dev_type, MinParams=MinParams)
    pos =  create_test.order.create_pos_order(part=part)
    pytest.globalvar['runtime_testdata']['Pos'][dev_type] = create_test
    return pos

def Update_Pos(dev_type,newvals):
    create_test = pytest.globalvar['runtime_testdata']['Pos'][dev_type]
    return create_test.update_Pos(dev_type, newvals)

def Create_Sds(dev_type,MinParams=False,end_username=False):
    create_test = aopFlows(end_username=end_username)
    device,part = create_test.create_device_of_type(dev_type, MinParams=MinParams)
    sds = create_test.order.create_sds_order(part=part)
    pytest.globalvar['runtime_testdata']['Sds'][dev_type] = create_test
    return sds

def Update_Sds(dev_type,newvals):
    create_test = pytest.globalvar['runtime_testdata']['Sds'][dev_type]
    return create_test.update_Sds(dev_type, newvals)

def Create_License(dev_type,MinParams=False,end_username=False, part_category=None):
    create_test = aopFlows(end_username=end_username)
    device,part = create_test.create_device_of_type(dev_type, MinParams=MinParams,part_category=part_category)
    lic = create_test.order.create_lic_order(part=part)
    pytest.globalvar['runtime_testdata']['Lic'][dev_type] = create_test
    return lic

def Update_License(dev_type,newvals, add_lic=False):
    create_test = pytest.globalvar['runtime_testdata']['Lic'][dev_type]
    if add_lic:
        return create_test.update_Lic(dev_type, newvals, add_lic=add_lic)
    return create_test.update_Lic(dev_type, newvals)

def Create_oaas():
    create_test = aopFlows()
    create_test.create_oaas_of_type('STORAGE')

def Create_oaas_claim(dev_type=None, part_category=None):
    create_test = aopFlows()
    res, part = create_test.create_oaas_of_type(dev_type)
    pytest.globalvar['runtime_testdata']['create_test'] = create_test
    pytest.globalvar['runtime_testdata']['oaas_dev_for_patch'] = res
    lic = create_test.order.create_lic_order(part=part, serial=res['serial_number'])
    create_test.adi.claim_device_app_api(dev_type, res['serial_number'], create_test.pcid, create_test.username, part_num=part, entitlement_id=lic,
                                         application_customer_id=create_test.acid)
    return True

def Oaas_devices_add_node():
     ct = pytest.globalvar['runtime_testdata']['create_test']
     dev = pytest.globalvar['runtime_testdata']['oaas_dev_for_patch']
     new_node = {k: dev[k] for k in dev.keys() - {'child_devices', 'eth_mac','activate_customer_id' ,'platform_customer_id', 'mfg_date'}}
     new_node['serial_number'] = 'ADDED_' + new_node['serial_number']
     new_node['obj_key'] = 'ADDED_' + new_node['obj_key']
     log.info(f"==================Serial numbers in device config before adding the node is:================")
     node_list = ct.traverseOaas([], dev)
     serial_list_before = [x['serial_number'] for x in node_list]
     log.info(serial_list_before)
     serial_list_expected_after = copy.deepcopy(serial_list_before)
     serial_list_expected_after.insert(5, new_node['serial_number'])
     fifth_node = node_list[4]
     parent_serial = fifth_node['serial_number']
     parent_part = fifth_node['part_number']
     res = ct.adi.add_devconfig_node(ct.pcid, ct.username, ct.acid, dev['serial_number'], dev['part_number'], parent_serial, parent_part, new_node)
     if "ERROR" in res.text:
         log.error(res.text)
         return False
     get_res = ct.adi.get_devconfig_node(ct.pcid, ct.username, ct.acid, dev['serial_number'], dev['part_number'])
     dev_after = get_res.json()
     node_list_after = ct.traverseOaas([], dev_after)
     serial_list_real_after = [x['serial_number'] for x in node_list_after]
     log.info(f"==================Serial numbers in device config after adding the node (Expected) is:================")
     log.info(serial_list_expected_after)
     log.info(f"==================Serial numbers in device config after adding the node (Real) is:================")
     log.info(serial_list_real_after)
     result = compare_SN_list(serial_list_expected_after, serial_list_real_after)
     #save the modified device for next modification use
     pytest.globalvar['runtime_testdata']['oaas_dev_for_patch'] = dev_after
     return result

def Oaas_devices_rem_node():
     ct = pytest.globalvar['runtime_testdata']['create_test']
     dev = pytest.globalvar['runtime_testdata']['oaas_dev_for_patch']
     log.info(f"==================Serial numbers in device config before removing the node is:================")
     node_list = ct.traverseOaas([], dev)
     serial_list_before = [x['serial_number'] for x in node_list]
     log.info(serial_list_before)
     serial_list_expected_after = copy.deepcopy(serial_list_before)
     del serial_list_expected_after[4]
     fifth_node = node_list[4]
     parent_serial = fifth_node['serial_number']
     parent_part = fifth_node['part_number']
     res = ct.adi.remove_devconfig_node(ct.pcid, ct.username, ct.acid, dev['serial_number'], dev['part_number'], parent_serial, parent_part)
     if "ERROR" in res.text:
         log.error(res.text)
         return False
     get_res = ct.adi.get_devconfig_node(ct.pcid, ct.username, ct.acid, dev['serial_number'], dev['part_number'])
     dev_after = get_res.json()
     node_list_after = ct.traverseOaas([], dev_after)
     serial_list_real_after = [x['serial_number'] for x in node_list_after]
     log.info(f"==================Serial numbers in device config after removing the node (Expected) is:================")
     log.info(serial_list_expected_after)
     log.info(f"==================Serial numbers in device config after removing the node (Real) is:================")
     log.info(serial_list_real_after)
     result = compare_SN_list(serial_list_expected_after, serial_list_real_after)
     #save the modified device for next modification use
     pytest.globalvar['runtime_testdata']['oaas_dev_for_patch'] = dev_after
     return result

def Oaas_devices_replace_node():
     ct = pytest.globalvar['runtime_testdata']['create_test']
     dev = pytest.globalvar['runtime_testdata']['oaas_dev_for_patch']
     new_node = {k: dev[k] for k in dev.keys() - {'child_devices', 'eth_mac','activate_customer_id' ,'platform_customer_id', 'mfg_date'}}
     new_node['serial_number'] = 'REPLACE_' + new_node['serial_number']
     new_node['obj_key'] = 'REPLACE_' + new_node['obj_key']
     log.info(f"==================Serial numbers in device config before replacing the node is:================")
     node_list = ct.traverseOaas([], dev)
     serial_list_before = [x['serial_number'] for x in node_list]
     log.info(serial_list_before)
     serial_list_expected_after = copy.deepcopy(serial_list_before)
     serial_list_expected_after[4] = new_node['serial_number']
     fifth_node = node_list[4]
     parent_serial = fifth_node['serial_number']
     parent_part = fifth_node['part_number']
     res = ct.adi.replace_devconfig_node(ct.pcid, ct.username, ct.acid, dev['serial_number'], dev['part_number'], parent_serial, parent_part, new_node)
     if "ERROR" in res.text:
         log.error(res.text)
         return False
     get_res = ct.adi.get_devconfig_node(ct.pcid, ct.username, ct.acid, dev['serial_number'], dev['part_number'])
     dev_after = get_res.json()
     node_list_after = ct.traverseOaas([], dev_after)
     serial_list_real_after = [x['serial_number'] for x in node_list_after]
     log.info(f"==================Serial numbers in device config after replacing the node (Expected) is:================")
     log.info(serial_list_expected_after)
     log.info(f"==================Serial numbers in device config after replacing the node (Real) is:================")
     log.info(serial_list_real_after)
     result = compare_SN_list(serial_list_expected_after, serial_list_real_after)
     #save the modified device for next modification use
     pytest.globalvar['runtime_testdata']['oaas_dev_for_patch'] = dev_after
     return result

def create_bulk_devices():
    create_test = aopFlows()
    for i in range(2):
        device,part = create_test.create_device_of_type(device_type="STORAGE", part_category="STORAGE", baas=True)
        pos =  create_test.order.create_pos_order(part=part,end_username="Test_varg_alias618")
    return pos

def Create_devices(dev_type=None, part_category=None, MinParams=False):
    create_test = aopFlows()
    mac = create_test.create_device_of_type(dev_type, part_category=part_category, MinParams=MinParams)[0][1]
    pytest.globalvar['runtime_testdata']['manufactured'][dev_type] = create_test
    if re.match("(\w\w:){5}(\w\w)",mac):
        return True
    else:
        return False

def Oaas_create_delete():
    create_test = aopFlows()
    res, part = create_test.create_oaas_of_type('STORAGE')
    obj_key = res['obj_key']
    serial_number = res['serial_number']
    create_test.order.order.delete_oaas_dev(serial_number)
    for i in range(5):
        time.sleep(2)
        get_dev = create_test.order.order.get_oaas_by_objkey(obj_key)
        if not get_dev:
            return True
    log.info("Delete device failed")
    return False
