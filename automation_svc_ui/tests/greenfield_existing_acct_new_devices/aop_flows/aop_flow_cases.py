import logging
import re

import pytest

from automation_svc_ui.tests.greenfield_existing_acct_new_devices.aop_flows.aop_flow_defs import aopFlows

log = logging.getLogger(__name__)

end_username = "aop_endusername_harness1"
unv_end_username = "unv_aop_endusername_harness1"


def init_global_test_Data():
    pytest.globalvar["runtime_testdata"]["end_username"] = end_username
    pytest.globalvar["runtime_testdata"]["unv_end_username"] = unv_end_username
    pytest.globalvar["runtime_testdata"]["manufactured"] = {}
    pytest.globalvar["runtime_testdata"]["Pos"] = {}
    pytest.globalvar["runtime_testdata"]["Sds"] = {}
    pytest.globalvar["runtime_testdata"]["Lic"] = {
        "STORAGE": {},
        "COMPUTE": {},
        "NETWORK": {},
    }


def Create_oaas_devices(dev_type=None, part_category=None, MinParams=False):
    create_test = aopFlows()
    res, part = create_test.create_oaas_of_type(dev_type)


def Create_devices(dev_type=None, part_category=None, MinParams=False):
    create_test = aopFlows()
    mac = create_test.create_device_of_type(
        dev_type, part_category=part_category, MinParams=MinParams
    )[0][1]
    pytest.globalvar["runtime_testdata"]["manufactured"][dev_type] = create_test
    if re.match("(\w\w:){5}(\w\w)", mac):
        return True
    else:
        return False


def Update_manufacture(dev_type, newvals):
    create_test = pytest.globalvar["runtime_testdata"]["manufactured"][dev_type]
    return create_test.update_manufacturing(dev_type, newvals)


def Update_manufacture_adchild(dev_type, newvals):
    create_test = pytest.globalvar["runtime_testdata"]["manufactured"][dev_type]
    return create_test.update_manufacturing_addchild(dev_type)


def Create_Pos(dev_type, MinParams=False, end_username=False):
    create_test = aopFlows(end_username=end_username)
    device, part = create_test.create_device_of_type(dev_type, MinParams=MinParams)
    pos = create_test.order.create_pos_order(part=part)
    pytest.globalvar["runtime_testdata"]["Pos"][dev_type] = create_test
    return pos


def Update_Pos(dev_type, newvals):
    create_test = pytest.globalvar["runtime_testdata"]["Pos"][dev_type]
    return create_test.update_Pos(dev_type, newvals)


def Create_Sds(dev_type, MinParams=False, end_username=False):
    create_test = aopFlows(end_username=end_username)
    device, part = create_test.create_device_of_type(dev_type, MinParams=MinParams)
    sds = create_test.order.create_sds_order(part=part)
    pytest.globalvar["runtime_testdata"]["Sds"][dev_type] = create_test
    return sds


def Update_Sds(dev_type, newvals):
    create_test = pytest.globalvar["runtime_testdata"]["Sds"][dev_type]
    return create_test.update_Sds(dev_type, newvals)


def Create_License(dev_type, MinParams=False, end_username=False, part_category=None):
    create_test = aopFlows(end_username=end_username)
    device, part = create_test.create_device_of_type(
        dev_type, MinParams=MinParams, part_category=part_category
    )
    lic = create_test.order.create_lic_order(part=part)
    pytest.globalvar["runtime_testdata"]["Lic"][dev_type] = create_test
    return lic


def Update_License(dev_type, newvals, add_lic=False):
    create_test = pytest.globalvar["runtime_testdata"]["Lic"][dev_type]
    if add_lic:
        return create_test.update_Lic(dev_type, newvals, add_lic=add_lic)
    return create_test.update_Lic(dev_type, newvals)


def Create_oaas():
    create_test = aopFlows()
    create_test.create_oaas_of_type("STORAGE")
