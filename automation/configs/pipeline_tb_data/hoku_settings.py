def hoku_test_data(current_env, secrets, passwords):
    tb_data = {}
    if "hoku" in current_env:
        tb_data["url"] = current_env

        tb_data["gmail_username"] = "hcloud203@gmail.com"
        tb_data["gmail_password"] = passwords[tb_data["gmail_username"]]
        tb_data["sso_host"] = "qa-sso.ccs.arubathena.com"
        tb_data[
            "ccs_activate_v1_device_url"
        ] = "hoku-activate-v1-device.ccs.arubathena.com"
        tb_data["gf_nw_api_client_id"] = "f387b93c-1474-4ddf-b837-2976aec18ac4_api"
        tb_data["gf_nw_api_client_secret"] = secrets[tb_data["gf_nw_api_client_id"]]
        tb_data["gf_nw_app_id"] = "df5b41c4-7c35-4158-af63-302042b9911b"
        tb_data["gf_nw_app_region"] = "us-west"

        tb_data["rma_devices_client_id"] = "hoku-asp-test"
        tb_data["rma_devices_client_secret"] = secrets[tb_data["rma_devices_client_id"]]

        tb_data["username"] = "hcloud203+vypkkjt@gmail.com"
        tb_data["password"] = passwords[tb_data["username"]]
        tb_data["acct_name"] = "vypkkjt-acct-1"
        tb_data["sm_username"] = "glcpqa.scale+user102432@gmail.com"
        tb_data["sm_password"] = passwords[tb_data["sm_username"]]
        tb_data["sm_acct_name"] = "Xilinx Inc"
        tb_data["api_auth_client_id"] = "f387b93c-1474-4ddf-b837-2976aec18ac4_api"
        tb_data["api_auth_client_secret"] = secrets[tb_data["api_auth_client_id"]]
        tb_data["gmail_username"] = "hcloud203@gmail.com"
        tb_data["gmail_password"] = passwords[tb_data["gmail_username"]]
        tb_data["gf_app_id"] = "df5b41c4-7c35-4158-af63-302042b9911b"
        tb_data["gf_region"] = "us-west"
        tb_data["sso_host"] = "qa-sso.ccs.arubathena.com"
        tb_data['brnf_existing_devices_username'] = "hcloud203+lvkauji@gmail.com"
        tb_data['brnf_existing_devices_password'] = passwords[tb_data["brnf_existing_devices_username"]]
        tb_data['brnf_existing_devices_acct1'] = "lvkauji Company"
        tb_data['brnf_existing_devices_pcid'] = "c5453a7cc9da11edac8e5a13adafad1f"
        tb_data['brnf_existing_devices_appid'] = "df5b41c4-7c35-4158-af63-302042b9911b"
        tb_data['brnf_existing_devices_instance_id'] = "f387b93c-1474-4ddf-b837-2976aec18ac4"
        tb_data['brnf_existing_devices_acid'] = "519ace8ac9de11eda4227e19dad5996f"
        tb_data['brnf_existing_devices_iap_sn'] = "STIAPUCS8J"
        tb_data['brnf_existing_devices_gw_sn'] = "STGWA3QT2X"
        tb_data['brnf_existing_devices_sw_sn'] = "STSWIWZAEA"
        tb_data['brnf_existing_devices_iap_lic_key'] = "E78D9E53746F54F38A"
        tb_data['brnf_existing_devices_gw_lic_key'] = "E74EB4955DD7B42D5A"
        tb_data['brnf_existing_devices_sw_lic_key'] = "ED30F05FE24EB4F39B"
        return tb_data

