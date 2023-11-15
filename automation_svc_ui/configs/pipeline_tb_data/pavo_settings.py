import json
import logging
import os
import sys

from automation_svc_ui.constants import AUTOMATION_DIRECTORY

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.INFO)


def pavo_test_data(current_env, secrets, passwords):
    tb_data = {}
    tb_data["brownfield_account_with_all_app_types"] = {}
    tb_data["brownfield_account_with_one_network_app"] = {}
    tb_data["brownfield_msp1_with_three_tenants_and_app"] = {}
    tb_data["brownfield_msp2_with_one_tenant_and_app"] = {}
    tb_data["harness_brownfield_account_parent_pcid"] = {}
    tb_data["harness_activate_bridge"] = {}

    if "pavo" in current_env:
        tb_data["url"] = current_env
        tb_data["gmail_username"] = "hcloud203@gmail.com"
        tb_data["gmail_password"] = passwords[tb_data["gmail_username"]]
        tb_data["sso_host"] = "sso.common.cloud.hpe.com"
        tb_data["gf_nw_api_client_id"] = "f2e9fe76-b3d4-4209-878d-a778a99cc060_api"
        tb_data["gf_nw_api_client_secret"] = secrets[tb_data["gf_nw_api_client_id"]]
        tb_data["gf_nw_app_id"] = "ea428cfc-b3b3-4d9c-93f0-87a3b7b633bd"
        tb_data["gf_nw_app_region"] = "us-west"

        tb_data["brnf_service_subs_username"] = "hcloud203+sbufuin@gmail.com"
        tb_data["brnf_service_subs_password"] = passwords[
            tb_data["brnf_service_subs_username"]
        ]
        tb_data["brnf_service_subs_pcid"] = "dbc5f1ecde5c11ed8807cac2e255840b"
        tb_data[
            "brnf_service_subs_existing_app_id"
        ] = "dfcd4900-533c-4116-a59d-11339ae9c919"
        tb_data["brnf_service_subs_new_app_id"] = "e96229dc-5d37-4a73-9063-f439175a9b66"
        tb_data["brnf_service_subs_new_region"] = "us-west"
        tb_data[
            "brnf_service_subs_api_client_id"
        ] = "a97c28dd-779d-43ba-be7b-1be8d19f9bba_api"
        tb_data["brnf_service_subs_api_client_secret"] = secrets[
            tb_data["brnf_service_subs_api_client_id"]
        ]

        tb_data["brnf_sc_api_client_id"] = "a97c28dd-779d-43ba-be7b-1be8d19f9bba_api"
        tb_data["brnf_sc_api_client_secret"] = secrets[tb_data["brnf_sc_api_client_id"]]
        tb_data["brnf_sc_username"] = "hcloud203+azoayyq@gmail.com"
        tb_data["brnf_sc_password"] = passwords[tb_data["brnf_sc_username"]]
        tb_data["brnf_sc_pcid"] = "b724a594de5d11ed810f1a4d9281a896"
        tb_data["brnf_sc_pcid_name"] = "azoayyq-1 company"
        tb_data["brnf_sc_app_instance"] = "a4c0a347-c64a-4a02-b02a-f9c385d3d340"
        tb_data["brnf_sc_app_id"] = "dfcd4900-533c-4116-a59d-11339ae9c919"
        tb_data["brnf_sc_app_cid"] = "e9a86c94de5d11edb6289ae7c29a0cf8"
        tb_data["brnf_sc_compute_serial_subs_mgmt"] = "SMCMPTO01"
        tb_data["brnf_sc_compute_partnumber_subs_mgmt"] = "R6Z88AAE"
        tb_data["brnf_sc_storage_serial_subs_mgmt"] = "SMBAASTST1"
        tb_data["brnf_sc_storage_partnumber_subs_mgmt"] = "BAASTESTVIJAY1"

        tb_data['brnf_existing_acct_existing_devices_username'] = "hcloud203+fbkwmqq@gmail.com"
        tb_data['brnf_existing_acct_existing_devices_password'] = passwords[
            tb_data["brnf_existing_acct_existing_devices_username"]]
        tb_data['brnf_existing_acct_existing_devices_acct1'] = "fbkwmqq Company"
        tb_data['brnf_existing_acct_existing_devices_client_id'] = "a97c28dd-779d-43ba-be7b-1be8d19f9bba_api"
        tb_data['brnf_existing_acct_existing_devices_client_secret'] = secrets[
            tb_data['brnf_existing_acct_existing_devices_client_id']]
        tb_data['brnf_existing_acct_existing_devices_pcid'] = "4b137af8b9e911edb9edf2f3ac56d5ee"
        tb_data['brnf_existing_acct_existing_devices_appid'] = "97ea1298-db08-4244-818f-2c11ef33396e"
        tb_data['brnf_existing_acct_existing_devices_instance_id'] = "b87b5d9c-0e83-499a-9cb7-19d84d9643d5"
        tb_data['brnf_existing_acct_existing_devices_acid'] = "72fe0c24018611eebab622510d733706"
        tb_data['brnf_existing_acct_existing_devices_iap_sn'] = "STIAP4KOBP"
        tb_data['brnf_existing_acct_existing_devices_iap_mac'] = "00:00:00:0B:B4:B9"
        tb_data['brnf_existing_acct_existing_devices_gw_sn'] = "STGWA722RQ"
        tb_data['brnf_existing_acct_existing_devices_gw_mac'] = "00:00:00:6B:B6:85"
        tb_data['brnf_existing_acct_existing_devices_sw_sn'] = "STSWIXMA7X"
        tb_data['brnf_existing_acct_existing_devices_sw_mac'] = "00:00:00:1B:B9:F1"
        tb_data["brnf_existing_acct_existing_devices_iap_serial_subs_mgmt"] = "SMTSTAP001"
        tb_data["brnf_existing_acct_existing_devices_iap_part_no_subs_mgmt"] = "JW242AR"
        tb_data["brnf_existing_acct_existing_devices_iap_mac_subs_mgmt"] = "01:02:03:a1:b1:a7"
        tb_data["brnf_existing_acct_existing_devices_sw_serial_subs_mgmt"] = "SMTSTSW001"
        tb_data["brnf_existing_acct_existing_devices_sw_part_no_subs_mgmt"] = "JL255A"
        tb_data["brnf_existing_acct_existing_devices_sw_mac_subs_mgmt"] = "AB:CD:EF:F8:FF:ED"
        tb_data["brnf_existing_acct_existing_devices_gw_serial_subs_mgmt"] = "SMTSTGW001"
        tb_data["brnf_existing_acct_existing_devices_gw_part_no_subs_mgmt"] = "7005-RW"
        tb_data["brnf_existing_acct_existing_devices_gw_mac_subs_mgmt"] = "AB:CD:EF:FF:FE:01"
        tb_data['brnf_existing_acct_existing_devices_iap_lic_key'] = "E02C4D220D60F45D49"
        tb_data['brnf_existing_acct_existing_devices_gw_lic_key'] = "EB7CDE16A436F4F5AA"
        tb_data['brnf_existing_acct_existing_devices_sw_lic_key'] = "ED02339C259C843D08"
        tb_data["brnf_existing_acct_existing_devices_vgw_serial_subs_mgmt"] = "SMVGWTST01"
        tb_data["brnf_existing_acct_existing_devices_vgw_part_no_subs_mgmt"] = "MC-VA"
        tb_data["brnf_existing_acct_existing_devices_vgw_mac_subs_mgmt"] = "AB:CD:EF:FA:FB:01"
        tb_data["brnf_existing_acct_existing_devices_vgw_serial_no"] = "VG2109047341"
        tb_data["brnf_existing_acct_existing_devices_vgw_part_no"] = "MC-VA"
        tb_data["brnf_existing_acct_existing_devices_vgw_mac"] = "02:1A:1E:C5:7B:CC"
        tb_data["brnf_existing_acct_existing_devices_nontpm_serial_no"] = "CN29FP307G"
        tb_data["brnf_existing_acct_existing_devices_nontpm_part_no"] = "J9772A"
        tb_data["brnf_existing_acct_existing_devices_nontpm_mac"] = "00:9C:02:63:C5:00"

        tb_data["brnf_existing_acct_new_devices_username"] = "hcloud203+igezfuq@gmail.com"
        tb_data["brnf_existing_acct_new_devices_password"] = passwords[
            tb_data["brnf_existing_acct_new_devices_username"]]
        tb_data["brnf_existing_acct_new_devices_pcid1"] = "048aa7ae3cda11eea3ae46b5064abf2a"
        tb_data["brnf_existing_acct_new_devices_pcid1_name"] = "igezfuq-2nd company"
        tb_data["brnf_existing_acct_new_devices_app_instance"] = "b87b5d9c-0e83-499a-9cb7-19d84d9643d5"
        tb_data["brnf_existing_acct_new_devices_app_id"] = "97ea1298-db08-4244-818f-2c11ef33396e"
        tb_data["brnf_existing_acct_new_devices_app_cid"] = "27cf93403cdb11eea867f27c3df0c6e2"
        tb_data["brnf_existing_acct_new_devices_client_id"] = "a97c28dd-779d-43ba-be7b-1be8d19f9bba_api"
        tb_data["brnf_existing_acct_new_devices_client_secret"] = \
            secrets[tb_data["brnf_existing_acct_new_devices_client_id"]]

        # standalone account with all app types
        tb_data['brownfield_account_with_all_app_types']['account_name'] = "fbmtuvk"
        tb_data['brownfield_account_with_all_app_types']['username'] = "hcloud203+fbmtuvk@gmail.com"
        tb_data['brownfield_account_with_all_app_types']['pcid'] = "e33404f4ee9811eda60d6a9e44d0ca9d"
        tb_data['brownfield_account_with_all_app_types']['appid_network'] = "97ea1298-db08-4244-818f-2c11ef33396e"
        tb_data["brownfield_account_with_all_app_types"][
            'app_instance_id_network'] = "b87b5d9c-0e83-499a-9cb7-19d84d9643d5"
        tb_data["brownfield_account_with_all_app_types"]['acid_network'] = "4f958dd0018f11eea18c62bd665379b8"
        tb_data['brownfield_account_with_all_app_types'][
            'appid_storage_compute'] = "dfcd4900-533c-4116-a59d-11339ae9c919"
        tb_data["brownfield_account_with_all_app_types"][
            'app_instance_id_storage_compute'] = "a4c0a347-c64a-4a02-b02a-f9c385d3d340"
        tb_data["brownfield_account_with_all_app_types"]['acid_storage_compute'] = "76976e9cf0ca11ed8d4c62d622ee59fc"

        # standalone account with only 1 Network app
        tb_data['brownfield_account_with_one_network_app']['account_name'] = "igezfuq"
        tb_data['brownfield_account_with_one_network_app']['username'] = "hcloud203+igezfuq@gmail.com"
        tb_data['brownfield_account_with_one_network_app']['pcid'] = "9c138d36effd11eda7e476e336d94fcd"
        tb_data['brownfield_account_with_one_network_app']['appid_network'] = "97ea1298-db08-4244-818f-2c11ef33396e"
        tb_data["brownfield_account_with_one_network_app"][
            'app_instance_id_network'] = "b87b5d9c-0e83-499a-9cb7-19d84d9643d5"
        tb_data["brownfield_account_with_one_network_app"]['acid_network'] = "10d222e2019011ee886b0e95f39eefb2"

        # MSP account with 3 Tenants and 1 Network app
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["account_name"] = "yaoseyz"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["username"] = "hcloud203+yaoseyz@gmail.com"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["password"] = \
            passwords[tb_data["brownfield_msp1_with_three_tenants_and_app"]["username"]]
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["app_name_network"] = "Authz Sample App"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["app_short_name_network"] = "AUTHSR"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["appid_network"] = "97ea1298-db08-4244-818f-2c11ef33396e"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["app_instance_id_network"] = \
            "b87b5d9c-0e83-499a-9cb7-19d84d9643d5"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid"] = "d93e1e08ee2f11edafc8865edd362fb8"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid_name"] = "yaoseyz"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["msp_acid_network"] = "c3eb9068017f11eebab622510d733706"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant1_name"] = "sm_tenant_1"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant1_pcid"] = "10ed3ff0ee3011edb1387aa1668f5b99"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant1_acid_network"] = \
            "a6d657e0019011eea1ffd2fd27a3727d"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant2_name"] = "sm_tenant_2"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant2_pcid"] = "18660230ee3011eda17c16af4ee97961"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant2_acid_network"] = \
            "952ea902019011eeaffa7ab663c053e1"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant3_name"] = "ztp_activate_account_tenant_1"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant3_pcid"] = "6d8b7ad4f3ca11ed8c92464acd06c229"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant3_acid_network"] = \
            "89b77f2c019011ee81d71e480d57c4e1"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_serial_subs_mgmt"] = "SMMSPAP004"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_part_no_subs_mgmt"] = "JW242AR"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_mac_subs_mgmt"] = "01:02:03:A1:B1:B1"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_lic_key"] = "EA017B8E9F7C24656A"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_serial_subs_mgmt"] = "SMMSPSW004"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_part_no_subs_mgmt"] = "JL255A"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_mac_subs_mgmt"] = "AB:CD:EF:F8:FF:A1"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_lic_key"] = "E6EF6F52AE0C2453D9"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_serial_subs_mgmt"] = "SMTSTGW004"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_part_no_subs_mgmt"] = "7005-RW"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_mac_subs_mgmt"] = "AB:CD:EF:FF:FE:04"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_lic_key"] = "E785C3C8EC3F74C7CB"

        # MSP account with 1 Tenant and 1 Network app
        tb_data['brownfield_msp2_with_one_tenant_and_app']['account_name'] = "dqhmbvd"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['username'] = "hcloud203+dqhmbvd@gmail.com"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['password'] = \
            passwords[tb_data['brownfield_msp2_with_one_tenant_and_app']['username']]
        tb_data['brownfield_msp2_with_one_tenant_and_app']['appid_network'] = "97ea1298-db08-4244-818f-2c11ef33396e"
        tb_data["brownfield_msp2_with_one_tenant_and_app"][
            'app_instance_id_network'] = "b87b5d9c-0e83-499a-9cb7-19d84d9643d5"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['msp_pcid'] = "e5b48bf8ee3011ed80ef82bc6c1a034b"
        tb_data["brownfield_msp2_with_one_tenant_and_app"]['msp_acid_network'] = "c4c810b2019111eea6e4224589e9e83f"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['tenant1_name'] = "tenant_tst1"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['tenant1_pcid'] = "6b4d4138ee3111edb03d82bc6c1a034b"
        tb_data["brownfield_msp2_with_one_tenant_and_app"]['tenant1_acid_network'] = "e3641444019111eebcdf7e44a970cb95"

        tb_data['harness_brownfield_account_parent_pcid']['account_name_parent'] = "HarnessParentAccount"
        tb_data['harness_brownfield_account_parent_pcid']['account_name_child'] = "HarnessChild1Account"
        tb_data['harness_brownfield_account_parent_pcid']['username'] = "ccsadift+brownfield_fta2@gmail.com"
        tb_data["harness_brownfield_account_parent_pcid"] = "60689fb603ed11ee8ccc72219d4c57ef"
        tb_data["harness_brownfield_account_child_pcid"] = "7fa73e0a03ed11eeab529ea55a4a159a"

        tb_data["humio_user_token"] = passwords["humio_token"]
        # Activate Bridge
        tb_data['harness_activate_bridge']['bridge_credential_user0'] = "cppm"
        tb_data['harness_activate_bridge']['bridge_credential_user1'] = "ccsadift+brownfield_fta2@gmail.com"
        tb_data["harness_activate_bridge"]["bridge_credential_password0"] = passwords[tb_data["harness_activate_bridge"]["bridge_credential_user0"]]
        tb_data["harness_activate_bridge"]["bridge_credential_password1"] = passwords[tb_data["harness_activate_bridge"]["bridge_credential_user1"]]

        sm_details_path = \
            os.path.join(AUTOMATION_DIRECTORY, "configs", "devices_data", "sm_files",
                         "new_aruba_skus_iap.json")
        log.info(f"Resolved path to 'new_aruba_skus_iap.json': {sm_details_path}")
        with open(sm_details_path, "r") as sm_keys:
            tb_data["brnf_existing_acct_existing_devices_iap_new_aruba_skus"] = json.load(sm_keys)

        return tb_data
