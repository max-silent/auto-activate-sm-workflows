import json
import logging
import os
import sys

from automation.constants import AUTOMATION_DIRECTORY

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.INFO)


def polaris_test_data(current_env, secrets, passwords):
    tb_data = {}
    tb_data['brownfield_account_with_all_app_types'] = {}
    tb_data['brownfield_account_with_one_network_app'] = {}
    tb_data["brownfield_msp1_with_three_tenants_and_app"] = {}
    tb_data['brownfield_msp2_with_one_tenant_and_app'] = {}
    tb_data['harness_brownfield_account_parent_pcid'] = {}
    tb_data["archive_devices_related_account"] = {}
    tb_data["harness_activate_bridge"] = {}

    if "polaris" in current_env:
        tb_data["url"] = current_env
        tb_data["gmail_username"] = "hcloud203@gmail.com"
        tb_data["gmail_password"] = passwords[tb_data["gmail_username"]]
        tb_data["sso_host"] = "qa-sso.ccs.arubathena.com"
        tb_data[
            "ccs_activate_v1_device_url"
        ] = "polaris-activate-v1-device-ccs.arubathena.com"
        tb_data["app_api_hostname"] = "polaris-default-app-api.ccs.arubathena.com"

        tb_data["gf_nw_api_client_id"] = "af4a9915-f274-44bc-b665-b75e8e131bc0_api"
        tb_data["gf_nw_api_client_secret"] = secrets[tb_data["gf_nw_api_client_id"]]
        tb_data["gf_nw_app_id"] = "17c23735-f960-4b85-9cc2-610a4fae617d"
        tb_data["gf_nw_app_region"] = "us-west"

        tb_data["brnf_service_subs_username"] = "hcloud203+sbufuin@gmail.com"
        tb_data["brnf_service_subs_password"] = passwords[tb_data["brnf_service_subs_username"]]
        tb_data["brnf_service_subs_pcid"] = "0f431d1a061c11ee86e6c27ce94978db"
        tb_data["brnf_service_subs_acid"] = "87419856062011ee8c4f5ab9cdf1d133"
        tb_data["brnf_service_subs_existing_app_id"] = "2e7bbe69-a40f-4398-948e-e5085f7c1c35"
        tb_data["brnf_service_subs_new_app_id"] = "826b4b95-90a1-4ccc-87b6-afca60c8c07e"
        tb_data["brnf_service_subs_new_region"] = "us-west"
        tb_data["brnf_service_subs_api_client_id"] = "2293390f-bf8b-47fd-b26b-b5d3a31b21cd_api"
        tb_data["brnf_service_subs_api_client_secret"] = secrets[tb_data["brnf_service_subs_api_client_id"]]

        tb_data["rma_devices_client_id"] = "polaris-asp-test"
        tb_data["rma_devices_client_secret"] = secrets[tb_data["rma_devices_client_id"]]

        tb_data["brnf_sc_api_client_id"] = "107f7193-a6f9-4b54-96c4-beddbcbac743_api"
        tb_data["brnf_sc_api_client_secret"] = secrets[tb_data["brnf_sc_api_client_id"]]
        tb_data["brnf_sc_username"] = "hcloud203+azoayyq@gmail.com"
        tb_data["brnf_sc_password"] = passwords[tb_data["brnf_sc_username"]]
        tb_data["brnf_sc_pcid"] = "dc16a5f4cebe11ed856592c18bd6cb96"
        tb_data["brnf_sc_pcid_name"] = "azoayyq-2nd company"
        tb_data["brnf_sc_app_instance"] = "107f7193-a6f9-4b54-96c4-beddbcbac743"
        tb_data["brnf_sc_app_id"] = "2e7bbe69-a40f-4398-948e-e5085f7c1c35"
        tb_data["brnf_sc_app_cid"] = "4252ecb0e4c211edb2fd6666e59cb4cf"
        tb_data["brnf_sc_compute_serial_subs_mgmt"] = "SMCMPTO01"
        tb_data["brnf_sc_compute_partnumber_subs_mgmt"] = "R6Z88AAE"
        tb_data["brnf_sc_storage_serial_subs_mgmt"] = "SMBAASTST1"
        tb_data["brnf_sc_storage_partnumber_subs_mgmt"] = "BAASTESTVIJAY1"

        tb_data["tac_admin_username"] = "glcpqa.scale+user102432@gmail.com"
        tb_data["tac_admin_password"] = \
            passwords[tb_data["tac_admin_username"]]
        tb_data["tac_admin_pcid1"] = "6ce6e470127511ecaac2669a948ce83d"
        tb_data["tac_admin_pcid1_name"] = "HPE GreenLake Support"
        tb_data["tac_existing_acct_existing_devices_username"] = "hcloud203+cqsqigh@gmail.com"
        tb_data["tac_existing_acct_existing_devices_password"] = \
            passwords[tb_data["tac_existing_acct_existing_devices_username"]]
        tb_data["tac_existing_acct_existing_devices_pcid1"] = "abe6574ed48b11ed8575161c34e374c8"
        tb_data["tac_existing_acct_existing_devices_pcid1_name"] = "cqsqigh"
        tb_data["tac_existing_acct_existing_devices_pcid1_athena_f_folder"] = \
            "athena-f-bb61b6d2d48b11eda1e9d2690d53741a"
        tb_data["tac_existing_acct_existing_devices_pcid1_iap_sn"] = "STIAP0HPAA"
        tb_data["tac_existing_acct_existing_devices_pcid1_iap_part_no"] = "IAP-225-US"
        tb_data["tac_existing_acct_existing_devices_pcid1_iap_mac"] = "00:00:00:57:71:07"
        tb_data["tac_existing_acct_existing_devices_pcid1_gw_sn"] = "STGWAPO9E6"
        tb_data["tac_existing_acct_existing_devices_pcid1_gw_part_no"] = "7005-RW"
        tb_data["tac_existing_acct_existing_devices_pcid1_gw_mac"] = "00:00:00:BE:B8:02"
        tb_data["tac_existing_acct_existing_devices_pcid1_sw_sn"] = "STSWIYL0VW"
        tb_data["tac_existing_acct_existing_devices_pcid1_sw_part_no"] = "2930F"
        tb_data["tac_existing_acct_existing_devices_pcid1_sw_mac"] = "00:00:00:E3:11:86"
        tb_data["tac_existing_acct_existing_devices_pcid1_iap_eval_subs_key_assigned"] = "E6B3FD04DAEEB46F18"
        tb_data["tac_existing_acct_existing_devices_pcid1_gw_brim_subs_key_assigned"] = "COGATEWAYCMEUPAPS14"
        tb_data["tac_existing_acct_existing_devices_pcid1_sw_brim_subs_key"] = "CTHSWITCHCMEUPAPS14"
        tb_data["tac_existing_acct_existing_devices_pcid1_service_brim_subs_key"] = "FLSP6SERTEST001"

        tb_data["brnf_existing_acct_existing_devices_username"] = "hcloud203+omedtmh@gmail.com"
        tb_data["brnf_existing_acct_existing_devices_password"] = passwords[
            tb_data["brnf_existing_acct_existing_devices_username"]]
        tb_data["brnf_existing_acct_existing_devices_acct1"] = "omedtmh-2nd company"
        tb_data["brnf_existing_acct_existing_devices_pcid"] = "25b5fce0cea711edb248263655e67ae4"
        tb_data["brnf_existing_acct_existing_devices_appid"] = "3bd7988b-5cdb-4377-8d6a-6c5972a1694f"
        tb_data["brnf_existing_acct_existing_devices_instance_id"] = "acbb0e91-6f63-4370-a31e-6419265b9be8"
        tb_data["brnf_existing_acct_existing_devices_acid"] = "7f81c746ceab11edb40d16d8833a9563"

        tb_data['harness_brownfield_account_parent_pcid']['account_name_parent'] = "HarnessParentAccount"
        tb_data['harness_brownfield_account_parent_pcid']['account_name_child'] = "HarnessChild1Account"
        tb_data['harness_brownfield_account_parent_pcid']['username'] = "ccsadift+brownfield_fta2@gmail.com"
        tb_data["harness_brownfield_account_parent_pcid"] = "44a902da03ec11ee81bcda6c11fbc7e5"
        tb_data["harness_brownfield_account_child_pcid"] = "5f83372e03ec11eeb831fa726de74704"

        # comp
        tb_data["brnf_existing_acct_existing_devices_comp_appid"] = "2e7bbe69-a40f-4398-948e-e5085f7c1c35"
        tb_data["brnf_existing_acct_existing_devices_comp_instance_id"] = "107f7193-a6f9-4b54-96c4-beddbcbac743"
        tb_data["brnf_existing_acct_existing_devices_comp_acid"] = "4252ecb0e4c211edb2fd6666e59cb4cf"
        tb_data["brnf_existing_acct_existing_devices_iap_sn"] = "STIAPVN699"
        tb_data["brnf_existing_acct_existing_devices_iap_mac"] = "00:00:00:23:5A:94"
        tb_data["brnf_existing_acct_existing_devices_gw_sn"] = "STGWAMGQF4"
        tb_data["brnf_existing_acct_existing_devices_gw_mac"] = "00:00:00:7D:73:05"
        tb_data["brnf_existing_acct_existing_devices_sw_sn"] = "STSWIOOJND"
        tb_data["brnf_existing_acct_existing_devices_sw_mac"] = "00:00:00:BF:5A:9F"
        tb_data["brnf_existing_acct_existing_devices_comp_sn"] = "STCOMSER1"
        tb_data["brnf_existing_acct_existing_devices_comp_mac"] = "02:2E:91:F2:B8:E2"
        tb_data["brnf_existing_acct_existing_devices_comp_part"] = "STCOMPT1"
        tb_data["brnf_existing_acct_existing_devices_client_id"] = "swsc_client"
        tb_data["brnf_existing_acct_existing_devices_client_secret"] = secrets[
            tb_data["brnf_existing_acct_existing_devices_client_id"]]
        tb_data["brnf_existing_acct_existing_devices_iap_serial_subs_mgmt"] = "STIAPFHIAF"
        tb_data["brnf_existing_acct_existing_devices_iap_part_no_subs_mgmt"] = "JW242AR"
        tb_data["brnf_existing_acct_existing_devices_iap_mac_subs_mgmt"] = "00:00:00:2A:2C:E5"
        tb_data["brnf_existing_acct_existing_devices_sw_serial_subs_mgmt"] = "STSWISSN40"
        tb_data["brnf_existing_acct_existing_devices_sw_part_no_subs_mgmt"] = "JL255A"
        tb_data["brnf_existing_acct_existing_devices_sw_mac_subs_mgmt"] = "00:00:00:34:18:92"
        tb_data["brnf_existing_acct_existing_devices_gw_serial_subs_mgmt"] = "STGWAYU1XO"
        tb_data["brnf_existing_acct_existing_devices_gw_part_no_subs_mgmt"] = "7005-RW"
        tb_data["brnf_existing_acct_existing_devices_gw_mac_subs_mgmt"] = "00:00:00:25:70:1A"
        tb_data["brnf_existing_acct_existing_devices_vgw_serial_subs_mgmt"] = "SMVGWTST01"
        tb_data["brnf_existing_acct_existing_devices_vgw_part_no_subs_mgmt"] = "MC-VA"
        tb_data["brnf_existing_acct_existing_devices_vgw_mac_subs_mgmt"] = "AB:CD:EF:FA:FB:01"
        tb_data["brnf_existing_acct_existing_devices_iap_lic_key"] = "EC182AE890C2B4ECAA"
        tb_data["brnf_existing_acct_existing_devices_gw_lic_key"] = "EADACCA1B6FC9483CA"
        tb_data["brnf_existing_acct_existing_devices_sw_lic_key"] = "EB88C200022A14C278"
        tb_data["brnf_existing_acct_existing_devices_vgw_serial_no"] = "VG2109047341"
        tb_data["brnf_existing_acct_existing_devices_vgw_part_no"] = "MC-VA"
        tb_data["brnf_existing_acct_existing_devices_vgw_mac"] = "02:1A:1E:C5:7B:CC"
        tb_data["brnf_existing_acct_existing_devices_nontpm_serial_no"] = "CN29FP307G"
        tb_data["brnf_existing_acct_existing_devices_nontpm_part_no"] = "J9772A"
        tb_data["brnf_existing_acct_existing_devices_nontpm_mac"] = "00:9C:02:63:C5:00"

        tb_data["brnf_existing_acct_new_devices_client_id"] = "swsc_client"
        tb_data["brnf_existing_acct_new_devices_client_secret"] = secrets[
            tb_data["brnf_existing_acct_new_devices_client_id"]]
        tb_data["brnf_existing_acct_new_devices_username"] = "hcloud203+zpakuhn@gmail.com"
        tb_data["brnf_existing_acct_new_devices_password"] = passwords[
            tb_data["brnf_existing_acct_new_devices_username"]]
        tb_data["brnf_existing_acct_new_devices_pcid1"] = "fd0e08fecebb11edb0b5263655e67ae4"
        tb_data["brnf_existing_acct_new_devices_pcid1_name"] = "zpakuhn-2nd company"
        tb_data["brnf_existing_acct_new_devices_pcid1_athena_f_folder"] = "athena-f-72227fd0cebc11ed9891befcefcd678c"
        tb_data["brnf_existing_acct_new_devices_app_instance"] = "8592e513-df73-4879-9dc6-429d78a1f2d5"
        tb_data["brnf_existing_acct_new_devices_app_id"] = "01e69890-a875-429f-a08b-1ef55a394f93"
        tb_data["brnf_existing_acct_new_devices_app_cid"] = "72227fd0cebc11ed9891befcefcd678c"
        tb_data["brnf_existing_acct_new_devices_iap_lic_key"] = "E4BC7B43E20804215A"
        tb_data["brnf_existing_acct_new_devices_gw_lic_key"] = "EF7B32B46FA8B4A8DB"
        tb_data["brnf_existing_acct_new_devices_sw_lic_key"] = "EDD6B46948615403E9"

        tb_data["brnf_existing_acct2_new_devices_username"] = "hcloud203+xjuciaf@gmail.com"
        tb_data["brnf_existing_acct2_new_devices_password"] = passwords[
            tb_data["brnf_existing_acct2_new_devices_username"]]
        tb_data["brnf_existing_acct2_new_devices_pcid1"] = "1fb4a786112f11ee880f26d6fe2a078d"
        tb_data["brnf_existing_acct2_new_devices_pcid1_name"] = "xjuciaf"
        tb_data["brnf_existing_acct2_new_devices_pcid1_athena_f_folder"] = "athena-f-2956cd5a112f11ee9ea2661bf5929560"

        # standalone account with all app types
        tb_data['brownfield_account_with_all_app_types']['account_name'] = "eptxyxf"
        tb_data['brownfield_account_with_all_app_types']['username'] = "hcloud203+eptxyxf@gmail.com"
        tb_data['brownfield_account_with_all_app_types']['pcid'] = "cb8d6b52f0d111edad4f0e59b93c1532"
        tb_data['brownfield_account_with_all_app_types']['appid_network'] = "3bd7988b-5cdb-4377-8d6a-6c5972a1694f"
        tb_data["brownfield_account_with_all_app_types"][
            'app_instance_id_network'] = "acbb0e91-6f63-4370-a31e-6419265b9be8"
        tb_data["brownfield_account_with_all_app_types"]['acid_network'] = "d3e8bfbaf0d411ed871f92aca8541e6a"
        tb_data['brownfield_account_with_all_app_types'][
            'appid_storage_compute'] = "2e7bbe69-a40f-4398-948e-e5085f7c1c35"
        tb_data["brownfield_account_with_all_app_types"][
            'app_instance_id_storage_compute'] = "107f7193-a6f9-4b54-96c4-beddbcbac743"
        tb_data["brownfield_account_with_all_app_types"]['acid_storage_compute'] = "54d6b8acf0d511edaf4f6a1a072de6c7"

        # standalone account with only 1 Network app
        tb_data['brownfield_account_with_one_network_app']['account_name'] = "coeuyid"
        tb_data['brownfield_account_with_one_network_app']['username'] = "hcloud203+coeuyid@gmail.com"
        tb_data['brownfield_account_with_one_network_app']['pcid'] = "317c6d32f0d211edba81425353b91f50"
        tb_data['brownfield_account_with_one_network_app']['appid_network'] = "3bd7988b-5cdb-4377-8d6a-6c5972a1694f"
        tb_data["brownfield_account_with_one_network_app"][
            'app_instance_id_network'] = "acbb0e91-6f63-4370-a31e-6419265b9be8"
        tb_data["brownfield_account_with_one_network_app"]['acid_network'] = "a51f7bfef0d611ed9c584a29996d971e"

        # MSP account with 3 Tenants and 1 Network app
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["account_name"] = "yaoseyz"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["username"] = "hcloud203+yaoseyz@gmail.com"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["password"] = \
            passwords[tb_data["brownfield_msp1_with_three_tenants_and_app"]["username"]]
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["app_name_network"] = "Local_ST NMSP APP"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["app_short_name_network"] = "STLNMSP"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["appid_network"] = "17c23735-f960-4b85-9cc2-610a4fae617d"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["app_instance_id_network"] = \
            "af4a9915-f274-44bc-b665-b75e8e131bc0"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid"] = "b9816634ee2e11ed8be5ce1dd1c0b808"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["msp_pcid_name"] = "yaoseyz"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["msp_acid_network"] = "07d6fa42ee2f11ed9afde2d97ed83ed7"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant1_name"] = "sm_tenant_1"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant1_pcid"] = "17212f72ee2f11eda07bdaa4a61562ff"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant1_acid_network"] = \
            "2f41a9baee2f11edb45b121ffdb4fbde"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant2_name"] = "sm_tenant_2"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant2_pcid"] = "1ffcfc3eee2f11ed9043866735c2f602"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant2_acid_network"] = \
            "82fddb82ee2f11ed807c8214deba95d0"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant3_name"] = "ztp_activate_account_tenant_1"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant3_pcid"] = "1098d578f3c611ed9139b238773fc8a4"
        tb_data["brownfield_msp1_with_three_tenants_and_app"]["tenant3_acid_network"] = \
            "69ec6bd0f3c611eda2c7d2f847c9add2"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_serial_subs_mgmt"] = "SMMSPAP004"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_part_no_subs_mgmt"] = "JW242AR"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_mac_subs_mgmt"] = "01:02:03:A1:B1:B1"
        tb_data["brownfield_msp1_with_three_tenants_and_app_iap_lic_key"] = "EF18D8C5ED8C84A9D9"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_serial_subs_mgmt"] = "SMMSPSW004"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_part_no_subs_mgmt"] = "JL255A"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_mac_subs_mgmt"] = "AB:CD:EF:F8:FF:A1"
        tb_data["brownfield_msp1_with_three_tenants_and_app_sw_lic_key"] = "EC82A4412DD5B4E008"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_serial_subs_mgmt"] = "SMTSTGW004"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_part_no_subs_mgmt"] = "7005-RW"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_mac_subs_mgmt"] = "AB:CD:EF:FF:FE:04"
        tb_data["brownfield_msp1_with_three_tenants_and_app_gw_lic_key"] = "E9B3F9E6A90084F8E9"

        # MSP account with 1 Tenant and 1 Network app
        tb_data['brownfield_msp2_with_one_tenant_and_app']['account_name'] = "dqhmbvd"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['username'] = "hcloud203+dqhmbvd@gmail.com"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['password'] = \
            passwords[tb_data['brownfield_msp2_with_one_tenant_and_app']['username']]
        tb_data['brownfield_msp2_with_one_tenant_and_app']['appid_network'] = "17c23735-f960-4b85-9cc2-610a4fae617d"
        tb_data["brownfield_msp2_with_one_tenant_and_app"][
            'app_instance_id_network'] = "af4a9915-f274-44bc-b665-b75e8e131bc0"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['msp_pcid'] = "af4a9915-f274-44bc-b665-b75e8e131bc0"
        tb_data["brownfield_msp2_with_one_tenant_and_app"]['msp_acid_network'] = "63391672ee2a11ed97337ea8c97cca35"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['tenant1_name'] = "tenant_tst1"
        tb_data['brownfield_msp2_with_one_tenant_and_app']['tenant1_pcid'] = "6b4d4138ee3111edb03d82bc6c1a034b"
        tb_data["brownfield_msp2_with_one_tenant_and_app"]['tenant1_acid_network'] = "73ee7e10ee3111ed9804b26dfa60b8bb"

        # Account for archive related test cases
        tb_data["archive_devices_related_account"]["pcid"] = "8765d97a175d11eeb342b6498c07eb4c"
        tb_data["archive_devices_related_account"]["acid_network"] = "7e29accc1a5211eead37d6e54e7a42ca"
        tb_data["archive_devices_related_account"]["account_name"] = "zpakuhn-3rd company"
        tb_data["archive_devices_related_account"]["username"] = "hcloud203+zpakuhn@gmail.com"

        tb_data["humio_user_token"] = passwords["humio_token"]
        # Activate Bridge
        tb_data['harness_activate_bridge']['bridge_credential_user0'] = "santosh"
        tb_data['harness_activate_bridge']['bridge_credential_user1'] = "ccsadift+brownfield_fta2@gmail.com"
        tb_data["harness_activate_bridge"]["bridge_credential_password0"] = passwords[tb_data["harness_activate_bridge"]["bridge_credential_user0"]]
        tb_data["harness_activate_bridge"]["bridge_credential_password1"] = passwords[tb_data["harness_activate_bridge"]["bridge_credential_user1"]]

        devices_details_path = \
            os.path.join(AUTOMATION_DIRECTORY, "configs", "devices_data", "device_files", "polaris_50_devices.json")
        log.info(f"Resolved path to 'polaris_50_devices.json': {devices_details_path}")
        with open(devices_details_path, "r") as polaris_devices:
            tb_data["brnf_existing_acct_devices_list"] = json.load(polaris_devices)
        devices_details_path = \
            os.path.join(AUTOMATION_DIRECTORY, "configs", "devices_data", "device_files",
                         "polaris_3_athena_f_devices.json")
        log.info(f"Resolved path to 'polaris_3_athena_f_devices.json': {devices_details_path}")
        with open(devices_details_path, "r") as polaris_devices:
            tb_data["brnf_existing_acct_athena_f_devices_list"] = json.load(polaris_devices)

        sm_details_path = \
            os.path.join(AUTOMATION_DIRECTORY, "configs", "devices_data", "sm_files",
                         "new_aruba_skus_iap.json")
        log.info(f"Resolved path to 'new_aruba_skus_iap.json': {sm_details_path}")
        with open(sm_details_path, "r") as sm_keys:
            tb_data["brnf_existing_acct_existing_devices_iap_new_aruba_skus"] = json.load(sm_keys)

        return tb_data
