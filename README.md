### auto-activate-sm-workflows
Purpose of this repo is to automate workflow based test cases for Activate and Subscriptions Management features: 
- Test repo uses similar structure in other test repo such as auto-activate-sm-workflows, auto-login-workflows, glcp-solution-testing

pyproject.toml and poetry.lock files are used to create python environment with required modules and libraries
- pyproject.toml: List of modules required to be installed when test scripts are executed
- poetry.lock: Lock file is created at the beginning when pyproject.toml is created, when poetry install is run then each environment is created based on poetry.lock file which has the module version
- Uses glcp-common-automation-libs for common libraries from glcp feature test https://github.com/glcp/glcp-common-automation-libs

- Test cases are developed locally, developed from Engineer's laptop environment and once working for different test beds, test cases is merged into mainline and start running periodically inside k8s container environment
- By default test cases for UI run in headless mode on k8s environment and headed mode in local environment

#### Directories description in Test Repo:
1. automation/configs: 
- Credentials such as password, app-api credentials are not check in to git hub,
- There are 2 directories in this folder: local_tb_data, pipeline_tb_data
- local_tb_data: Separate file for each test bed, has usernames, app_api_id, applications, accounts, devices
- test data from this file is used when Engineer wants to run the test cases from local environment

- pipeline_tb_data: Separate file for each test bed, has usernames, app_api_id, applications, accounts, devices test data from this file is used when test run detect its envoked within k8s environment
- All passwords and api credentials by each repo for all the test beds as a json file is in S3 bucket location under repo_folder name

- For k8s runs:
  - creds will be downloaded during test execution to a location, read the file in conftest.py and initialize as login_data. Test case parse the username/app_api_id from test_data and matching password/secret from login_data for the test to use in its steps. 
- For local runs:
  - jenkins job to pull down the credentials from S3 using job at https://acp-jenkins.arubathena.com/job/ccs/job/Development/job/s3_akuc_download/ with S3 path `akuc/auto-activate-sm-workflows/creds`
  - Place the file in automation directory as user_creds.json and not push this file to github.
  
2. automation/conftest.py: 
- Initialize test data, CreateLogFile, CertFileLocation, set environment variable for local runs (by default: polaris), playwright browser_instance for tests to initialize(chromium)

3. automation/libs_local:
- If tester needs to build local library to be used by test scripts those files can be placed in this directory

4. automation/test folders
- automation/tests/<test_name_folder>:
- test_case_name.py - Test case names
- conftest.py - Fixtures used by test cases in test_case_name.py
- workflow_step_file.py - Test steps to be used by test_case_name.py and conftest.py and it uses common glcp automation libs 

5. auto-activate-sm-workflows/automation/tests/workflows/brownfield/networking:
- test_bf_network_existing_acct_new_devices.py - Test case name description, pytest invoke test case from this folder
- conftest.py - Fixtures used by test cases in test_bf_network_existing_acct_new_devices.py
- brnf_network_existing_acct_new_devices.py - Test logic file and make up test data for the test case steps to use
  common glcp automation libs.

#### using common-libs in test cases examples: for playwright pom, user-api session, app-api session 
- Poetry install has installed the glcp-common-automation-libs on test repo under .venv/lib/python3.8/site-packages/hpe_glcp_automation_lib (It may be different for different OS)
- Example using playwright page object model to login and go to audit logs page:
- https://github.com/glcp/auto-activate-sm-workflows/blob/mainline/automation/tests/workflows/greenfield/wf_session_new_user_acct_first_order_auto_claim.py#L501
- https://github.com/glcp/auto-activate-sm-workflows/blob/mainline/automation/tests/workflows/greenfield/wf_session_new_user_acct_first_order_auto_claim.py#L167
- In common libs hpe_glcp_automation_lib/libs/commons/utils/pwright/pwright_utils.py there are commonly used utilities can be used during playwright UI tests
- In common libs utils there are functions `browser_page` will initiate with context tracing throughout the test run and `browser_stop` will stop the trace if test case finishes or fails due to errors
- trace logs can be viewed after downloading the trace file from the test run with running command as "playwright show-trace <path to downloaded file>"

- Example using User_api to login and provision the application instance:
- https://github.com/glcp/auto-activate-sm-workflows/blob/mainline/automation/tests/workflows/greenfield/conftest.py#L78
- https://github.com/glcp/auto-activate-sm-workflows/blob/mainline/automation/tests/workflows/greenfield/wf_session_new_user_acct_first_order_auto_claim.py#L222

- Example using App_api to create session make the app_api call:
- https://github.com/glcp/auto-activate-sm-workflows/blob/mainline/automation/tests/workflows/greenfield/wf_session_new_user_acct_first_order_auto_claim.py#L394

#### Making any changes to libraries: 
- You can refer to below link for making any changes to common libs and test locally and raise PR in common libs repo 
- https://hpe.atlassian.net/wiki/spaces/GST/pages/1949761650/CAFE+-+Common+Automation+Framework+and+Environments#Making-any-changes-to-libraries-locally:

#### How to run the test cases:
- In k8s environment test cases will be executed by docker entrypoint for automation/run-st.sh which has command like
- poetry run pytest --alluredir /tmp/results --junitxml=/tmpdir/results/testrail/"STStorageComputeTestResults_Regression.xml" automation/tests/ -v -s -m ${TestType}  || true

- In local laptop environment:
- Pre-requisite: 
- Setup test environment - Follow instructions at https://hpe.atlassian.net/wiki/spaces/GST/pages/1974763867/CAFE+Setup#Set-Up-Local-Test-Environment

- To run test cases under automation/tests/examples/greenfield/CreateNewUserNewAcctNewDevices:
- Download user creds file from jenkins job https://acp-jenkins.arubathena.com/job/ccs/job/Development/job/s3_akuc_download/ with S3 path: akuc/auto-cafe-template/creds
- Replace the content of file at auto-cafe-template/automation/configs/local_tb_data/user_creds.json
- If you are using your own gmail address, replace gmail username in file auto-cafe-template/automation/configs/local_tb_data/<testbed_name.py>
- Replace 16 digit gmail password with your working gmail. auto-cafe-template/automation/configs/local_tb_data/user_creds.json
- For gmail allow gmail account login from less secure apps, you can follow steps at: https://support.google.com/accounts/answer/6010255?hl=en#zippy=%2Cuse-an-app-password
- Gmail method at hpe_glcp_automation_lib.libs.commons.utils.gmail.gmail_imap2.GmailOps_okta parses the received emails from GLCP for user signup and account activation
  - After gmail is setup from prompt type: 
  - python3 -m pytest --alluredir=/tmp/results automation/tests/examples/greenfield/CreateNewUserNewAcctNewDevices/test_gf_network_new_device_evals_subs_new_acct_manual_claim.py --env=polaris -m Regression
  - This will run on polaris cluster, to run on other clusters you will want to populate the data in configs file for the respective test bed
  - To view results type: allure serve /tmp/results/ allure -h localhost
  
- To run test cases under auto-cafe-template/automation/tests/examples/greenfield/CreateNewUserNewAcctNewDevices/:
- Download user creds file from jenkins job https://acp-jenkins.arubathena.com/job/ccs/job/Development/job/s3_akuc_download/ with S3 path akuc/auto-activate-sm-workflows/creds
- replace the content of file at auto-cafe-template/automation/configs/local_tb_data/user_creds.json
  - From prompt type:
  - python3 -m pytest --alluredir=/tmp/results
    automation/tests/examples/brownfield/ExistingAcctNewDevices/test_bf_network_existing_acct_new_devices.py
    --env=polaris -m Regression
  - This will run on polaris cluster, to run on other clusters you will want to populate the data in configs file for
    the respective test bed
  - To view results type: allure serve /tmp/results/ allure -h localhost
