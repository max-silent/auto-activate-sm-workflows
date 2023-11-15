import json
import logging
import os
import sys

from automation_svc_ui.constants import AUTOMATION_DIRECTORY

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.INFO)


def triton_lite_test_data(current_env, secrets, passwords):
    tb_data = {}
    tb_data["brownfield_account_with_all_app_types"] = {}
    tb_data["brownfield_account_with_one_network_app"] = {}
    tb_data["brownfield_msp1_with_three_tenants_and_app"] = {}
    tb_data["brownfield_msp2_with_one_tenant_and_app"] = {}
    if "triton-lite" in current_env:
        tb_data["url"] = current_env
        tb_data["gmail_username"] = "hcloud203@gmail.com"
        tb_data["gmail_password"] = passwords[tb_data["gmail_username"]]
        tb_data["sso_host"] = "qa-sso.ccs.arubathena.com"
        tb_data["app_api_hostname"] = "triton-lite-app-api.ccs.arubathena.com"
        tb_data[
            "ccs_activate_v1_device_url"
        ] = "triton-lite-activate-v1-device.ccs.arubathena.com"
        tb_data["gf_nw_api_client_id"] = "swsc_client"
        tb_data["gf_nw_api_client_secret"] = secrets[tb_data["gf_nw_api_client_id"]]
        tb_data["gf_nw_app_id"] = "601ad8d5-520b-4d10-ad97-40ec5ec801ba"
        tb_data["gf_nw_app_region"] = "us-west"

        tb_data["brnf_service_subs_username"] = "hcloud203+sbufuin@gmail.com"
        tb_data["brnf_service_subs_password"] = passwords[
            tb_data["brnf_service_subs_username"]
        ]
        tb_data["brnf_service_subs_pcid"] = "c0cc79f69d8411edb50a8a531f6b79ec"
        tb_data[
            "brnf_service_subs_existing_app_id"
        ] = "ba9e8972-0169-4415-993a-81a0eeb328b2"
        tb_data["brnf_service_subs_new_app_id"] = "3266d6fb-0eb8-4d76-927e-61bd495e53ce"
        tb_data["brnf_service_subs_new_region"] = "us-west"
        tb_data["brnf_service_subs_api_client_id"] = "swsc_client"
        tb_data["brnf_service_subs_api_client_secret"] = secrets[
            tb_data["brnf_service_subs_api_client_id"]
        ]

        tb_data["brnf_sc_api_client_id"] = "swsc_client"
        tb_data["brnf_sc_api_client_secret"] = secrets[tb_data["brnf_sc_api_client_id"]]
        tb_data["brnf_sc_username"] = "hcloud203+azoayyq@gmail.com"
        tb_data["brnf_sc_password"] = passwords[tb_data["brnf_sc_username"]]
        tb_data["brnf_sc_pcid"] = "b4d89adece5e11ed85c872d08b9f3bfe"
        tb_data["brnf_sc_app_instance"] = "ecb8c0dd-0da0-4bc1-b8c6-7d13ea17c93a"
        tb_data["brnf_sc_app_id"] = "127c75dd-77ab-416c-a275-943b2e638fb5"
        tb_data["brnf_sc_app_cid"] = "41e09794dfb511ed80a6ba9ae4076112"

        tb_data["brnf_existing_acct_existing_devices_api_client_id"] = "swsc_client"
        tb_data["brnf_existing_acct_existing_devices_api_client_secret"] = secrets[
            tb_data["brnf_existing_acct_existing_devices_api_client_id"]
        ]

        tb_data['brnf_existing_acct_existing_devices_username'] = "hcloud203+omedtmh@gmail.com"
        tb_data['brnf_existing_acct_existing_devices_password'] = passwords[tb_data["brnf_existing_acct_existing_devices_username"]]
        tb_data['brnf_existing_acct_existing_devices_acct1'] = "omedtmh-2nd company"
        tb_data['brnf_existing_acct_existing_devices_pcid'] = "76e67304ceb811ed99bfd257bafdd3a0"
        tb_data['brnf_existing_acct_existing_devices_appid'] = "601ad8d5-520b-4d10-ad97-40ec5ec801ba"
        tb_data['brnf_existing_acct_existing_devices_instance_id'] = "647b0340-e014-4a41-b361-06a7864c3a44"
        tb_data['brnf_existing_acct_existing_devices_acid'] = "76e67304ceb811ed99bfd257bafdd3a0"
        tb_data['brnf_existing_acct_existing_devices_iap_sn'] = "STIAPKF51R"
        tb_data['brnf_existing_acct_existing_devices_iap_mac'] = "00:00:00:3B:4E:36"
        tb_data['brnf_existing_acct_existing_devices_gw_sn'] = "STGWALNFAM"
        tb_data['brnf_existing_acct_existing_devices_gw_mac'] = "00:00:00:53:5A:13"
        tb_data['brnf_existing_acct_existing_devices_sw_sn'] = "STSWI2UOL1"
        tb_data['brnf_existing_acct_existing_devices_sw_mac'] = "00:00:00:55:91:37"
        tb_data['brnf_existing_acct_existing_devices_client_id'] = "swsc_client"
        tb_data['brnf_existing_acct_existing_devices_client_secret'] = secrets[tb_data['brnf_existing_acct_existing_devices_client_id']]
        # tb_data['brnf_existing_acct_existing_devices_client_id'] = "c82c2e24-1507-4c73-9f54-40bc6066f3fe_api"
        # tb_data['brnf_existing_acct_existing_devices_client_secret'] = secrets[tb_data['brnf_existing_acct_existing_devices_client_id']]
        tb_data['brnf_existing_acct_existing_devices_iap_lic_key'] = "E01314EBED4744453B"
        tb_data['brnf_existing_acct_existing_devices_gw_lic_key'] = "E923A0EC2128444AFB"
        tb_data['brnf_existing_acct_existing_devices_sw_lic_key'] = "EAA4BA3A3223F4AF68"
        tb_data['brnf_existing_acct_existing_devices_iap_serial_subs_mgmt'] = "STIAPCD3OH"
        tb_data['brnf_existing_acct_existing_devices_iap_part_no_subs_mgmt'] = "JW242AR"
        tb_data['brnf_existing_acct_existing_devices_iap_mac_subs_mgmt'] = "00:00:00:13:EA:74"
        tb_data['brnf_existing_acct_existing_devices_sw_serial_subs_mgmt'] = "STSWI0PNSK"
        tb_data['brnf_existing_acct_existing_devices_sw_part_no_subs_mgmt'] = "JL255A"
        tb_data['brnf_existing_acct_existing_devices_sw_mac_subs_mgmt'] = "00:00:00:22:09:66"
        tb_data['brnf_existing_acct_existing_devices_gw_serial_subs_mgmt'] = "STGWADWNVA"
        tb_data['brnf_existing_acct_existing_devices_gw_part_no_subs_mgmt'] = "7005-RW"
        tb_data['brnf_existing_acct_existing_devices_gw_mac_subs_mgmt'] = "00:00:00:EA:BB:21"

        tb_data["brnf_existing_acct_new_devices_client_id"] = "swsc_client"
        tb_data["brnf_existing_acct_new_devices_client_secret"] = secrets[tb_data["brnf_existing_acct_existing_devices_api_client_id"]]
        tb_data["brnf_existing_acct_new_devices_username"] = "hcloud203+zpakuhn@gmail.com"
        tb_data["brnf_existing_acct_new_devices_password"] = passwords[tb_data["brnf_existing_acct_new_devices_username"]]
        tb_data["brnf_existing_acct_new_devices_pcid1"] = "20f02a7acec311eda43ac293e4de9785"
        tb_data["brnf_existing_acct_new_devices_pcid1_name"] = "zpakuhn-2nd company"
        tb_data["brnf_existing_acct_new_devices_app_instance"] = "647b0340-e014-4a41-b361-06a7864c3a44"
        tb_data["brnf_existing_acct_new_devices_app_id"] = "601ad8d5-520b-4d10-ad97-40ec5ec801ba"
        tb_data["brnf_existing_acct_new_devices_app_cid"] = "4b506e92cec311eda81ae2bd9d3ef79c"

        tb_data["humio_user_token"] = passwords["humio_token"]

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

        tb_data["humio_user_token"] = passwords["humio_token"]

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
