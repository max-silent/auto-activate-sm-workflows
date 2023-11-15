def aquila_test_data(current_env, secrets, passwords):
    tb_data = {}
    if "aquila" in current_env:
        tb_data["url"] = current_env
        tb_data["username"] = "hcloud203+usfampv@gmail.com"
        tb_data["password"] = passwords[tb_data["username"]]
        tb_data["acct_name"] = "acct_mgmt_tst1"
        tb_data["sm_username"] = "hcloud203+aqsanity@gmail.com"
        tb_data["sm_password"] = passwords[tb_data["sm_username"]]
        tb_data["sm_acct_name"] = "sanity acct1"
        tb_data["sm_pcid"] = "b64c92aeeefd11eb8a56fe3eeefe00a6"
        tb_data["sm_ap_lic"] = "E50E13889608240F79"
        tb_data["sm_ap_sn"] = "5J9HHN2G1U"
        tb_data["sm_ap_dev_type"] = "IAP"
        tb_data["sm_ap_part_number"] = "JW242AR"
        tb_data["activate_folder_name"] = "folder51"
        tb_data["activate_folder_dev_sn"] = "3J4ZA8Z0NR"
        tb_data["authz_username"] = "hcloud203+yrqsxse@gmail.com"
        tb_data["authz_password"] = passwords[tb_data["authz_username"]]
        tb_data["authz_pcid1"] = "yrqsxse"
        tb_data["authz_pcid2"] = "yrqsxse-acct-1"
        tb_data["sso_host"] = "sso.common.cloud.hpe.com"
        tb_data["api_auth_client_id"] = "swsc_client"
        tb_data["api_auth_client_secret"] = secrets[tb_data["api_auth_client_id"]]
        tb_data["app_api_hostname"] = "aquila-app-api.common.cloud.hpe.com"
        tb_data["gmail_username"] = "hcloud203@gmail.com"
        tb_data["gmail_password"] = passwords[tb_data["gmail_username"]]
        tb_data["brnf_existing_devices_username"] = "hcloud203+pudyuag@gmail.com"
        tb_data["brnf_existing_devices_password"] = passwords[
            tb_data["brnf_existing_devices_username"]
        ]
        tb_data["brnf_existing_devices_acct1"] = "pudyuag Company"
        tb_data["brnf_existing_devices_pcid"] = "d0655994ba4111ed88d8327445eb9742"
        tb_data["brnf_existing_devices_appid"] = "683da368-66cb-4ee7-90a9-ec1964768092"
        tb_data[
            "brnf_existing_devices_instance_id"
        ] = "3c450d6a-2cb8-4d4c-893b-c336903a5cea"
        tb_data["brnf_existing_devices_acid"] = "39a9a68aba4211eda088ae42110b9bb2"
        tb_data["brnf_existing_devices_iap_sn"] = "82UEB1LPIO"
        tb_data["brnf_existing_devices_gw_sn"] = "XF94CYGZVP"
        tb_data["brnf_existing_devices_sw_sn"] = "BPZK75N72C"
        tb_data["brnf_existing_devices_iap_lic_key"] = "E269737FA9F8C4DA8A"
        tb_data["brnf_existing_devices_gw_lic_key"] = "EAAB36D4455824C9DA"
        tb_data["brnf_existing_devices_sw_lic_key"] = "E75C062504FAD48D49"
        return tb_data
