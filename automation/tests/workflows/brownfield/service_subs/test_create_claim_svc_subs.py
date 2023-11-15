import logging
import time
import pytest
import allure
from automation.tests.workflows.brownfield.service_subs.create_claim_svc_subs import WfCreateSvcSubs
from automation.local_libs.humio.humio_logs import HumioLogLocalHelper
from automation.conftest import ExistingUserAcctDevices
from automation.conftest import SkipTest

log = logging.getLogger(__name__)

@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield Service Subscriptions")
@pytest.mark.Plv
class TestServiceSubscription:
    @pytest.mark.testrail(id=1277316)
    @pytest.mark.order(1)
    @pytest.mark.Regression
    def test_create_vm_backup_svc_subs_c1277316(self, create_vm_backup_svc_subs):
        """
        Create service subscription
        """
        SkipTest.skip_if_triton_lite()
        assert create_vm_backup_svc_subs


    @pytest.mark.testrail(id=1277316)
    @pytest.mark.order(2)
    @pytest.mark.Regression
    def test_add_lic_acct_c1277316(self, create_vm_backup_svc_subs,
                          svc_subs_sa_user_login_load_account):
        """
        Add service subscription to account
        """
        SkipTest.skip_if_triton_lite()
        create_test = WfCreateSvcSubs()
        lic_key, lic_quote = create_vm_backup_svc_subs
        assert create_test.add_lic_to_account(lic_key, svc_subs_sa_user_login_load_account)


    @pytest.mark.testrail(id=1277318)
    @pytest.mark.order(3)
    @pytest.mark.Regression
    def test_sm_app_subs_info_acid_existing_app_c1277318(self,
                                                         create_vm_backup_svc_subs,
                                                         svc_subs_sa_user_login_load_account):
        """
        Make app api call to verify service subscription for app instance
        """
        SkipTest.skip_if_triton_lite()
        create_test = WfCreateSvcSubs()
        app_id = ExistingUserAcctDevices.test_data["brnf_service_subs_existing_app_id"]
        assert create_test.sm_app_subs_info_acid(create_vm_backup_svc_subs,
                                                 svc_subs_sa_user_login_load_account,
                                                 app_id)


    @pytest.mark.testrail(id=1277318)
    @pytest.mark.order(4)
    @pytest.mark.Regression
    def test_prov_app_svc_subs_c1277318(self, svc_subs_sa_user_login_load_account):
        """
        Provision new application instance
        """
        SkipTest.skip_if_triton_lite()
        time.sleep(10)
        create_test = WfCreateSvcSubs()
        assert create_test.wf_prov_app_svc_subs(svc_subs_sa_user_login_load_account)


    @pytest.mark.testrail(id=1277318)
    @pytest.mark.order(5)
    @pytest.mark.Regression
    def test_sm_app_subs_info_acid_new_app_c1277318(self, create_vm_backup_svc_subs,
                                           svc_subs_sa_user_login_load_account):
        """
        Make app api call to verify service subscription for new provisioned app instance
        """
        SkipTest.skip_if_triton_lite()
        time.sleep(10)
        create_test = WfCreateSvcSubs()
        app_id = ExistingUserAcctDevices.test_data["brnf_service_subs_new_app_id"]
        assert create_test.sm_app_subs_info_acid(create_vm_backup_svc_subs,
                                                 svc_subs_sa_user_login_load_account,
                                                 app_id)


    @pytest.mark.testrail(id=1277318)
    @pytest.mark.order(6)
    @pytest.mark.Regression
    def test_unprov_app_svc_subs_c1277318(self, svc_subs_sa_user_login_load_account):
        """
        Unprovision the new application instance for the next run
        """
        time.sleep(10)
        SkipTest.skip_if_triton_lite()
        create_test = WfCreateSvcSubs()
        assert create_test.wf_unprov_app_svc_subs(svc_subs_sa_user_login_load_account)


    @pytest.mark.testrail(id=1292747)
    @pytest.mark.order(7)
    @pytest.mark.Regression
    def test_create_vm_backup_svc_subs_expired_lic_c1292747(self, create_vm_backup_svc_subs_expired):
        """
        Create service subscription
        """
        SkipTest.skip_if_triton_lite()
        assert create_vm_backup_svc_subs_expired


    @pytest.mark.testrail(id=1292747)
    @pytest.mark.order(8)
    @pytest.mark.Regression
    def test_add_lic_acct_expired_lic_c1292747(self, create_vm_backup_svc_subs_expired,
                          svc_subs_sa_user_login_load_account):
        """
        Add service subscription to account
        """
        SkipTest.skip_if_triton_lite()
        create_test = WfCreateSvcSubs()
        lic_key, lic_quote = create_vm_backup_svc_subs_expired
        assert create_test.add_lic_to_account(lic_key, svc_subs_sa_user_login_load_account)


    @pytest.mark.testrail(id=1292747)
    @pytest.mark.order(9)
    @pytest.mark.Regression
    # NEGATIVE TEST
    def test_sm_app_subs_info_acid_existing_app_expired_lic_c1292747(self,
                                                                     create_vm_backup_svc_subs_expired,
                                                                     svc_subs_sa_user_login_load_account):
        """
        Make app api call to verify service subscription for app instance
        """
        SkipTest.skip_if_triton_lite()
        create_test = WfCreateSvcSubs()
        app_id = ExistingUserAcctDevices.test_data["brnf_service_subs_existing_app_id"]
        assert ((False == create_test.sm_app_subs_info_acid(create_vm_backup_svc_subs_expired,
                                                 svc_subs_sa_user_login_load_account, app_id)),
                        "Negative test, expired lic should not have provisioned apps.\n")

    @pytest.mark.testrail(id=1277316)
    @pytest.mark.order(10)
    @pytest.mark.Regression
    def test_humio_msg_svc_subscription_event_c1277316(self, create_vm_backup_svc_subs):
        """
         ===== Claim service subscription key in an account ======
         1. In humio logs search for claim request and published subscription event
         2. Search for "Received post subscription claim request"
         3. Search for event published "Successfully published subscription event: operation=SUBSCRIPTION_UPDATED"
        """
        lic_key, lic_quote = create_vm_backup_svc_subs

        search_str = "\"Received post subscription claim request:\" AND {}".format(lic_key)
        log.info("searching for transaction_id with string as {} in logs".format(search_str))
        create_test = HumioLogLocalHelper()
        transaction_id = create_test.get_subs_mgmt_event_transaction_id(search_str)
        result_search_str = "\"Successfully published subscription event: operation=SUBSCRIPTION_UPDATED\" " \
                            "AND {} " \
                            "AND {}".format(lic_key, transaction_id)
        log.info("searching for logs with string as: {}".format(search_str))
        assert create_test.humio_query_logs(result_search_str)
