import json
import logging
import os
import sys

from automation.constants import AUTOMATION_DIRECTORY

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.INFO)


def mira_test_data(current_env, secrets, passwords):
    tb_data = {}
    tb_data['brownfield_account_with_all_app_types'] = {}
    tb_data['brownfield_account_with_one_network_app'] = {}
    tb_data["brownfield_msp1_with_three_tenants_and_app"] = {}
    tb_data['brownfield_msp2_with_one_tenant_and_app'] = {}
    tb_data['harness_brownfield_account_parent_pcid'] = {}
    tb_data["archive_devices_related_account"] = {}
    tb_data["harness_activate_bridge"] = {}

    if "mira" in current_env:
        tb_data["url"] = current_env
        tb_data["gmail_username"] = "hcloud203@gmail.com"
        tb_data["gmail_password"] = passwords[tb_data["gmail_username"]]
        tb_data["sso_host"] = "qa-sso.ccs.arubathena.com"
        tb_data[
            "ccs_activate_v1_device_url"
        ] = "mira-activate-v1-device.ccs.arubathena.com"
        tb_data["gf_nw_api_client_id"] = "swsc_client"
        tb_data["gf_nw_api_client_secret"] = secrets[tb_data["gf_nw_api_client_id"]]
        tb_data["gf_nw_app_id"] = "65858496-324d-492e-b117-6cfbb10b90a4"
        tb_data["gf_nw_app_region"] = "ap-southeast"

        tb_data["brnf_service_subs_username"] = "hcloud203+sbufuin@gmail.com"
        tb_data["brnf_service_subs_password"] = passwords[tb_data["brnf_service_subs_username"]]
        tb_data["brnf_service_subs_pcid"] = "c0cc79f69d8411edb50a8a531f6b79ec"
        tb_data["brnf_service_subs_existing_app_id"] = "ba9e8972-0169-4415-993a-81a0eeb328b2"
        tb_data["brnf_service_subs_new_app_id"] = "0fc65719-156c-46f3-b804-a65e1aa811f3"
        tb_data["brnf_service_subs_new_region"] = "us-west"
        tb_data["brnf_service_subs_api_client_id"] = "swsc_client"
        tb_data["brnf_service_subs_api_client_secret"] = secrets[tb_data["brnf_service_subs_api_client_id"]]

        tb_data["brnf_sc_api_client_id"] = "swsc_client"
        tb_data["brnf_sc_api_client_secret"] = secrets[tb_data["brnf_sc_api_client_id"]]
        tb_data["brnf_sc_username"] = "hcloud203+azoayyq@gmail.com"
        tb_data["brnf_sc_password"] = passwords[tb_data["brnf_sc_username"]]
        tb_data["brnf_sc_pcid"] = "420b8d76cebe11edae518aa4e409bf24"
        tb_data["brnf_sc_pcid_name"] = "azoayyq-2nd company"
        tb_data["brnf_sc_app_instance"] = "d67454df-5068-4811-a72e-bbe0e3908e0f"
        tb_data["brnf_sc_app_id"] = "ba9e8972-0169-4415-993a-81a0eeb328b2"
        tb_data["brnf_sc_app_cid"] = "6ff2e748cebe11ed9aeec6b701bb9a56"
        tb_data["brnf_sc_compute_serial_subs_mgmt"] = "SMCMPTO01"
        tb_data["brnf_sc_compute_partnumber_subs_mgmt"] = "R6Z88AAE"
        tb_data["brnf_sc_storage_serial_subs_mgmt"] = "SMBAASTST1"
        tb_data["brnf_sc_storage_partnumber_subs_mgmt"] = "BAASTESTVIJAY1"

        tb_data["tac_admin_username"] = "vingogkum+mira-25@gmail.com"
        tb_data["tac_admin_password"] = \
            passwords[tb_data["tac_admin_username"]]
        tb_data["tac_admin_pcid1"] = "c76633d8127511eca5121eea03ba3a0a"
        tb_data["tac_admin_pcid1_name"] = "HPE GreenLake Support"
        tb_data["tac_existing_acct_existing_devices_username"] = "hcloud203+fogvqrr@gmail.com"
        tb_data["tac_existing_acct_existing_devices_password"] = \
            passwords[tb_data["tac_existing_acct_existing_devices_username"]]
        tb_data["tac_existing_acct_existing_devices_pcid1"] = "597987f8cf9311edb8f2a243e89d56d8"
        tb_data["tac_existing_acct_existing_devices_pcid1_name"] = "fogvqrr"
        tb_data["tac_existing_acct_existing_devices_pcid1_athena_f_folder"] = \
            "athena-f-66d34ff6cf9311ed844372916cc9bfc8"
        tb_data["tac_existing_acct_existing_devices_pcid1_iap_sn"] = "STIAP9NHBU"
        tb_data["tac_existing_acct_existing_devices_pcid1_iap_part_no"] = "JW242AR"
        tb_data["tac_existing_acct_existing_devices_pcid1_iap_mac"] = "00:00:00:01:17:AC"
        tb_data["tac_existing_acct_existing_devices_pcid1_gw_sn"] = "STGWAI33U1"
        tb_data["tac_existing_acct_existing_devices_pcid1_gw_part_no"] = "7005-RW"
        tb_data["tac_existing_acct_existing_devices_pcid1_gw_mac"] = "00:00:00:81:BF:EB"
        tb_data["tac_existing_acct_existing_devices_pcid1_sw_sn"] = "STSWIPKDOF"
        tb_data["tac_existing_acct_existing_devices_pcid1_sw_part_no"] = "JL255A"
        tb_data["tac_existing_acct_existing_devices_pcid1_sw_mac"] = "00:00:00:48:5B:91"
        tb_data["tac_existing_acct_existing_devices_pcid1_iap_eval_subs_key_assigned"] = "E732C77524AF342319"
        tb_data["tac_existing_acct_existing_devices_pcid1_gw_brim_subs_key_assigned"] = "COGATEWAYCMEUPAPS14"
        tb_data["tac_existing_acct_existing_devices_pcid1_sw_brim_subs_key"] = "CTHSWITCHCMEUPAPS14"
        tb_data["tac_existing_acct_existing_devices_pcid1_service_brim_subs_key"] = "FLSP6SERTEST001"
        # comp
        tb_data["brnf_existing_acct_existing_devices_comp_appid"] = "ba9e8972-0169-4415-993a-81a0eeb328b2"
        tb_data["brnf_existing_acct_existing_devices_comp_instance_id"] = "d67454df-5068-4811-a72e-bbe0e3908e0f"
        tb_data["brnf_existing_acct_existing_devices_comp_acid"] = "6ff2e748cebe11ed9aeec6b701bb9a56"
        tb_data["brnf_existing_acct_existing_devices_comp_sn"] = "STCOMSER1"
        tb_data["brnf_existing_acct_existing_devices_comp_mac"] = "02:2E:91:F2:B8:E2"
        tb_data["brnf_existing_acct_existing_devices_comp_part"] = "STCOMPT1"

        tb_data["brnf_existing_acct_existing_devices_username"] = "hcloud203+omedtmh@gmail.com"
        tb_data["brnf_existing_acct_existing_devices_password"] = passwords[
            tb_data["brnf_existing_acct_existing_devices_username"]]
        tb_data["brnf_existing_acct_existing_devices_acct1"] = "omedtmh-2nd company"
        tb_data["brnf_existing_acct_existing_devices_pcid"] = "0a708a58cea811edba93468850bb45f6"
        tb_data["brnf_existing_acct_existing_devices_appid"] = "65858496-324d-492e-b117-6cfbb10b90a4"
        tb_data["brnf_existing_acct_existing_devices_instance_id"] = "05a2fdd2-b91e-4a02-834f-262a88b4de43"
        tb_data["brnf_existing_acct_existing_devices_acid"] = "b1ee50dacea811edbfceeefd57059e3b"
        tb_data["brnf_existing_acct_existing_devices_iap_sn"] = "STIAPERP4Q"
        tb_data["brnf_existing_acct_existing_devices_iap_mac"] = "00:00:00:8C:CF:D4"
        tb_data["brnf_existing_acct_existing_devices_gw_sn"] = "STGWAQEAF5"
        tb_data["brnf_existing_acct_existing_devices_gw_mac"] = "00:00:00:2F:20:08"
        tb_data["brnf_existing_acct_existing_devices_sw_sn"] = "STSWI364FU"
        tb_data["brnf_existing_acct_existing_devices_sw_mac"] = "00:00:00:C2:67:EA"
        tb_data["brnf_existing_acct_existing_devices_client_id"] = "swsc_client"
        tb_data["brnf_existing_acct_existing_devices_client_secret"] = secrets[
            tb_data["brnf_existing_acct_existing_devices_client_id"]]
        tb_data["brnf_existing_acct_existing_devices_api_client_id"] = "swsc_client"
        tb_data["brnf_existing_acct_existing_devices_api_client_secret"] = secrets[
            tb_data["brnf_existing_acct_existing_devices_api_client_id"]]
        tb_data["brnf_existing_acct_existing_devices_iap_serial_subs_mgmt"] = "STIAP3MHIC"
        tb_data["brnf_existing_acct_existing_devices_iap_part_no_subs_mgmt"] = "JW242AR"
        tb_data["brnf_existing_acct_existing_devices_iap_mac_subs_mgmt"] = "00:00:00:43:B1:A8"
        tb_data["brnf_existing_acct_existing_devices_sw_serial_subs_mgmt"] = "STSWI6CKIL"
        tb_data["brnf_existing_acct_existing_devices_sw_part_no_subs_mgmt"] = "JL255A"
        tb_data["brnf_existing_acct_existing_devices_sw_mac_subs_mgmt"] = "00:00:00:47:68:5B"
        tb_data["brnf_existing_acct_existing_devices_gw_serial_subs_mgmt"] = "STGWABSZYB"
        tb_data["brnf_existing_acct_existing_devices_gw_part_no_subs_mgmt"] = "7005-RW"
        tb_data["brnf_existing_acct_existing_devices_gw_mac_subs_mgmt"] = "00:00:00:0E:0F:25"
        tb_data["brnf_existing_acct_existing_devices_vgw_serial_subs_mgmt"] = "SMVGWTST01"
        tb_data["brnf_existing_acct_existing_devices_vgw_part_no_subs_mgmt"] = "MC-VA"
        tb_data["brnf_existing_acct_existing_devices_vgw_mac_subs_mgmt"] = "AB:CD:EF:FA:FB:01"
        tb_data["brnf_existing_acct_existing_devices_iap_lic_key"] = "E40BE7837277949D88"
        tb_data["brnf_existing_acct_existing_devices_gw_lic_key"] = "E41E6961F7A4A4CBBB"
        tb_data["brnf_existing_acct_existing_devices_sw_lic_key"] = "E83AFF772D2CB46E9A"
        tb_data["brnf_existing_acct_existing_devices_vgw_serial_no"] = "VG2109047341"
        tb_data["brnf_existing_acct_existing_devices_vgw_part_no"] = "MC-VA"
        tb_data["brnf_existing_acct_existing_devices_vgw_mac"] = "02:1A:1E:C5:7B:CC"
        tb_data["brnf_existing_acct_existing_devices_nontpm_serial_no"] = "CN29FP307G"
        tb_data["brnf_existing_acct_existing_devices_nontpm_part_no"] = "J9772A"
        tb_data["brnf_existing_acct_existing_devices_nontpm_mac"] = "00:9C:02:63:C5:00"

        tb_data["rma_devices_client_id"] = "mira-asp-test"
        tb_data["rma_devices_client_secret"] = secrets[tb_data["rma_devices_client_id"]]

        tb_data["brnf_existing_acct_new_devices_username"] = "hcloud203+zpakuhn@gmail.com"
        tb_data["brnf_existing_acct_new_devices_password"] = passwords[
            tb_data["brnf_existing_acct_new_devices_username"]]
        tb_data["brnf_existing_acct_new_devices_pcid1"] = "6f01dbdacebb11ed859e5e2881d808e7"
        tb_data["brnf_existing_acct_new_devices_pcid1_name"] = "zpakuhn-2nd company"
        tb_data["brnf_existing_acct_new_devices_pcid1_athena_f_folder"] = "athena-f-8d0f74accebb11eda74f2e23f228b9aa"
        tb_data["brnf_existing_acct_new_devices_app_instance"] = "05a2fdd2-b91e-4a02-834f-262a88b4de43"
        tb_data["brnf_existing_acct_new_devices_app_id"] = "65858496-324d-492e-b117-6cfbb10b90a4"
        tb_data["brnf_existing_acct_new_devices_app_cid"] = "8d0f74accebb11eda74f2e23f228b9aa"
        tb_data["brnf_existing_acct_new_devices_client_id"] = "swsc_client"
        tb_data["brnf_existing_acct_new_devices_client_secret"] = secrets[
            tb_data["brnf_existing_acct_new_devices_client_id"]]
        tb_data["brnf_existing_acct_new_devices_iap_lic_key"] = "EC63FE2F380634656B"
        tb_data["brnf_existing_acct_new_devices_gw_lic_key"] = "E77AEE75D79E543DAA"
        tb_data["brnf_existing_acct_new_devices_sw_lic_key"] = "EA520D4677D924431B"

        tb_data["brnf_existing_acct2_new_devices_username"] = "hcloud203+chpatzr@gmail.com"
        tb_data["brnf_existing_acct2_new_devices_password"] = passwords[
            tb_data["brnf_existing_acct2_new_devices_username"]]
        tb_data["brnf_existing_acct2_new_devices_pcid1"] = "779d097613f911eeb235ea371e477a75"
        tb_data["brnf_existing_acct2_new_devices_pcid1_name"] = "chpatzr"
        tb_data["brnf_existing_acct2_new_devices_pcid1_athena_f_folder"] = "athena-f-7fb5082013f911eebb4ddeaf5c210d4b"

        # standalone account with all app types
        tb_data['brownfield_account_with_all_app_types']['account_name'] = "jyeaept"
        tb_data['brownfield_account_with_all_app_types']['username'] = "hcloud203+jyeaept@gmail.com"
        tb_data['brownfield_account_with_all_app_types']['pcid'] = "9ce2382ef09411edb540226817358741"
        tb_data['brownfield_account_with_all_app_types']['appid_network'] = "65858496-324d-492e-b117-6cfbb10b90a4"
        tb_data["brownfield_account_with_all_app_types"][
            'app_instance_id_network'] = "37539f93-d549-458f-9731-28974c910326"
        tb_data["brownfield_account_with_all_app_types"]['acid_network'] = "af8bf046f09411ed887b0e28f2b59657"
        tb_data['brownfield_account_with_all_app_types'][
            'appid_storage_compute'] = "0fc65719-156c-46f3-b804-a65e1aa811f3"
        tb_data["brownfield_account_with_all_app_types"][
            'app_instance_id_storage_compute'] = "5432da04-5376-4ea2-84f0-e2d1effaecc2"
        tb_data["brownfield_account_with_all_app_types"]['acid_storage_compute'] = "5ad0ff80f0c911edabcf32ee7ed9cf99"

        # standalone account with only 1 Network app
        tb_data['brownfield_account_with_one_network_app']['account_name'] = "zpakuhn-2nd company"
        tb_data['brownfield_account_with_one_network_app']['username'] = "hcloud203+zpakuhn@gmail.com"
        tb_data['brownfield_account_with_one_network_app']['pcid'] = "6f01dbdacebb11ed859e5e2881d808e7"
        tb_data['brownfield_account_with_one_network_app']['appid_network'] = "65858496-324d-492e-b117-6cfbb10b90a4"
        tb_data["brownfield_account_with_one_network_app"][
            'app_instance_id_network'] = "05a2fdd2-b91e-4a02-834f-262a88b4de43"
        tb_data["brownfield_account_with_one_network_app"]["pcid1_athena_f_folder"] = \
            "athena-f-8d0f74accebb11eda74f2e23f228b9aa"
        tb_data["brownfield_account_with_one_network_app"]['acid_network'] = "8d0f74accebb11eda74f2e23f228b9aa"
        tb_data["brownfield_account_with_one_network_app"]["app_client_id"] = "swsc_client"
        tb_data["brownfield_account_with_one_network_app"]["app_client_secret"] = secrets[
            tb_data["brownfield_account_with_one_network_app"]["app_client_id"]]

        # MSP account with 3 Tenants and 1 Network app
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["account_name"] = "yaoseyz"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["username"] = "hcloud203+yaoseyz@gmail.com"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["password"] = \
            passwords[tb_data["brownfield_msp1_with_three_tenants_and_app"]["username"]]
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["app_name_network"] = "Mira nms scale app"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["app_short_name_network"] = "NGMNGM"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["appid_network"] = "65858496-324d-492e-b117-6cfbb10b90a4"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["app_instance_id_network"] = \
            "37539f93-d549-458f-9731-28974c910326"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid"] = "ce38127ce98211eda8146e64c87cfe80"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid_name"] = "yaoseyz"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["msp_acid_network"] = "d70cfd22e98211ed8f211a7438fbf301"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant1_name"] = "sm_tenant_1"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant1_pcid"] = "0d150f76eb6411edb3d5daa06241a464"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant1_acid_network"] = \
            "37b7e7dcedbf11ed9f850ab5433a2f80"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant2_name"] = "sm_tenant_2"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant2_pcid"] = "70ee089aee1611ed9f919a2cd0cb9b28"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant2_acid_network"] = \
            "7d84e966ee1611ed9a0c2e3b7148d122"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant3_name"] = "ztp_activate_account_tenant_1"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant3_pcid"] = "48da59c4eff311ed876d2235530046ab"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant3_acid_network"] = \
            "bee1104ef0ad11ed8bfc66fc7ae26d88"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_serial_subs_mgmt"] = "SMMSP001AP1"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_part_no_subs_mgmt"] = "JW242A"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_mac_subs_mgmt"] = "0A:02:03:B1:B1:01"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_lic_key"] = "EE0D458CFC9DB4B459"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_serial_subs_mgmt"] = "SMMSPSW004"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_part_no_subs_mgmt"] = "JL255A"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_mac_subs_mgmt"] = "AB:CD:EF:F8:FF:A1"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_lic_key"] = "EB914603B0BD94CAFA"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_serial_subs_mgmt"] = "SMTSTGW004"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_part_no_subs_mgmt"] = "7005-RW"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_mac_subs_mgmt"] = "AB:CD:EF:FF:FE:04"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_lic_key"] = "E97BE52E86E194A089"

        # MSP account with 1 Tenant and 1 Network app
        tb_data['brownfield_msp2_with_one_tenant_and_app']['account_name'] = "dqhmbvd"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['username'] = "hcloud203+dqhmbvd@gmail.com"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['password'] = \
            passwords[tb_data['brownfield_msp2_with_one_tenant_and_app']['username']]
        tb_data['brownfield_msp2_with_one_tenant_and_app']['appid_network'] = "65858496-324d-492e-b117-6cfbb10b90a4"
        tb_data["brownfield_msp2_with_one_tenant_and_app"][
            'app_instance_id_network'] = "37539f93-d549-458f-9731-28974c910326"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['msp_pcid'] = "1f11ced6e9e711eda9c70ab5433a2f80"
        tb_data["brownfield_msp2_with_one_tenant_and_app"]['msp_acid_network'] = "27d41b28e9e711edbc430a10745cc266"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['tenant1_name'] = "tenant_tst1"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['tenant1_pcid'] = "f11ced6e9e711eda9c70ab5433a2f80"
        tb_data["brownfield_msp2_with_one_tenant_and_app"]['tenant1_acid_network'] = "73257f84ee1711ed81ab7a0023e80d83"

        tb_data['harness_brownfield_account_parent_pcid']['account_name_parent'] = "HarnessParentAccount"
        tb_data['harness_brownfield_account_parent_pcid']['account_name_child'] = "HarnessChild1Account"
        tb_data['harness_brownfield_account_parent_pcid']['username'] = "ccsadift+brownfield_fta2@gmail.com"
        tb_data["harness_brownfield_account_parent_pcid"] = "0ab5ed0003eb11eea42042f80fb7c763"
        tb_data["harness_brownfield_account_child_pcid"] = "311149a403eb11ee9a6fc228feb99c99"

        # Account for archive related test cases
        tb_data["archive_devices_related_account"]["pcid"] = "79a846a01a4711eeac7726ddc9b0521e"
        tb_data["archive_devices_related_account"]["acid_network"] = "1172249c1a5211eea28e266d1498c05e"
        tb_data["archive_devices_related_account"]["account_name"] = "zpakuhn-3rd company"
        tb_data["archive_devices_related_account"]["username"] = "hcloud203+zpakuhn@gmail.com"

        tb_data["humio_user_token"] = passwords["humio_token"]
        # Activate Bridge
        tb_data['harness_activate_bridge']['bridge_credential_user0'] = "santosh"
        tb_data['harness_activate_bridge']['bridge_credential_user1'] = "rshettiaruba+bridge35@gmail.com"
        tb_data["harness_activate_bridge"]["bridge_credential_password0"] = passwords[tb_data["harness_activate_bridge"]["bridge_credential_user0"]]
        tb_data["harness_activate_bridge"]["bridge_credential_password1"] = passwords[tb_data["harness_activate_bridge"]["bridge_credential_user1"]]

        devices_details_path = \
            os.path.join(AUTOMATION_DIRECTORY, "configs", "devices_data", "device_files", "mira_50_devices.json")
        log.info(f"Resolved path to 'mira_50_devices.json': {devices_details_path}")
        with open(devices_details_path, "r") as mira_devices:
            tb_data["brnf_existing_acct_devices_list"] = json.load(mira_devices)
        devices_details_path = \
            os.path.join(AUTOMATION_DIRECTORY, "configs", "devices_data", "device_files",
                         "mira_3_athena_f_devices.json")
        log.info(f"Resolved path to 'mira_3_athena_f_devices.json': {devices_details_path}")
        with open(devices_details_path, "r") as mira_devices:
            tb_data["brnf_existing_acct_athena_f_devices_list"] = json.load(mira_devices)

        sm_details_path = \
            os.path.join(AUTOMATION_DIRECTORY, "configs", "devices_data", "sm_files",
                         "new_aruba_skus_iap.json")
        log.info(f"Resolved path to 'new_aruba_skus_iap.json': {sm_details_path}")
        with open(sm_details_path, "r") as sm_keys:
            tb_data["brnf_existing_acct_existing_devices_iap_new_aruba_skus"] = json.load(sm_keys)

        return tb_data
