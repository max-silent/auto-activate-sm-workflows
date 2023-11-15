import logging
import time

from automation_svc_ui.conftest import ExistingUserAcctDevices
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils
from hpe_glcp_automation_lib.libs.sm.app_api.sm_app_api import SubscriptionManagementApp
from hpe_glcp_automation_lib.libs.sm.helpers.sm_create_orders_helper import NewSubsOrder
# from hpe_glcp_automation_lib.libs.sm.helpers.sm_payload_constants import SmInputPayload

log = logging.getLogger(__name__)


class WfCreateSvcSubs:
    def __init__(self):
        log.info("Initialize WfCreateSvcSubs")
        """Step #0: Create Test constants and variables like sn, mac, system under test, , device_type"""
        # init_subs_constants = SmInputPayload()
        self.end_username = RandomGenUtils.random_string_of_chars(7)
        self.app_api_hostname = ExistingUserAcctDevices.app_api_hostname

    def create_svc_subs(self, subs_type):
        """Step # 1: Create 1 create_svc_subs for VM backup"""
        aop_sso_url = ExistingUserAcctDevices.test_data["sso_host"]
        aop_client = ExistingUserAcctDevices.test_data["brnf_service_subs_api_client_id"]
        aop_secret = ExistingUserAcctDevices.test_data["brnf_service_subs_api_client_secret"]
        create_order = NewSubsOrder(self.end_username,
                                    self.app_api_hostname,
                                    aop_sso_url,
                                    aop_client,
                                    aop_secret)
        lic_key, quote = create_order.create_svc_order(subs_type)
        if lic_key is not None:
            return lic_key, quote
        else:
            return False

    def create_svc_subs_expired(self, subs_type):
        """Step # 1: Create 1 create_svc_subs for VM backup"""
        aop_sso_url = ExistingUserAcctDevices.test_data["sso_host"]
        aop_client = ExistingUserAcctDevices.test_data["brnf_service_subs_api_client_id"]
        aop_secret = ExistingUserAcctDevices.test_data["brnf_service_subs_api_client_secret"]
        create_order = NewSubsOrder(self.end_username,
                                    self.app_api_hostname,
                                    aop_sso_url,
                                    aop_client,
                                    aop_secret)
        lic_key, quote = create_order.create_svc_order(subs_type)
        lic_key_update, lic_quote_updated = create_order.update_subs_order_to_expired(quote)
        if lic_key != lic_key_update or quote != lic_quote_updated:
            log.error("Wrong quote updated, orig quote, {}, updated quote: {}".format(quote, lic_quote_updated))
        if lic_key is not None:
            return lic_key, quote
        else:
            return False

    def add_lic_to_account(self,
                           lic_key,
                           svc_subs_sa_user_login_load_account):
        """Step # 1: add svc_subs for VM backup in customer account"""
        resp = svc_subs_sa_user_login_load_account.sm_add_lic(lic_key)
        if resp:
            return True
        else:
            return False

    @staticmethod
    def sm_app_subs_info_acid(create_vm_backup_svc_subs,
                              svc_subs_sa_user_login_load_account,
                              application_id):
        """Step # 2: find svc_subs for VM backup in customer account using app api call"""
        app_sm = SubscriptionManagementApp(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["brnf_service_subs_api_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["brnf_service_subs_api_client_secret"],
        )
        lic_key, lic_quote = create_vm_backup_svc_subs
        params = {"subscription_key": lic_key}
        log.info(svc_subs_sa_user_login_load_account)
        provisioned_apps = svc_subs_sa_user_login_load_account.get_provisions()
        for app in provisioned_apps["provisions"]:
            if app["application_id"] == application_id:
                sm_app_subs_by_pcid = app_sm.get_sm_app_subscription_assign_app_instance_by_acid_pcid(
                    app["platform_customer_id"],
                    app["application_customer_id"],
                    params
                )
                for sub_key in sm_app_subs_by_pcid['subscriptions']:
                    lic_key, lic_quote = create_vm_backup_svc_subs
                    if sub_key['subscription_key'] == lic_key:
                        log.info("found key in get sm subs assign to app instance by acid, "
                                 "pcid call: {}".format(sub_key['subscription_key']))
                        return True
        return False

    def wf_prov_app_svc_subs(self, new_user_login_load_account):
        """Step #3: Provision application in customer account"""
        prov_app = new_user_login_load_account.provision_application(
            ExistingUserAcctDevices.test_data["brnf_service_subs_new_region"],
            ExistingUserAcctDevices.test_data["brnf_service_subs_new_app_id"],
        )
        log.info(prov_app)
        status = "PROVISIONED"
        prov_status = new_user_login_load_account.wait_for_provision_status(
            prov_app["application_customer_id"], status, iterations=30, delay=12
        )
        log.info(prov_status)
        self.acid = prov_app["application_customer_id"]
        time.sleep(11)
        """adding delay for app provisioning to add application customer id 
        Activate services for auto assignments"""
        if prov_status:
            return prov_app
        else:
            log.error("Not able to provision the application instance")
            return False

    def wf_unprov_app_svc_subs(self, new_user_login_load_account):
        """Step #4: UnProvision application in new signup account"""
        apps = new_user_login_load_account.get_provisions()
        prov_app = ExistingUserAcctDevices.test_data["brnf_service_subs_new_app_id"]
        for app in apps["provisions"]:
            if app['application_id'] == prov_app:
                new_user_login_load_account.delete_application_customer(app['application_customer_id'])
                time.sleep(10)
                break
        apps = new_user_login_load_account.get_provisions()
        log.info(prov_app)
        for app in apps["provisions"]:
            if app['application_id'] == prov_app:
                return False
            return True
