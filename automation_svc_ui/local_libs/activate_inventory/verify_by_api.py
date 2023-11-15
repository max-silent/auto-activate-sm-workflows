import json
import logging

log = logging.getLogger(__name__)


class VerifyByApi:
    @staticmethod
    def verify_get_devices_by_acid(brnf_sa_login_load_account,
                                   app_adi,
                                   device,
                                   app_cust_id=None,
                                   secondary=None):
        if not app_cust_id:
            provisioned_apps = brnf_sa_login_load_account.get_provisions()
            for app in provisioned_apps["provisions"]:
                if app["provision_status"] == "PROVISIONED":
                    app_cust_id = app["application_customer_id"]
        get_device_by_acid_list = app_adi.get_devices_by_acid(application_customer_id=app_cust_id, secondary=secondary).json()
        if isinstance(device, str):
            for get_device in get_device_by_acid_list['devices']:
                if get_device["serial_number"] == device:
                    return True
        else:
            log.error("not able to run device_by_acid_list")
            return False

    @staticmethod
    def verify_get_devices_by_pcid(brnf_sa_login_load_account,
                                   app_adi,
                                   device,
                                   platform_cust_id=None,
                                   secondary=None):
        if not platform_cust_id:
            provisioned_apps = brnf_sa_login_load_account.get_provisions()
            for app in provisioned_apps['provisions']:
                if app['provision_status'] == "PROVISIONED":
                    platform_cust_id = app['platform_customer_id']

        device_by_pcid_list = app_adi.get_devices_by_pcid(platform_customer_id=platform_cust_id, secondary=secondary)
        device_list = json.loads(device_by_pcid_list.content)
        log.info(device_by_pcid_list.content)
        if isinstance(device, str):
            for get_device in device_list['devices']:
                if get_device["serial_number"] == device:
                    return True
            log.error(f"Device '{device}' is not in the devices' list of account with PCID: '{platform_cust_id}'")
            return False
        else:
            log.error("not able to run device_by_acid_list")
            return False

    @staticmethod
    def verify_app_subscription_info_acid(brnf_sa_login_load_account,
                                          app_sm,
                                          device,
                                          app_cust_id=None,
                                          platform_cust_id=None):
        if not app_cust_id:
            provisioned_apps = brnf_sa_login_load_account.get_provisions()
            for app in provisioned_apps["provisions"]:
                if app["provision_status"] == "PROVISIONED":
                    app_cust_id = app['application_customer_id']
                    platform_cust_id = app['platform_customer_id']
        sm_app_subs_by_acid = app_sm.get_sm_app_subscription_devices(platform_cust_id,
                                                                     app_cust_id,
                                                                     params={"limit": 500, "offset": 0})
        if isinstance(device, str):
            for get_subscriptions in sm_app_subs_by_acid['subscription_assignments']:
                if get_subscriptions['device']['serial_number'] == device:
                    return True
            log.error("Device was not found in the list of subscribed devices")
            return False
        else:
            log.error("not able to run device_by_acid_list")
            return False

    @staticmethod
    def verify_app_subscription_info_pcid(brnf_sa_login_load_account,
                                          app_sm,
                                          device,
                                          platform_cust_id=None):
        if not platform_cust_id:
            provisioned_apps = brnf_sa_login_load_account.get_provisions()
            for app in provisioned_apps['provisions']:
                if app['provision_status'] == "PROVISIONED":
                    platform_cust_id = app['platform_customer_id']
        sm_app_subs_by_pcid = app_sm.get_sm_app_subscription_info_pcid(platform_cust_id)
        if isinstance(device, str):
            if len(sm_app_subs_by_pcid['subscriptions']) >= 16:
                return True
        else:
            log.error("not able to run device_by_acid_list")
            return False
        
    @staticmethod     
    def get_all_network_devices_by_pcid(adi_app_api_session, pcid, archived_only = None) -> list:
        """
        Method to filter the list of Network devices
        :param adi_app_api_session: Authorization bearer token
        :param pcid: Platform Customer ID
        :return: list of network devices
        """

        response = adi_app_api_session.get_devices_by_pcid(platform_customer_id=pcid, archived_only=archived_only)
        log.info(type(response))
        log.info(response.json())
        devices = response.json()["devices"]
        net_devices = []
        for dev in devices:
            if dev["device_type"] == "AP" or dev["device_type"] == "GATEWAY" or dev["device_type"] == "SWITCH":
                net_devices.append(dev)

        return net_devices
