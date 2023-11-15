#!/bin/bash -x

set -e

current_path=${PWD}
pushd /opt/ccs

file="poetry.lock"

if [ -f "$file" ] ; then
    rm "$file"
fi

running_cm=`cat /configmap/data/infra_clusterinfo.json`
echo "running with configmap: " $running_cm

# Generate spec will install all python libs as well ("not required for integration tests")
#./generate_spec.sh ${current_path} ("not required for integration tests")
popd

pip uninstall pytest-randomly -y

source /opt/ccs/automation/parser.sh

echo "================="
echo "cluster under test"
echo $ClusterUnderTest
if [ $AppNamespaceSuffix = "lite" ]; then
  export ClusterUnderTest="triton_lite"
  echo "changing ClusterUnderTest for triton_lite"
fi
echo $ClusterUnderTest
echo "================="

rm -rf /tmp/results || true

mkdir -p /tmp/results/testrail

export PYTHONPATHORIG="${PYTHONPATH}"
pushd /opt/ccs/automation
export PYTHONPATH="${PYTHONPATHORIG}:/opt/ccs/automation"

chmod 777 /input/data.txt
container_input=`cat /input/data.txt`
CurrentDate=$(date "+%Y%m%d")
TestRunTime=$(date +"%T")
export TestRunTime

if [ ${container_input} = "test_container_1" ]; then
  echo "running test cases from test_container_1 with arg: $container_input"
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/storage_compute/test_bf_str_com_existing_acct_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/storage_compute/test_bf_str_com_new_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/storage_compute/test_bf_idev_ldev_compute_provisioning.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_new_devices/test_bf_network_existing_msp_acct_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results  tests/workflows/brownfield/networking/existing_acct_new_devices/test_bf_network_existing_acct_new_devices.py -v -s -m ${TestType}  || true
fi

if [ ${container_input} = "test_container_2" ]; then
  echo "running test cases from test_container_2 with arg: $container_input"
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_new_devices/test_bf_network_existing_alias_acct_new_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/greenfield/test_gf_network_new_device_evals_subs_new_acct_manual_claim.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_archive_assigned_dev_from_list_of_dev.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results  tests/workflows/brownfield/networking/existing_acct_new_devices/test_archive_unassign_device.py -v -s -m ${TestType}  || true
fi

if [ ${container_input} = "test_container_3" ]; then
  echo "running test cases from test_container_3 with arg: $container_input"
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_bf_sm_existing_acct_existing_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/service_subs/test_create_claim_svc_subs.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_tac_acct_existing_devices/test_bf_network_existing_tac_acct_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_claim_vgw_device.py -v -s -m ${TestType}  || true
fi

if [ ${container_input} = "test_container_4" ]; then
  echo "running test cases from test_container_4 with arg: $container_input"
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_app_api_bf_existing_account_existing_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_unassign_device.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_move_device_from_parent_to_child_customer.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_move_device_to_folder.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_app_api_archive_existing_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_existing_acct_existing_dynamic_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_rma_flow.py -v -s -m ${TestType}  || true
fi

if [ ${container_input} = "test_container_5" ]; then
  echo "running test cases from test_container_5 with arg: $container_input"
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_new_devices/test_bf_network_tac_existing_acct_new_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_bf_network_existing_acct_existing_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/aop_flows/test_aop_flows.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_existing_devices/test_bf_vgw_nontpm_existing_acct_existing_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_new_devices/test_verify_claim_of_a_device.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results --milestone UndefTestType  tests/workflows/brownfield/networking/existing_acct_new_devices/test_bf_app_api_network_existing_acct_devices.py -v -s -m ${TestType}  || true
  poetry run pytest --alluredir /tmp/results  tests/workflows/brownfield/activate_bridge/test_abridge_harness_test_cases.py -v -s -m ${TestType}  || true
fi

pushd /opt/ccs/automation_svc_ui
export PYTHONPATH="${PYTHONPATHORIG}:/opt/ccs/automation_svc_ui"
if [ ${container_input} = "test_container_6" ]; then
  echo "running test cases from test_container_6 with arg: $container_input"
  poetry run pytest --alluredir /tmp/results  tests --ignore=tests/workflows --order-scope=class -v -s -m "${TestType} and not nonsvc and not wip"  || true
fi

# poetry run python /opt/ccs/results_parser.py --results_path /tmp/results --report_path /tmpdir/results/testrail
# poetry run python -m json.tool /tmpdir/results/testrail/test_rail_report.json

poetry run python /opt/ccs/automation/.venv/lib/python3.8/site-packages/hpe_glcp_automation_lib/libs/commons/utils/s3/s3-upload.py
