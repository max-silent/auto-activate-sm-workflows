import json
import logging
import os
import sys

from automation.constants import AUTOMATION_DIRECTORY

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.INFO)


def glcphf_test_data(current_env, secrets, passwords):
    tb_data = {}
    tb_data['brownfield_account_with_all_app_types'] = {}
    tb_data['brownfield_account_with_one_network_app'] = {}
    tb_data["brownfield_msp1_with_three_tenants_and_app"] = {}
    tb_data['brownfield_msp2_with_one_tenant_and_app'] = {}
    tb_data['harness_brownfield_account_parent_pcid'] = {}
    tb_data["archive_devices_related_account"] = {}

    if "glcphf" in current_env:
        tb_data["url"] = current_env
        tb_data["gmail_username"] = "hcloud203@gmail.com"
        tb_data["gmail_password"] = "uwagtlwmcedlyayg"
        tb_data["sso_host"] = "qa-sso.ccs.arubathena.com"
        tb_data[
            "ccs_activate_v1_device_url"
        ] = "glcphf-activate-v1-device.ccs.arubathena.com"
        tb_data["gf_nw_api_client_id"] = "86992024-5c49-4374-9852-63f3a28a8726_api"
        tb_data["gf_nw_api_client_secret"] = secrets[tb_data["gf_nw_api_client_id"]]
        tb_data["gf_nw_app_id"] = "65858496-324d-492e-b117-6cfbb10b90a4"
        tb_data["gf_nw_app_region"] = "us-west"
        return tb_data