import logging
from os import path

from automation_svc_ui.conftest import ExistingUserAcctDevices

log_file_path = path.join(
    path.dirname(path.abspath(__file__)), "config/logging_config.ini"
)
log = logging.getLogger(__name__)

CLUSTER_INFO_FILE = "/configmap/data/infra_clusterinfo.json"


class InputPayload:
    def network_default_part_map(self):
        DEFAULT_PART_MAP = {"SWITCH": "JL255A", "IAP": "JW242AR", "GATEWAY": "7005-RW"}
        return DEFAULT_PART_MAP

    def app_prov_data(self):
        cluster = ExistingUserAcctDevices.login_page_url
        if "polaris" in cluster:
            polaris_app_prov_data = {
                "application_id": "17c23735-f960-4b85-9cc2-610a4fae617d",
                "region": "us-west",
            }
            return polaris_app_prov_data
        if "mira" in cluster:
            mira_app_prov_data = {
                "application_id": "65858496-324d-492e-b117-6cfbb10b90a4",
                "region": "eu-central",
            }
            return mira_app_prov_data
        if "triton" in cluster:
            triton_app_prov_data = {
                "application_id": "65858496-324d-492e-b117-6cfbb10b90a4",
                "region": "eu-central",
            }
            return triton_app_prov_data
