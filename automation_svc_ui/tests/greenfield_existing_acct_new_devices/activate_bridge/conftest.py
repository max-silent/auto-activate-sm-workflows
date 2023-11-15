import logging

import pytest

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.local_libs.activate_bridge.activate_bridge_utils import ActivateBridgeUtils
from hpe_glcp_automation_lib.libs.abridge.helpers.abridge_device_helper import ActivateBridgeHelper

log = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def post_bridge_login_user(init_bridge_object):
    """
    Fixture for performing a bridge login for user 1.
    Returns:
        dict: The response data of the bridge login request for user 1.
    """
    credential_0 = ExistingUserAcctDevices.test_data['harness_activate_bridge']['bridge_credential_user0']
    credential_1 = ExistingUserAcctDevices.test_data['harness_activate_bridge']['bridge_credential_password0']
    create_test = ActivateBridgeUtils()
    return create_test.create_bridge_login(credential_0, credential_1, init_bridge_object=init_bridge_object)


@pytest.fixture(scope="function")
def post_bridge_login_user2(init_bridge_object_user2):
    """
    Fixture for performing a bridge login for user 2.

    This fixture creates a bridge login for user 2 using the specified credentials and the initialized ActivateBridgeHelper object
    init_bridge_object (ActivateBridgeHelper): An instance of the ActivateBridgeHelper class.
    Returns:
        dict: The response data of the bridge login request for user 2.
    """
    credential_0 = ExistingUserAcctDevices.test_data['harness_activate_bridge']['bridge_credential_user1']
    credential_1 = ExistingUserAcctDevices.test_data['harness_activate_bridge']['bridge_credential_password1']
    create_test = ActivateBridgeUtils()
    return create_test.create_bridge_login(credential_0, credential_1, init_bridge_object=init_bridge_object_user2)


@pytest.fixture(scope="function")
def init_bridge_object():
    """
    Fixture for initializing the ActivateBridgeHelper object.
    :return: ActivateBridgeHelper: An instance of the ActivateBridgeHelper class.
    """
    host = ExistingUserAcctDevices.ccs_activate_v1_device_url
    credential_0 = ExistingUserAcctDevices.test_data['harness_activate_bridge']['bridge_credential_user0']
    credential_1 = ExistingUserAcctDevices.test_data['harness_activate_bridge']['bridge_credential_password0']
    return ActivateBridgeHelper(host, credential_0, credential_1)


@pytest.fixture(scope="function")
def init_bridge_object_user2():
    """
    Fixture for initializing the ActivateBridgeHelper object.
    :return: ActivateBridgeHelper: An instance of the ActivateBridgeHelper class.
    """
    host = ExistingUserAcctDevices.ccs_activate_v1_device_url
    credential_0 = ExistingUserAcctDevices.test_data['harness_activate_bridge']['bridge_credential_user1']
    credential_1 = ExistingUserAcctDevices.test_data['harness_activate_bridge']['bridge_credential_password1']
    return ActivateBridgeHelper(host, credential_0, credential_1)
