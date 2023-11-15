from datetime import datetime

from hpe_glcp_automation_lib.libs.commons.common_testbed_data.settings import Settings

settings = Settings()
now = datetime.utcnow()
date_tag = now.strftime("%B-%d-%Y")
time_tag = now.strftime("%B-%d-%Y-%H:%M:%S")

test_suite = "SystemTests"
cluster = settings.current_env()
test_type = settings.get_testType() or "Regression"
collection_type = settings.get_collectionType() or "Morning-Coffee"

testrail_configs = {
    "project": "",
    "milestone": "",
    "child_milestone": collection_type,
    "test_suite": test_suite,
    "test_plan": f"Activate-SM-plan-{cluster}-{collection_type}-{date_tag}",
    "test_run": f"Activate-SM-run-{cluster}-{collection_type}-{time_tag}-UTC",
    "tc_ids": [],
    "config_ids": [],
}
