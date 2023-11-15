import logging

import pytest
from automation.conftest import ExistingUserAcctDevices
from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway
from automation.tests.workflows.brownfield.service_subs.create_claim_svc_subs import WfCreateSvcSubs
from automation.conftest import SkipTest
log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def create_vm_backup_svc_subs():
    SkipTest.skip_if_triton_lite()
    create_test = WfCreateSvcSubs()
    subs_test = "VM_BACKUP"
    lic_key, lic_quote = create_test.create_svc_subs(subs_test)
    return lic_key, lic_quote

@pytest.fixture(scope="session")
def create_vm_backup_svc_subs_expired():
    SkipTest.skip_if_triton_lite()
    create_test = WfCreateSvcSubs()
    subs_test = "VM_BACKUP"
    lic_key, lic_quote = create_test.create_svc_subs_expired(subs_test)
    return lic_key, lic_quote


@pytest.fixture(scope="session")
def svc_subs_sa_user_login_load_account():
    SkipTest.skip_if_triton_lite()
    hostname = ExistingUserAcctDevices.login_page_url
    username = ExistingUserAcctDevices.test_data["brnf_service_subs_username"]
    password = ExistingUserAcctDevices.test_data["brnf_service_subs_password"]
    pcid = ExistingUserAcctDevices.test_data["brnf_service_subs_pcid"]
    url = hostname.split("//")[1]
    return UIDoorway(url, username, password, pcid)

