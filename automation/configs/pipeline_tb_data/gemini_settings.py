def gemini_test_data(current_env, secrets, passwords):
    tb_data = {}
    if "gemini" in current_env:
        tb_data["url"] = current_env
        tb_data["username"] = "hcloud203+vypkkjt@gmail.com"
        tb_data["password"] = passwords[tb_data["username"]]
        tb_data["acct_name"] = "vypkkjt-acct-1"
        tb_data["sm_username"] = "glcpqa.scale+user102432@gmail.com"
        tb_data["sm_password"] = passwords[tb_data["sm_username"]]
        tb_data["sm_acct_name"] = "Xilinx Inc"
        tb_data["aop_client_id"] = "727c1252-384d-4818-a554-d8b3077f460f_api"
        tb_data["aop_client_secret"] = secrets[tb_data["aop_client_id"]]
        tb_data["gmail_username"] = "hcloud203@gmail.com"
        tb_data["gmail_password"] = passwords[tb_data["gmail_username"]]
        tb_data['brnf_existing_devices_username'] = "hcloud203+lvkauji@gmail.com"
        tb_data['brnf_existing_devices_password'] = passwords[tb_data["brnf_existing_devices_username"]]
        tb_data['brnf_existing_devices_acct1'] = "lvkauji Company"
        tb_data['brnf_existing_devices_pcid'] = "9858de56beae11ed82994264c78024fb"
        tb_data['brnf_existing_devices_appid'] = "da85d9ba-05dc-490c-b615-469927c01a2f"
        tb_data['brnf_existing_devices_instance_id'] = "1f8b0002-8d95-4416-a123-e93f3bf2cded"
        tb_data['brnf_existing_devices_acid'] = "3f763a2cbf1211ed88eb1ee96942aeed"
        tb_data['brnf_existing_devices_iap_sn'] = "STIAPV8DX3"
        tb_data['brnf_existing_devices_gw_sn'] = "STGWADOVI6"
        tb_data['brnf_existing_devices_sw_sn'] = "STSWIEZK4J"
        tb_data['brnf_existing_devices_iap_lic_key'] = "E9271F08B7ACF4586A"
        tb_data['brnf_existing_devices_gw_lic_key'] = "EEDCB236ADE784A938"
        tb_data['brnf_existing_devices_sw_lic_key'] = "EF3E88F76D45F444CB"
        return tb_data
