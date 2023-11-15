import datetime
import json
import logging
import os
import time

import pytz

from automation_svc_ui.conftest import ExistingUserAcctDevices, SubscriptionData
from automation_svc_ui.local_libs.activate_devices.manufacture_order_utils import ManufactureDevicesHelper
from automation_svc_ui.local_libs.activate_orders.activate_orders_utils import ActivateOrdersHelper
from automation_svc_ui.local_libs.audit_logs.audit_logs_ui_utils import AuditLogsVerifier, LogsEventType
from automation_svc_ui.local_libs.ui_doorway.ui_doorway_devices_by_api import UiDoorwayDevices
from hpe_glcp_automation_lib.libs.acct_mgmt.helpers.ui_am_create_new_user_new_acct_setup import (
    HlpCreateUserCreateAcct,
)
from hpe_glcp_automation_lib.libs.add.device_calls.device_prov import (
    NetworkStorageComputeDeviceProvisionHelper,
)
from hpe_glcp_automation_lib.libs.adi.app_api.adi_app_api import ActivateInventory
from hpe_glcp_automation_lib.libs.aop.helpers.aop_payload_constants import (
    AOPDeviceConstants,
)
from hpe_glcp_automation_lib.libs.commons.ui.home_page import HomePage
from hpe_glcp_automation_lib.libs.commons.ui.manage_account_page import ManageAccount
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import (
    browser_page,
    browser_stop,
)
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils
from hpe_glcp_automation_lib.libs.sm.app_api.sm_app_api import SubscriptionManagementApp

log = logging.getLogger(__name__)


class WfNewDeviceNewUserSignupCreateAcct:
    def __init__(self):
        log.info("Initialize new_device_new_user_signup_create_acct")
        """Step #0: Create Test constants and variables like sn, mac, system under test, device_category, device_type"""
        self.end_username = RandomGenUtils.random_string_of_chars(7)
        self.cluster = ExistingUserAcctDevices.login_page_url
        self.email_IdRand = "hcloud203+" + str(self.end_username) + "@gmail.com"
        self.app_api_hostname = ExistingUserAcctDevices.app_api_hostname
        self.dev_constants = AOPDeviceConstants.generate_devices_details()
        self.gmail_creds = (
            ExistingUserAcctDevices.test_data["gmail_username"],
            ExistingUserAcctDevices.test_data["gmail_password"],
        )
        self.acid = ""

    def new_nw_device_fn(self, device_type):
        """Step # 1: Create 1 iap devices"""
        aop_client = ExistingUserAcctDevices.test_data["gf_nw_api_client_id"]
        aop_secret = ExistingUserAcctDevices.test_data["gf_nw_api_client_secret"]
        return ManufactureDevicesHelper(aop_client, aop_secret, self.dev_constants) \
            .create_device_of_type(device_type, end_username=self.end_username)

    def wf_sm_audit_log_info(
            self, browser_instance, storage_state_path, devices_details, user_login_load_account
    ) -> bool:
        """Step #17: Check subscription for device's serial number."""
        test_name = (
            os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        )
        context, page = browser_page(browser_instance, storage_state_path)

        try:
            HomePage(
                page, self.cluster
            ).open().wait_for_loaded_state().nav_bar.navigate_to_manage()
            audit_logs = ManageAccount(page, self.cluster).open_audit_logs().wait_for_loaded_table()

            # Get details of first device of each type in devices_details dictionaries
            for device in ActivateOrdersHelper.get_dev_details_per_dev_type(devices_details):
                device_type = device["device_type"]
                part_no = self.dev_constants["DEFAULT_PART_MAP"][device_type]
                subscr_key = UiDoorwayDevices.get_subscription_key(device_type, device["serial_no"], part_no,
                                                                   user_login_load_account)
                AuditLogsVerifier.check_device_events(audit_logs, [LogsEventType.SUBSCRIPTION], device,
                                                      subscr_key=subscr_key)

            return True

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_new_user_acct_fn(self, browser):
        """Step # 2: signup new user and create new account"""
        new_ac = HlpCreateUserCreateAcct(self.gmail_creds)

        test_name = os.environ.get("PYTEST_CURRENT_TEST", "").split(":")[-1].split(" ")[0]
        context, page = browser_page(browser)

        try:
            customer_details = new_ac.svc_new_user_signup(
                page, self.cluster, self.email_IdRand, self.end_username
            )
            if customer_details:
                log.info("customer details: {}".format(customer_details))
                return customer_details
            else:
                log.error("not able to signup a new customer")
                return False

        except Exception as ex:
            log.error(f"Error:\n{ex}")
            return False

        finally:
            browser_stop(context, page, test_name)

    def wf_prov_app_fn(self, new_user_login_load_account):
        """Step #3: Provision application in new signup account"""
        prov_app = new_user_login_load_account.provision_application(
            ExistingUserAcctDevices.test_data["gf_nw_app_region"],
            ExistingUserAcctDevices.test_data["gf_nw_app_id"],
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

    @staticmethod
    def wf_create_activate_verified_alias(tac_ui_doorway, setup_info):
        """Step #4: add end_username (alias) to the customer"""
        customer_name = setup_info.user.split("@")[0].split("+")[1]
        customer_alias_created = tac_ui_doorway.add_cm_activate_alias(customer_name, setup_info.pcid)
        if customer_alias_created.get("response"):
            return True
        else:
            log.error("Not able to create customer alias.")
            return False

    @staticmethod
    def verify_device_claimed(device_order, ui_doorway):
        devices = claimed_device = None
        start_time = time.time()
        while not devices and (time.time() < start_time + 15):
            time.sleep(2)
            devices = ui_doorway.list_devices().get("devices")
        assert devices, "Failed! No devices were claimed by Customers' Alias"
        for device in devices:
            if device.get("serial_number") == device_order.get("serial_no"):
                claimed_device = device
                break
        assert claimed_device, f"Failure! Device was not claimed automatically."

    @classmethod
    def wf_assign_subs_eval(cls, device_type, ordered_devices, new_user_login_load_account):
        subscr_data = SubscriptionData(device_type)
        subs_type = subscr_data.subscription_type
        part_number = subscr_data.part_number
        license_list = dict()
        try:
            for i in range(1, 20):
                license_list = new_user_login_load_account.get_licenses()
                if len(license_list["subscriptions"]) < 14:
                    log.info(f"Number of active subscriptions: {len(license_list['subscriptions'])}")
                    time.sleep(10)
                if len(license_list["subscriptions"]) >= 14:
                    log.info(f"Number of active subscriptions: {len(license_list['subscriptions'])}")
                    break
        except Exception as e:
            log.error(e)
            return False
        log.debug("found license for device {}: {}".format(subs_type, license_list))
        license_key = None
        for subscription in license_list["subscriptions"]:  # top loop
            if subscription["subscription_type"] == subs_type == "CENTRAL_AP":
                if subscription["license_tier"] == "ADVANCED":
                    subs_details = subscription
                    if cls._is_actual_subs(subs_details):
                        license_key = subs_details["subscription_key"]
                        log.info(f"Found suitable subscription: {license_key}")
                        break  # exit from nested loop 2 (AP)
            elif subscription["subscription_type"] == subs_type == "CENTRAL_SWITCH":
                if subscription["license_tier"] == "ADVANCED" and \
                        subscription["subscription_tier_description"] in [
                    "Advanced-Switch-62xx/29xx",
                    "Advanced-Switch-6200/29xx"
                ]:
                    subs_details = subscription
                    if cls._is_actual_subs(subs_details):
                        license_key = subs_details["subscription_key"]
                        log.info(f"Found suitable subscription: {license_key}")
                        break  # exit from nested loop 2 (SW)
            elif subscription["subscription_type"] == subs_type == "CENTRAL_GW":
                if subscription["license_tier"] == "ADVANCED" and \
                        subscription["subscription_tier_description"] in [
                    "Advance-70XX",
                    "Advanced-70xx/90xx"
                ]:
                    subs_details = subscription
                    if cls._is_actual_subs(subs_details):
                        license_key = subs_details["subscription_key"]
                        log.info(f"Found suitable subscription: {license_key}")
                        break  # exit from nested loop 2 (GW)
        if not license_key:
            log.error("license key not found.")
            return False
        device_license = []
        time.sleep(3)
        try:
            for idx in range(0, len(ordered_devices)):
                device_license = [
                    (
                        ordered_devices["device_" + device_type + str(idx)][
                            "serial_no"
                        ],
                        license_key,
                    )
                ]
        except Exception as e:
            log.warning(e)
        time.sleep(11)
        try:
            for index in range(3):
                resp = new_user_login_load_account.assign_license_to_devices(
                    device_license, device_type, part_number
                )
                if resp[0]["status"] == "SUCCESS":
                    log.info(
                        "license response for device_type: {}, {}".format(
                            device_type, resp
                        )
                    )
                    return True
                time.sleep(5)
        except Exception as e:
            log.error(f"not able to license the device_type {device_type}. Error: {e}")
            return False

    @staticmethod
    def wf_adi_get_devices_by_acid(new_user_login_load_account):
        app_adi = ActivateInventory(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["gf_nw_api_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["gf_nw_api_client_secret"],
        )
        log.info(new_user_login_load_account)
        provisioned_apps = new_user_login_load_account.get_provisions()
        for app in provisioned_apps["provisions"]:
            if app["provision_status"] == "PROVISIONED":
                app_cust_id = app["application_customer_id"]
                device_by_acid_list = app_adi.get_devices_by_acid(
                    application_customer_id=app_cust_id
                )
                device_list = json.loads(device_by_acid_list.content)
                if device_list.get("error_code"):
                    log.error(f"Error code in response: '{device_list['error_code']}'.")
                    error_message = device_list.get("message")
                    if error_message:
                        log.error(f"Error message: '{error_message}'.")
                    return False
                if len(device_list.get("devices", [])) == 3:
                    log.info(
                        f'"subscriptions list by device_by_acid_list: {len(device_list["devices"])}"'
                    )
                    return True
        log.error("Not able to get expected device_by_acid_list.")
        return False

    @staticmethod
    def wf_adi_get_devices_by_pcid(new_user_login_load_account):
        app_adi = ActivateInventory(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["gf_nw_api_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["gf_nw_api_client_secret"],
        )
        log.info(new_user_login_load_account)
        provisioned_apps = new_user_login_load_account.get_provisions()
        for app in provisioned_apps["provisions"]:
            if app["provision_status"] == "PROVISIONED":
                platform_cust_id = app["platform_customer_id"]
                device_by_pcid_list = app_adi.get_devices_by_pcid(
                    platform_customer_id=platform_cust_id
                )
                device_list = json.loads(device_by_pcid_list.content)
                if len(device_list["devices"]) == 3:
                    log.info(
                        f'"subscriptions list by device_by_pcid_list: {len(device_list["devices"])}"'
                    )
                    return True
                else:
                    log.error("not able to run device_by_pcid_list")
                    return False

    @staticmethod
    def wf_sm_app_subscription_info_acid(new_user_login_load_account):
        app_sm = SubscriptionManagementApp(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["gf_nw_api_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["gf_nw_api_client_secret"],
        )
        log.info(new_user_login_load_account)
        provisioned_apps = new_user_login_load_account.get_provisions()
        for app in provisioned_apps["provisions"]:
            if app["provision_status"] == "PROVISIONED":
                app_cust_id = app["application_customer_id"]
                platform_cust_id = app["platform_customer_id"]
                sm_app_subs_by_acid = app_sm.get_sm_app_subscription_devices(
                    platform_cust_id, app_cust_id
                )
                subscr_assignments = sm_app_subs_by_acid["subscription_assignments"]
                if len(subscr_assignments) == 3:
                    log.info(
                        f"subscriptions list by sm_app_subs_by_acid: {sm_app_subs_by_acid}"
                    )
                    return True
                else:
                    log.error(
                        f"unexpected count of subscription assignments found: {len(subscr_assignments)}"
                    )
                    log.error(subscr_assignments)
                    return False

    @staticmethod
    def wf_sm_app_subscription_info_pcid(new_user_login_load_account):
        app_sm = SubscriptionManagementApp(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["gf_nw_api_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["gf_nw_api_client_secret"],
        )
        log.info(new_user_login_load_account)
        provisioned_apps = new_user_login_load_account.get_provisions()
        for app in provisioned_apps["provisions"]:
            if app["provision_status"] == "PROVISIONED":
                platform_cust_id = app["platform_customer_id"]
                sm_app_subs_by_pcid = app_sm.get_sm_app_subscription_info_pcid(
                    platform_cust_id
                )
                if len(sm_app_subs_by_pcid["subscriptions"]) >= 14:
                    log.info(
                        f'"subscriptions list by sm_app_subs_by_pcid: {0}"'.format(
                            sm_app_subs_by_pcid
                        )
                    )
                    return True
                else:
                    log.error("not able to run sm_app_subs_by_pcid")
                    return False

    def grnf_sa_nw_new_device_prov(self, ordered_devices, device_type):
        serial_number = ordered_devices[f"device_{device_type}0"]["serial_no"]
        mac_address = ordered_devices[f"device_{device_type}0"]["mac"]
        part_number = self.dev_constants["DEFAULT_PART_MAP"][device_type]
        certs = ExistingUserAcctDevices.iap_certs
        aruba_device_url = ExistingUserAcctDevices.aruba_device_url
        cluster_device_url = ExistingUserAcctDevices.ccs_activate_v1_device_url
        make_add_iap_device_call = NetworkStorageComputeDeviceProvisionHelper(
            cluster_device_url,
            serial_number,
            part_number,
            device_type,
            certs,
            aruba_device_url=aruba_device_url,
            mac_address=mac_address,
        )
        return make_add_iap_device_call.iap_add_call_fn()

    def grnf_device_app_unassignment(self, ordered_device, ui_doorway):
        devices = [
            {
                "serial_number": ordered_device["serial_no"],
                "device_type": ordered_device["device_type"],
                "part_number": self.dev_constants["DEFAULT_PART_MAP"][ordered_device["device_type"]]
            }
        ]
        return ui_doorway.unassign_devices_from_app_in_activate_inventory(devices)

    @staticmethod
    def verify_device_not_claimed(device_order, ui_doorway):
        devices = claimed_device = None
        start_time = time.time()
        while not devices and (time.time() < start_time + 15):
            time.sleep(2)
            devices = ui_doorway.list_devices().get("devices")
        for device in devices:
            if device.get("serial_number") == device_order.get("serial_no"):
                claimed_device = device
                break
        assert not claimed_device, \
            f"Failure! Device was claimed. Expected behaviour - device was not claimed by current account"

    @staticmethod
    def verify_eval_subs(ui_doorway):
        app_sm = SubscriptionManagementApp(
            host=ExistingUserAcctDevices.app_api_hostname,
            sso_host=ExistingUserAcctDevices.sso_hostname,
            client_id=ExistingUserAcctDevices.test_data["gf_nw_api_client_id"],
            client_secret=ExistingUserAcctDevices.test_data["gf_nw_api_client_secret"],
        )
        sm_app_subs_by_pcid = app_sm.get_sm_app_subscription_info_pcid(
            ui_doorway.pcid
        )
        day_start_timestamp = datetime.datetime.combine(
            datetime.datetime.now().date(),
            datetime.time.min,
            tzinfo=pytz.UTC
        ).timestamp()
        for subscription in sm_app_subs_by_pcid["subscriptions"]:
            assert subscription.get("evaluation_type") == "EVAL", \
                f"Failed! Subscription {subscription.get('subscription_key')} is not EVAL."
            assert day_start_timestamp == subscription.get("appointments").get("subscription_start") / 1000, \
                f"Failed! Subscription {subscription.get('subscription_key')} start time differ with current time:" \
                f"Actual timestamp: {subscription.get('appointments').get('subscription_start') / 1000}.\n" \
                f"Expected timestamp: {day_start_timestamp}."
        assert len(sm_app_subs_by_pcid["subscriptions"]) >= 14, \
            f"Failure! Wrong EVAL subscriptions count. Expected: more than 13; " \
            f"Actual: {len(sm_app_subs_by_pcid['subscriptions'])}"

    @staticmethod
    def _is_actual_subs(subs_details: dict, seats_required=2):
        subscription_end = subs_details.get("appointments", {}).get("subscription_end", 0) // 1000
        current_date = int(datetime.datetime.today().timestamp())
        available_quantity = subs_details.get("available_quantity")
        return subscription_end > current_date and available_quantity >= seats_required
