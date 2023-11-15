import json
import logging
import time

from hpe_glcp_automation_lib.libs.sm.helpers.sm_create_orders_helper import NewSubsOrder

from automation.configs.device_mappings.sm_mapping import SubsPartMap
from automation.conftest import ExistingUserAcctDevices, SubscriptionData
from automation.local_libs.ui_doorway.ui_doorway_devices_by_api import UiDoorwayDevices
from automation.tests.workflows.brownfield.networking.existing_acct_existing_devices. \
    brnf_network_existing_acct_existing_devices import WfExistingAcctExistingDevices
from automation.tests.workflows.brownfield.storage_compute.brnf_str_com_existing_acct_devices import \
    WfScExistingAcctDevices

log = logging.getLogger(__name__)


class SMAssignments:
    @classmethod
    def wf_assign_subs_eval(cls, device_type, serial, brnf_sa_login_load_account):
        license_tier_type = "ADVANCED"
        subscription_tier_name = SubsPartMap.lic_tier_type_mapping(device_type)
        subs_type, part_number = SubsPartMap.subs_part_map(device_type)
        try:
            for i in range(1, 10):
                license_list = brnf_sa_login_load_account.get_licenses()
                if len(license_list['subscriptions']) < 14:
                    log.info(len(license_list['subscriptions']))
                    time.sleep(10)
                if len(license_list['subscriptions']) >= 14:
                    log.info(len(license_list['subscriptions']))
                    break
            else:
                raise Exception("Not found license with sufficient count of subscriptions.")
        except Exception as e:
            log.info(e)
            return False
        log.info("found license for device {}: {}".format(subs_type, license_list))
        license_key = None
        for subscription in license_list['subscriptions']:
            if cls._is_actual_subs(subscription) and \
                    subscription.get("subscription_type") == subs_type and \
                    subscription.get("license_tier") == license_tier_type and \
                    subscription.get("subscription_tier_description") in subscription_tier_name:
                license_key = subscription['subscription_key']
                log.info(f"Found actual subscription: '{license_key}'.")
                break
        if not license_key:
            log.error("license key not found.")
            return False
        device_license = [(serial, license_key)]
        try:
            for index in range(3):
                resp = brnf_sa_login_load_account.assign_license_to_devices(device_license, device_type, part_number)
                if resp[0]['status'] == "SUCCESS":
                    log.info("license response for device_type: {}, {}".format(device_type, resp))
                    return True
                time.sleep(5)
        except Exception as e:
            log.error(f"not able to license the device_type {device_type}. Error: {e}")
            return False

    @classmethod
    def wf_create_new_subscription_assign_to_device(cls, device_type, brnf_sa_new_brim_subs_device,
                                                    brnf_sa_user_login_load_account):
        if "IAP" in device_type:
            serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_serial_subs_mgmt']
            part_number = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_part_no_subs_mgmt']
        elif "SWITCH" in device_type:
            serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_sw_serial_subs_mgmt']
            part_number = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_sw_part_no_subs_mgmt']
        elif "GATEWAY" in device_type:
            serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_gw_serial_subs_mgmt']
            part_number = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_gw_part_no_subs_mgmt']
        elif "COMPUTE" in device_type:
            serial = ExistingUserAcctDevices.test_data["brnf_sc_compute_serial_subs_mgmt"]
            part_number = ExistingUserAcctDevices.test_data["brnf_sc_compute_partnumber_subs_mgmt"]
        elif "STORAGE" in device_type:
            serial = ExistingUserAcctDevices.test_data["brnf_sc_storage_serial_subs_mgmt"]
            part_number = ExistingUserAcctDevices.test_data["brnf_sc_storage_partnumber_subs_mgmt"]
        else:
            log.error("Unknown device type: {}".format(device_type))

        if ("COMPUTE" in device_type) or ("STORAGE" in device_type):
            appid = ExistingUserAcctDevices.test_data['brnf_sc_app_id']
            application_instance_id = ExistingUserAcctDevices.test_data['brnf_sc_app_instance']
        else:
            appid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_appid']
            application_instance_id = ExistingUserAcctDevices.test_data[
                'brnf_existing_acct_existing_devices_instance_id']

        device_list = [{"serial_number": serial, "device_type": device_type, "part_number": part_number}]
        try:
            log.info("device list: {}".format(device_list))
            brnf_sa_user_login_load_account.unassign_devices_from_app_in_activate_inventory(device_list)
        except Exception as e:
            log.info(f"device in assign state, unassign before assigning. Error: {e}")
            pass
        time.sleep(11)

        verify_claim_devices = (brnf_sa_user_login_load_account.assign_devices_to_app_in_activate_inventory(
            device_list, appid, application_instance_id))
        log.info(f"Assigned application to device.")
        if 'OK' not in verify_claim_devices:
            log.info(f"Could not assign app to device, assign app before assigning subscription. Error: {e}")
            return False
        time.sleep(11)

        license_key, lic_quote = brnf_sa_new_brim_subs_device

        brnf_sa_user_login_load_account.sm_add_lic(license_key)
        if cls.check_licence_for_device_type(device_type, license_key, brnf_sa_user_login_load_account):
            device_licence = [(serial, license_key)]
            log.info("Assign license, {}, to device {}.".format(license_key, serial))
        else:
            raise Exception(f"Licence {license_key} not found")
        return cls.assign_license_to_device(device_type=device_type,
                                            device_license=device_licence,
                                            brnf_sa_login_load_account=brnf_sa_user_login_load_account)

    @staticmethod
    def wf_create_new_gecko_subscription_assign_to_device(device_type, brnf_sa_new_brim_subs_device,
                                                          brnf_sa_user_login_load_account, reverse=False):

        appid = ExistingUserAcctDevices.test_data['brnf_sc_app_id']
        application_instance_id = ExistingUserAcctDevices.test_data['brnf_sc_app_instance']

        license_key, lic_quote, lic_devices = brnf_sa_new_brim_subs_device

        if not reverse:
            # Toggle to see if subscription should be added first to customer account or device
            # if reverse not set, add license first. If reverse set, add device first
            # Claim the Gecko subscription
            brnf_sa_user_login_load_account.sm_add_lic(license_key)

        # Create Devices from Subscription List
        try:
            adi = WfScExistingAcctDevices()
            if "STORAGE" in device_type:
                created_device_info = adi.existing_acct_sc_create_device_fn(device_type=device_type,
                                                                            lic_devices=lic_devices)
            else:
                created_device_info = adi.existing_acct_sc_create_device_for_iaas(device_type, lic_devices)
        except Exception as e:
            log.error(f"unable to create devices from gecko subscription order. Error: {e}")
            return False

        # Claim the created Gecko Devices
        try:
            ui = UiDoorwayDevices()
            ui.claim_app_assignment_iaas_hciaas(device_type, created_device_info, brnf_sa_user_login_load_account)
        except Exception as e:
            log.error(f"unable to claim created devices from gecko subscription order. Error: {e}")
            return False

        device_list = [{"serial_number": lic_devices[0]["serial"],
                        "device_type": device_type, "part_number": lic_devices[0]["material"]}]

        try:
            log.info("device list: {}".format(device_list))
            brnf_sa_user_login_load_account.unassign_devices_from_app_in_activate_inventory(device_list)
        except Exception as e:
            log.info(f"device in assign state, unassign before assigning. Error: {e}")
            pass
        time.sleep(11)

        verify_claim_devices = (brnf_sa_user_login_load_account.assign_devices_to_app_in_activate_inventory(
            device_list, appid, application_instance_id))
        log.info(f"Assigned application to device.")
        if 'OK' not in verify_claim_devices:
            log.info(f"Could not assign app to device, assign app before assigning subscription. Error: {e}")
            return False
        time.sleep(11)

        if reverse:
            # Toggle to see if subscription should be added first to customer account or device
            # If reverse set, add device first. if reverse not set, add license first.
            # Claim the Gecko subscription
            brnf_sa_user_login_load_account.sm_add_lic(license_key)
            time.sleep(2)

        # Assign Gecko device with Gecko subscription
        create_test = WfExistingAcctExistingDevices()
        return create_test.check_iaas_license_key_assign_to_device(
            device_type,
            device_list[0]["serial_number"],
            license_key, brnf_sa_user_login_load_account
        )

    @staticmethod
    def wf_create_new_combined_subscription_ap_sw_gw(brnf_sa_new_brim_combined_subs_ap_sw_gw,
                                                     brnf_sa_user_login_load_account):
        ap_key, sw_key, gw_key, lic_quote = brnf_sa_new_brim_combined_subs_ap_sw_gw

        if ap_key:
            brnf_sa_user_login_load_account.sm_add_lic(ap_key)
        else:
            return False
        if sw_key:
            brnf_sa_user_login_load_account.sm_add_lic(sw_key)
        else:
            return False
        if gw_key:
            brnf_sa_user_login_load_account.sm_add_lic(gw_key)
        else:
            return False
        return True

    @staticmethod
    def wf_create_new_vgw_subscription_assign_to_device(device_type, brnf_sa_new_brim_subs_device,
                                                        brnf_sa_user_login_load_account,
                                                        sm_app_api, app_adi):
        if "GATEWAY" in device_type:
            serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_vgw_serial_subs_mgmt']
        else:
            log.error("Unknown device type: {}".format(device_type))

        pcid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_pcid']
        acid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_acid']
        device_list = {"serial_number": serial}

        # unprovision app for device
        res_unprov = app_adi.unprovision_device_from_application(payload=device_list)
        output_res_unprov = json.loads(res_unprov.content)
        log.info(f"Unprovision, output_res_unprov: {output_res_unprov}.")
        time.sleep(6)

        # provision app for device
        res_prov = app_adi.provision_dev_acid(acid, payload=device_list)
        output_res_prov = json.loads(res_prov.content)
        log.info(f"Provision, output_res_prov: {output_res_prov}.")
        time.sleep(6)

        # Add new BRIM license to account
        license_key, lic_quote = brnf_sa_new_brim_subs_device
        brnf_sa_user_login_load_account.sm_add_lic(license_key)

        # assign new subscription to device
        assert SMAssignments.wf_assign_subs_key_to_device(pcid=pcid, acid=acid, serial=serial, subs_key=license_key,
                                                          sm_app_api=sm_app_api)
        log.info("\nCurrent subscription key {}, assiged to IAP device, {}\n".format(license_key, serial))
        return True

    @staticmethod
    def wf_msp_unassign_and_assign_appl_subs_assign_to_device(device_type, tenant_acid, sm_app_api, app_adi):
        if "IAP" in device_type:
            serial = ExistingUserAcctDevices.test_data[
                'brownfield_msp1_with_three_tenants_and_app_iap_serial_subs_mgmt']
            # EVAL License to assign to device
            license_key = ExistingUserAcctDevices.test_data['brownfield_msp1_with_three_tenants_and_app_iap_lic_key']
        elif "SWITCH" in device_type:
            serial = ExistingUserAcctDevices.test_data[
                'brownfield_msp1_with_three_tenants_and_app_sw_serial_subs_mgmt']
            # EVAL License to assign to device
            license_key = ExistingUserAcctDevices.test_data['brownfield_msp1_with_three_tenants_and_app_sw_lic_key']
        elif "GATEWAY" in device_type:
            serial = ExistingUserAcctDevices.test_data[
                'brownfield_msp1_with_three_tenants_and_app_gw_serial_subs_mgmt']
            # EVAL License to assign to device
            license_key = ExistingUserAcctDevices.test_data['brownfield_msp1_with_three_tenants_and_app_gw_lic_key']
        else:
            log.error("Unknown device type: {}".format(device_type))

        acid = tenant_acid
        device_list = {"serial_number": serial}

        # unprovision app for device
        res_unprov = app_adi.unprovision_device_from_application(payload=device_list)
        output_res_unprov = json.loads(res_unprov.content)
        log.info(f"Unprovision, output_res_unprov: {output_res_unprov}.")
        time.sleep(6)

        # provision app for device
        res_prov = app_adi.provision_dev_acid(acid, payload=device_list)
        output_res_prov = json.loads(res_prov.content)
        log.info(f"Provision, output_res_prov: {output_res_prov}.")
        time.sleep(6)

        # MSP pcid, acid, to assign subscription to device
        msp_pcid = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid"]
        msp_acid = ExistingUserAcctDevices.test_data["brownfield_msp1_with_three_tenants_and_app"]["msp_acid_network"]

        # assign new subscription to device
        assert SMAssignments.wf_assign_subs_key_to_device(pcid=msp_pcid, acid=msp_acid, serial=serial,
                                                          subs_key=license_key,
                                                          sm_app_api=sm_app_api)
        log.info("\nCurrent subscription key {}, assigned to IAP device, {}\n".format(license_key, serial))
        return True

    def wf_update_qty_existing_subs_iap(quote, qty):
        end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
        app_api_host = ExistingUserAcctDevices.app_api_hostname
        sso_host = ExistingUserAcctDevices.sso_hostname
        aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
        aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']

        # create a new subscription for AP and add to account
        new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
        try:
            lic_qty, lic_quote = new_order.update_qty_subs_order(quote=quote, qty=qty)
            log.info("update_qty_subs_order, results: {}, {}".format(lic_qty, lic_quote))
            if (qty in lic_qty) or (lic_qty in qty):
                return True
        except Exception as e:
            log.error(f"Could not create new subscription dynamically. Error: {e}")
            return False

    def wf_upgrade_subs_tier_existing_subs_iap(upgrade_quote):
        end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
        app_api_host = ExistingUserAcctDevices.app_api_hostname
        sso_host = ExistingUserAcctDevices.sso_hostname
        aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
        aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']

        # create a new subscription for AP and add to account
        new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
        try:
            lic_quote = new_order.upgrade_subs_tier_ap(quote=upgrade_quote)
            log.info("upgrade_subs_order for quote: {}".format(lic_quote))
            return True
        except Exception as e:
            log.error(f"Could not create new subscription dynamically. Error: {e}")
            return False

    def wf_downgrade_subs_tier_existing_subs_iap(downgrade_quote):
        end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
        app_api_host = ExistingUserAcctDevices.app_api_hostname
        sso_host = ExistingUserAcctDevices.sso_hostname
        aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
        aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']

        # create a new subscription for AP and add to account
        new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
        try:
            lic_quote = new_order.downgrade_subs_tier_ap(quote=downgrade_quote)
            log.info("downgrade_subs_order for quote: {}".format(lic_quote))
            return True
        except Exception as e:
            log.error(f"Could not create new subscription dynamically. Error: {e}")
            return False

    def wf_existing_subs_to_expire(quote, sm_app_api):
        end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
        app_api_host = ExistingUserAcctDevices.app_api_hostname
        sso_host = ExistingUserAcctDevices.sso_hostname
        aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
        aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']
        serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_serial_subs_mgmt']

        # create a new subscription for AP and add to account
        new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
        try:
            lic_order_updated_key, lic_quote = new_order.update_subs_order_to_expired(quote=quote)
            log.info("update subscription key to expire, results: {}, {}".format(lic_order_updated_key, lic_quote))
            time.sleep(11)  # wait for the expired subscription to be removed from device

            try:
                for index in range(5):
                    res = sm_app_api.get_sm_app_device_subscription_assignment_based_on_serial(serial_no=serial)

                    if res['subscription_device_assignment']['subscription'][
                        'subscription_key'] != lic_order_updated_key:
                        log.info("Device subscription key changed after sub key expired, works correctly\n")
                        return True
                    time.sleep(6)
            except Exception as e:
                log.info(f"Device subscription key was not unassigned after key expiry: {e}")
                return False
        except Exception as e:
            log.error(f"Could not set the subscription to expire. Error: {e}")
            return False

    def wf_existing_subs_to_terminate(quote, sm_app_api):
        end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
        app_api_host = ExistingUserAcctDevices.app_api_hostname
        sso_host = ExistingUserAcctDevices.sso_hostname
        aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
        aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']
        serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_serial_subs_mgmt']

        # create a new subscription for AP and add to account
        new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
        try:
            lic_order_updated_key, lic_quote = new_order.terminate_subs_order(quote=quote)
            log.info("update subscription key to expire, results: {}, {}".format(lic_order_updated_key, lic_quote))
            time.sleep(11)  # wait for the expired subscription to be removed from device

            try:
                for index in range(5):
                    res = sm_app_api.get_sm_app_device_subscription_assignment_based_on_serial(serial_no=serial)

                    if res['subscription_device_assignment']['subscription'][
                        'subscription_key'] != lic_order_updated_key:
                        log.info("Device subscription key changed after sub key expired, works correctly\n")
                        return True
                    time.sleep(6)
            except Exception as e:
                log.info(f"Device subscription key was not unassigned after key expiry: {e}")
                return False
        except Exception as e:
            log.error(f"Could not set the subscription to expire. Error: {e}")
            return False

    def wf_extend_existing_subs_key(extend_quote, extend_by_sec):
        end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
        app_api_host = ExistingUserAcctDevices.app_api_hostname
        sso_host = ExistingUserAcctDevices.sso_hostname
        aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
        aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']

        # create a new subscription for AP and add to account
        new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
        try:
            lic_order_updated_key, lic_quote = new_order.extend_subs_order_by_seconds(quote=extend_quote,
                                                                                      sec=extend_by_sec)
            log.info("extend subscription key, results: {}, {}".format(lic_order_updated_key, lic_quote))
            time.sleep(6)  # wait for the expired subscription to be removed from device
            return True
        except Exception as e:
            log.error(f"Could not extend the subscription. Error: {e}")
            return False

    def wf_unassign_subs_key_to_device(pcid, acid, serial, sm_app_api):
        device_list = [serial]

        # create a new subscription for AP and add to account
        try:
            for index in range(5):  # try 5 times
                res = sm_app_api.subscription_unassign(device_list_lic=device_list, pcid=pcid, acid=acid)
                if res[0]['status'] == "SUCCESS" or res[0]['status'] == "DEVICE_NOT_FOUND":
                    log.info("Device subscription key unassigned \n")
                    return True
                time.sleep(6)  # wait for the expired subscription to be removed from device
            #     loop again if device key is still assigned

            log.info("Device subscription key was not unassigned\n")
            return False
        except Exception as e:
            log.error(f"Could not unassign the subscription from device. Error: {e}")
            return False

    def wf_assign_subs_key_to_device(pcid, acid, serial, subs_key, sm_app_api):
        try:
            for index in range(5):  # try 5 times
                res = sm_app_api.subscription_assign(pcid=pcid, acid=acid, device=serial, license=subs_key)

                if res[0]['status'] == "SUCCESS":
                    log.info("Device subscription key assigned: {} \n".format(res))
                    if res[0]['subscription_key'] == subs_key:
                        return True
                elif res[0]['status'] == "DEVICE_NOT_FOUND":
                    log.info("Device may not be provisioned with app ..")
                    return False
                time.sleep(6)  # wait for the expired subscription to be removed from device
            #     loop again if device key is still assigned

            log.info("Device subscription key was not unassigned\n")
            return False
        except Exception as e:
            log.error(f"Could not assign the subscription to device. Error: {e}")
            return False

    def wf_existing_subs_to_cancel(quote):
        end_username = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_username']
        app_api_host = ExistingUserAcctDevices.app_api_hostname
        sso_host = ExistingUserAcctDevices.sso_hostname
        aop_client_id = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_id']
        aop_client_secret = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_client_secret']

        # create a new subscription for AP and add to account
        new_order = NewSubsOrder(end_username, app_api_host, sso_host, aop_client_id, aop_client_secret)
        try:
            lic_order_updated_key, lic_quote = new_order.update_subs_order_to_cancelled(quote=quote)
            log.info("update subscription key to expire, results: {}, {}".format(lic_order_updated_key, lic_quote))
            return True
        except Exception as e:
            log.error(f"Could not set the subscription to expire. Error: {e}")
            return False

    @staticmethod
    def wf_unassign_assign_new_aruba_skus_iap(sm_app_api, device_type):
        serial = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_serial_subs_mgmt']
        pcid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_pcid']
        acid = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_acid']
        lic_key = ExistingUserAcctDevices.test_data['brnf_existing_acct_existing_devices_iap_new_aruba_skus']

        for each in lic_key:
            # unassign the subscription to device
            assert SMAssignments.wf_unassign_subs_key_to_device(pcid=pcid, acid=acid,
                                                                serial=serial, sm_app_api=sm_app_api)
            log.info("\nCurrent subscription key unassiged from IAP device, {}\n".format(serial))
            # assign the subscription to device
            assert SMAssignments.wf_assign_subs_key_to_device(pcid=pcid, acid=acid, serial=serial, subs_key=each,
                                                              sm_app_api=sm_app_api)
            log.info("\nCurrent subscription key {}, assiged to IAP device, {}\n".format(each, serial))
        return True

    @staticmethod
    def _is_actual_subs(subs_details: dict, seats_required=2):
        subscription_end = subs_details.get("appointments", {}).get("subscription_end", 0) // 1000
        current_date = int(time.time())
        available_quantity = subs_details.get("available_quantity")
        return subscription_end > current_date and available_quantity >= seats_required

    @staticmethod
    def check_licence_for_device_type(device_type, license_key, brnf_sa_login_load_account) -> bool:
        params = {"subscription_key": license_key}
        try:
            license_list = brnf_sa_login_load_account.get_licenses(params=params)
        except Exception as e:
            log.error(e)
            return False
        log.info("found license for device: {}".format(license_list))
        if not license_list['subscriptions'][0]['subscription_key']:
            log.error("license key not found.")
            return False
        log.info("License key found in details: {}".format(license_list['subscriptions'][0]['subscription_key']))
        return True

    @staticmethod
    def assign_license_to_device(device_type, device_license, brnf_sa_login_load_account):
        if "COMPUTE" in device_type:
            part_number = ExistingUserAcctDevices.test_data["brnf_sc_compute_partnumber_subs_mgmt"]
        elif "STORAGE" in device_type:
            part_number = ExistingUserAcctDevices.test_data["brnf_sc_storage_partnumber_subs_mgmt"]
        else:
            part_number = SubscriptionData(device_type).part_number
        try:
            for index in range(3):
                resp = brnf_sa_login_load_account.assign_license_to_devices(device_license, device_type, part_number)
                if resp[0]['status'] == "SUCCESS":
                    log.info("license response for device_type: {},\n{}".format(device_type, resp))
                    return True
                time.sleep(5)
        except Exception as e:
            log.error(f"not able to license the device_type {device_type}. Error: {e}")
            return False

    @staticmethod
    def wf_existing_device_subscription_assignment(pcid, acid, serial, lic_key, sm_app_api_session):
        """ Helper function to assign the subscription for a device
            params:- pcid, acid, serial, lic_key, sm_app_api_session"""

        SMAssignments.wf_unassign_subs_key_to_device(pcid=pcid, acid=acid, serial=serial,
                                                     sm_app_api=sm_app_api_session)

        result = SMAssignments.wf_assign_subs_key_to_device(pcid=pcid, acid=acid, serial=serial, subs_key=lic_key,
                                                            sm_app_api=sm_app_api_session)
        if result:
            log.info("Subscription assigned successfully")

        return result
