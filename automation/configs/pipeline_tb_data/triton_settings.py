def triton_test_data(current_env, secrets, passwords):
    tb_data = {}
    if "triton" in current_env:
        tb_data["url"] = current_env
        tb_data["username"] = "hcloud203+vypkkjt@gmail.com"
        tb_data["password"] = passwords[tb_data["username"]]
        tb_data["acct_name"] = "vypkkjt-acct-1"
        tb_data["sm_acct_name"] = "pavo-sanity-sm"
        tb_data["sm_pcid"] = "3900efa2286911ec96e3d26354c40014"
        tb_data["sm_ap_lic"] = "E50E2C07E0A2E4B2E8"
        tb_data["sm_ap_sn"] = "CO9T4WJQ6S"
        tb_data["sm_ap_dev_type"] = "IAP"
        tb_data["sm_ap_part_number"] = "JW242AR"
        tb_data["sm_app_id"] = "405e2be8-da21-44b9-bbb4-dedf5c437fd1"
        tb_data["sm_region"] = "us-west"
        tb_data["activate_folder_name"] = "folder51"
        tb_data["activate_folder_dev_sn"] = "6TOOAE34RE"
        tb_data["msp_username"] = "admin@frontendauto.com"
        tb_data["msp_password"] = passwords[tb_data["msp_username"]]
        tb_data["msp_acct_name"] = "turid12"
        tb_data["msp_acct_name_2"] = "turid+zqz"
        tb_data["authz_username"] = "hcloud203+yrqsxse@gmail.com"
        tb_data["authz_password"] = passwords[tb_data["authz_username"]]
        tb_data["authz_pcid1"] = "yrqsxse"
        tb_data["authz_pcid2"] = "yrqsxse-acct-1"
        tb_data["di_username"] = "hcloud203+gtvwfqf@gmail.com"
        tb_data["di_password"] = passwords[tb_data["di_username"]]
        tb_data["di_acct_name"] = "gtvwfqf"
        tb_data["di_pcid"] = "2c34d2aaf7d711ec82232627647e7489"
        tb_data["di_app_name"] = "ST_NMS_devices_app"
        tb_data["di_ap_lic"] = "EA7E740B7DAD74475B"
        tb_data["di_ap_sn"] = "STIAPTNXOV"
        tb_data["di_ap_dev_type"] = "IAP"
        tb_data["di_ap_part_number"] = "JW242AR"
        tb_data["aop_client_id"] = "13e94c56-ef52-4d01-9710-47e158e2cc21_api"
        tb_data["aop_client_secret"] = secrets[tb_data["aop_client_id"]]
        tb_data["api_auth_client_id"] = "13e94c56-ef52-4d01-9710-47e158e2cc21_api"
        tb_data["api_auth_client_secret"] = secrets[tb_data["api_auth_client_id"]]
        tb_data["sso_host"] = "qa-sso.ccs.arubathena.com"
        tb_data["app_api_hostname"] = "triton-lite-app-api.ccs.arubathena.com"
        tb_data["brn_fld_sa_username"] = "hcloud203+zrctivv@gmail.com"
        tb_data["brn_fld_sa_password"] = passwords[tb_data["brn_fld_sa_username"]]
        tb_data["brn_fld_sa_pcid"] = "e069bc56962c11ed8fcc5662539ff115"
        tb_data["brn_fld_sa_nms_app_instance"] = "c82c2e24-1507-4c73-9f54-40bc6066f3fe"
        tb_data["brn_fld_sa_nms_app_id"] = "405e2be8-da21-44b9-bbb4-dedf5c437fd1"
        tb_data["brn_fld_sa_nms_app_cid"] = "f44bb9e0962c11edaaf6723ddadb3227"
        tb_data["brn_fld_sa_sc_pcid"] = "ba1e640a987711ed8017569a4c8587c0"
        tb_data["brn_fld_sa_sc_app_instance"] = "ecb8c0dd-0da0-4bc1-b8c6-7d13ea17c93a"
        tb_data["brn_fld_sa_sc_app_id"] = "127c75dd-77ab-416c-a275-943b2e638fb5"
        tb_data["brn_fld_sa_sc_app_cid"] = "0fcda924987811edaba70e84ce0b78ff"
        tb_data["ccs_device_url"] = "triton-lite-device.ccs.arubathena.com"
        tb_data[
            "ccs_activate_v1_device_url"
        ] = "triton-lite-activate-v1-device.ccs.arubathena.com"
        tb_data[
            "ccs_activate_v2_device_url"
        ] = "triton-lite-activate-v2-device.ccs.arubathena.com"
        tb_data["gmail_username"] = "hcloud203@gmail.com"
        tb_data["gmail_password"] = passwords[tb_data["gmail_username"]]

        tb_data["humio_user_token"] = passwords["humio_token"]

        tb_data["brnf_existing_acct_existing_devices_client_id"] = "13e94c56-ef52-4d01-9710-47e158e2cc21_api"
        tb_data["brnf_existing_acct_existing_devices_client_secret"] = secrets[
            tb_data["brnf_existing_acct_existing_devices_client_id"]]
        tb_data["harness_brownfield_account_parent_pcid"] = "08300c1251ab11ec84290e1dba8b8e00"
        tb_data["harness_brownfield_account_child_pcid"] = "2bc33caa51a911ecb0f70e1dba8b8e00"

        return tb_data
