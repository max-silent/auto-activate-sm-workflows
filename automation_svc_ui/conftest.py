import json
import logging
import os
import shutil
import subprocess
import sys

import pytest

from automation_svc_ui.configs.testrail_configs import testrail_configs
from automation_svc_ui.constants import AUTOMATION_DIRECTORY
from hpe_glcp_automation_lib.libs.adi.app_api.adi_app_api import ActivateInventory
from hpe_glcp_automation_lib.libs.commons.common_testbed_data.settings import (
    Settings,
    all_envs
)
from hpe_glcp_automation_lib.libs.commons.utils.s3.s3_download import download_file
from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail_plugin import (
    PyTestRailPlugin,
)

settings = Settings()

# set default_env to polaris if none is provided from pytest command line or clusterinfo
default_env = "polaris"
os.environ["CURRENT_ENV"] = default_env
os.environ["AUTOMATION_DIRECTORY"] = AUTOMATION_DIRECTORY


def pytest_configure(config):
    config.pluginmanager.register(PyTestRailPlugin(testrail_configs, username="", password=""))


# Placeholder for pytest not to raise exception because of new unknown argument.
# Argument processing need to be executed before all imports, so pytest build in will not help, it's too late.
def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", choices=all_envs.keys(), default=default_env
    )


# command line argument parser to find env under test
for index, arg in enumerate(sys.argv):
    if arg.startswith("--env"):
        if "=" in arg:
            if arg.split("=")[1] in all_envs.keys():
                os.environ["CURRENT_ENV"] = arg.split("=")[1]
                break
            else:
                raise Exception(f"Unsupported environment: {arg.split('=')[1]}")
        elif sys.argv[index + 1] in all_envs.keys():
            os.environ["CURRENT_ENV"] = sys.argv[index + 1]
            break
        else:
            raise ValueError(f"Unsupported environment: {sys.argv[index + 1]}")

# default env or command line env will override if settings.current_env() found env from clusterinfo
current_env = settings.current_env()

# import test data environment based on current env under test in local environment or on k8s environment
if os.getenv("POD_NAMESPACE") is None:
    exec(
        f"from automation_svc_ui.configs.local_tb_data.{current_env}_settings import {current_env}_test_data"
    )
else:
    exec(
        f"from automation_svc_ui.configs.pipeline_tb_data.{current_env}_settings import {current_env}_test_data"
    )

# global variables used for aop flows
aop_dict = {"manufacture": [], "license": [], "sds": [], "pos": []}
pytest.globalvar = {
    "runtime_testdata": {"STORAGE": aop_dict, "NETWORK": aop_dict, "COMPUTE": aop_dict}
}

log = logging.getLogger(__name__)


class Creds:
    @staticmethod
    def downloaded_test_envs():
        """
        downloading creds from remote s3 locations if available or use from local directory
        """
        s3_file_location = "akuc/auto-activate-sm-workflows/test_envs/"
        get_cwd = os.getcwd()
        try:
            download_file(s3_file_location)
            shutil.copy(
                f"{get_cwd}/{s3_file_location}*.*",
                AUTOMATION_DIRECTORY + "configs" + "pipeline_tb_data",
            )
            return True
        except Exception as ex:
            log.error(f"Not able to download the test_envs files. Error: {ex}")

    @staticmethod
    def downloaded_creds():
        """
        downloading creds from remote s3 locations if available or use from local directory
        """
        s3_file_location = "akuc/auto-activate-sm-workflows/creds/"
        get_cwd = os.getcwd()
        try:
            download_file(s3_file_location)
            shutil.copy(
                f"{get_cwd}/{s3_file_location}user_creds.json",
                AUTOMATION_DIRECTORY,
            )
            with open(os.path.join(AUTOMATION_DIRECTORY, "user_creds.json")) as fd:
                s3_login_data = json.load(fd)
                log.info("downloading creds from remote locations")
        except Exception as ex:
            with open(os.path.join(AUTOMATION_DIRECTORY, "user_creds.json")) as fd:
                s3_login_data = json.load(fd)
                log.info(f"Error on downloading creds. {ex}")
                log.info("using creds from local locations")
        return s3_login_data

    @staticmethod
    def resolve_creds(cluster):
        """
        downloading creds from remote s3 locations if available
        """
        log.info("getting creds from remote or local location")
        try:
            getcreds = Creds.downloaded_creds()
            client_ids_secrets = getcreds[cluster]["app_api_secrets"]
            users_passwords = getcreds[cluster]["users"]
            log.info(users_passwords)
            return client_ids_secrets, users_passwords
        except Exception as e:
            log.error(f"not able to download credentials, check logs:\n{e}")


class TestEnv:
    @staticmethod
    def download_all_envs_file():
        """
        download clusterinfo from s3 all_envs.json when running in k8s environment
        """
        test_env_file_location = "akuc/common/clusterinfo/"
        get_cwd = os.getcwd()
        try:
            download_file(test_env_file_location)
            shutil.copy(
                f"{get_cwd}/{test_env_file_location}all_envs.json",
                AUTOMATION_DIRECTORY,
            )
            with open(os.path.join(AUTOMATION_DIRECTORY, "all_envs.json")) as fd:
                test_envs = json.load(fd)
                log.info("downloading test environments from S3 location")
                return test_envs
        except Exception as ex:
            log.error(f"Error on downloading test environments from S3 location. {ex}")


def get_cluster_name_for_s3():
    cluster_name = os.environ.get("CURRENT_ENV")
    cluster_split_list = cluster_name.split("-")
    cluster = cluster_split_list[0] if len(cluster_split_list) > 1 else cluster_name
    log.info("Cluster name: {}".format(cluster))
    if len(cluster) < 3:
        raise ValueError(f"cluster_under_test is not valid: {cluster_name}")
    return cluster


def get_decryption_key(cluster):
    try:
        creds = Creds.downloaded_creds()
        decryption_password = creds[cluster]["add_pass"]
    except Exception as ex:
        with open(os.path.join(AUTOMATION_DIRECTORY, "user_creds.json")) as fd:
            decryption_password = json.load(fd)[cluster]["add_pass"]
            log.info(f"Error on downloading creds. {ex}")
            log.info("using creds from local locations")
    return decryption_password


@pytest.fixture(scope="module", autouse=True)
def decrypt_private_key():
    cluster = get_cluster_name_for_s3()
    password = get_decryption_key(cluster)

    pfx_file = os.path.join(AUTOMATION_DIRECTORY, "configs", "certs", "add_key.pfx")
    output_file = os.path.join(AUTOMATION_DIRECTORY, "configs", "certs", "add.key")

    # Decrypting the rsa_private_key
    try:
        cmd = ["openssl", "pkcs12", "-in", pfx_file, "-nocerts", "-nodes", "-passin", f"pass:{password}"]
        output = subprocess.check_output(cmd)
        with open(output_file, "wb") as f:
            f.write(output)
    except subprocess.CalledProcessError as e:
        log.error(f"Error decrypting file: {e}")
        raise

    # Check if the output file is decrypted properly
    with open(output_file) as f:
        file_contents = f.read()
    assert "PRIVATE KEY" in file_contents


class CreateLogFile:
    """
    Usage: Create log and result file location if not exists
    From this location Job will upload all logs and results
    """

    @staticmethod
    def log_file_location():
        return "/tmp/results/"

    @staticmethod
    def create_log_file():
        try:
            if not os.path.exists("/tmp/results/"):
                os.mkdir("/tmp/results/")
            if not os.path.exists("/tmp/results/log1.log"):
                with open("/tmp/results/log1.log", "w"):
                    pass
            return True
        except Exception as ex:
            log.info(f"not able to create log file and directory. Error: {ex}")


class CertFileLocation:
    """
    Usage: For activate device provisioning call certs are initialized from these locations
    Certs are needed to make the device provisioning calls in test cases.
    """

    certs_path = os.path.join(AUTOMATION_DIRECTORY, "configs", "certs")

    @classmethod
    def storage_certs_files(cls):
        storage_cert_data = {
            "cert": os.path.join(cls.certs_path, "storage-central-cert.pem"),
            "key": os.path.join(cls.certs_path, "storage-central-pkey.pem"),
            "ca_cert": os.path.join(cls.certs_path, "device.cloud.hpe.com.pem"),
        }
        return storage_cert_data

    @classmethod
    def compute_certs_files(cls):
        compute_cert_data = {
            "cert": os.path.join(cls.certs_path, "compute-central-cert.pem"),
            "key": os.path.join(cls.certs_path, "compute-central-pkey.pem"),
            "ca_cert": os.path.join(cls.certs_path, "device.cloud.hpe.com.pem"),
        }
        return compute_cert_data

    @classmethod
    def iap_cert_files(cls):
        iap_cert_data = {
            "cert": os.path.join(cls.certs_path, "iap-pem.pem"),
            "key": os.path.join(cls.certs_path, "iap-key.key"),
        }
        return iap_cert_data

    @classmethod
    def non_existent_comp_cert_files(cls):
        nonexistent_cert_data = {
            "cert": os.path.join(cls.certs_path, "STCOMNONEXTN_02_20_E0_81_D5_78_cert.pem"),
            "key": os.path.join(cls.certs_path, "add.key"),
            "ca_cert": os.path.join(cls.certs_path, "device.cloud.hpe.com.pem")
        }
        return nonexistent_cert_data

    @classmethod
    def success_comp_cert_files(cls):
        correct_cert_data = {
            "cert": os.path.join(cls.certs_path, "STCOMSER1_02_20_E0_81_D5_78_cert.pem"),
            "key": os.path.join(cls.certs_path, "add.key"),
            "ca_cert": os.path.join(cls.certs_path, "device.cloud.hpe.com.pem")
        }
        return correct_cert_data

    @classmethod
    def no_serial_cert_files(cls):
        no_serial_cert_data = {
            "cert": os.path.join(cls.certs_path, "STCOMSER1_NO_SERIAL_cert.pem"),
            "key": os.path.join(cls.certs_path, "add.key"),
            "ca_cert": os.path.join(cls.certs_path, "device.cloud.hpe.com.pem")
        }
        return no_serial_cert_data

    @classmethod
    def no_part_cert_files(cls):
        no_part_cert_data = {
            "cert": os.path.join(cls.certs_path, "STCOMSER1_NO_PART_cert.pem"),
            "key": os.path.join(cls.certs_path, "add.key"),
            "ca_cert": os.path.join(cls.certs_path, "device.cloud.hpe.com.pem")
        }
        return no_part_cert_data

    @classmethod
    def incorrect_part_cert_files(cls):
        incorrect_part_cert_data = {
            "cert": os.path.join(cls.certs_path, "STCOMSER1_INCORRECT_PART_cert.pem"),
            "key": os.path.join(cls.certs_path, "add.key"),
            "ca_cert": os.path.join(cls.certs_path, "device.cloud.hpe.com.pem")
        }
        return incorrect_part_cert_data

    @classmethod
    def incorrect_serial_cert_files(cls):
        incorrect_serial_cert_data = {
            "cert": os.path.join(cls.certs_path, "STCOMSERUNK1_INCORRECT_SERIAL_cert.pem"),
            "key": os.path.join(cls.certs_path, "add.key"),
            "ca_cert": os.path.join(cls.certs_path, "device.cloud.hpe.com.pem")
        }
        return incorrect_serial_cert_data


class NewUserAcctDevices:
    new_session = "None"
    new_acct_info = "None"
    new_iap_device_list = "None"
    new_sw_device_list = "None"
    new_gw_device_list = "None"
    new_storage_device_list = "None"
    new_compute_device_list = "None"
    app_prov_done = "None"
    verification_hash = "None"
    time_for_id = "None"
    email_with_timestamp = "None"
    cookies = ["None", "None", "None", "None"]


class ExistingUserAcctDevices:
    """
    ExistingUserAcctDevices test env variables available for usage in test cases,
    inner tests' conftest.py, and in test helper methods, local_libs
    """

    current_env = settings.current_env()
    login_page_url = settings.login_page_url()
    app_api_hostname = settings.get_app_api_hostname()
    sso_hostname = settings.get_sso_host()
    hpe_device_url = settings.get_hpe_device_url()
    aruba_device_url = settings.get_aruba_device_url()
    aruba_switch_device_url = settings.get_aruba_switch_device_url()
    ccs_device_url = settings.get_ccs_device_url()
    ccs_activate_v1_device_url = settings.get_ccs_activate_v1_device_url()
    ccs_activate_v2_device_url = settings.get_ccs_activate_v2_device_url()
    auth_url = settings.get_auth_url()

    if current_env == "mira" or current_env == "pavo":
        current_env_r = settings.current_env(readonly=True)
        login_page_url_r = settings.login_page_url(readonly=True)
        user_api_url_r = settings.get_user_api_hostname(readonly=True)
        app_api_hostname_r = settings.get_app_api_hostname(readonly=True)
        sso_hostname_r = settings.get_sso_host(readonly=True)
        hpe_device_url_r = settings.get_hpe_device_url(readonly=True)
        aruba_device_url_r = settings.get_aruba_device_url(readonly=True)
        aruba_switch_device_url_r = settings.get_aruba_switch_device_url(readonly=True)
        ccs_device_url_r = settings.get_ccs_device_url(readonly=True)
        ccs_activate_v1_device_url_r = settings.get_ccs_activate_v1_device_url(readonly=True)
        ccs_activate_v2_device_url_r = settings.get_ccs_activate_v2_device_url(readonly=True)
        auth_url_r = settings.get_auth_url(readonly=True)

    s3_login_data = Creds.downloaded_creds()
    login_data = s3_login_data[current_env]
    # aruba_legacy_device_url = settings.get_aruba_legacy_device_url()
    create_log_file = CreateLogFile.create_log_file()
    log_files = CreateLogFile.log_file_location()
    storage_certs = CertFileLocation.storage_certs_files()
    compute_certs = CertFileLocation.compute_certs_files()
    idev_ldev_non_existent_comp_certs = CertFileLocation.non_existent_comp_cert_files()
    idev_ldev_success_certs = CertFileLocation.success_comp_cert_files()
    idev_ldev_without_serial_certs = CertFileLocation.no_serial_cert_files()
    idev_ldev_without_part_certs = CertFileLocation.no_part_cert_files()
    idev_ldev_incorrect_part_certs = CertFileLocation.incorrect_part_cert_files()
    idev_ldev_incorrect_serial_certs = CertFileLocation.incorrect_serial_cert_files()
    iap_certs = CertFileLocation.iap_cert_files()
    secrets, passwords = Creds.resolve_creds(current_env)
    test_data = dict()
    exec("test_data = {}_test_data(current_env, secrets, passwords)".format(current_env))
    humio_url = settings.get_humio_url()


def browser_type(playwright, browser_name: str):
    """
    instantiate browser types based on local or k8s env with headless true or false
    """
    if browser_name == "chromium":
        browser = playwright.chromium
        if os.getenv("DEBIAN_FRONTEND") == "noninteractive":
            return browser.launch(headless=True, slow_mo=100)
        elif os.getenv("POD_NAMESPACE") is None:
            return browser.launch(headless=False, slow_mo=100)
        else:
            return browser.launch(headless=True, slow_mo=100)
    if browser_name == "firefox":
        browser = playwright.firefox
        if os.getenv("DEBIAN_FRONTEND") == "noninteractive":
            return browser.launch(headless=True, slow_mo=100)
        elif os.getenv("POD_NAMESPACE") is None:
            return browser.launch(headless=False, slow_mo=100)
        else:
            return browser.launch(headless=True, slow_mo=100)
    if browser_name == "webkit":
        browser = playwright.webkit
        if os.getenv("DEBIAN_FRONTEND") == "noninteractive":
            return browser.launch(headless=True, slow_mo=100)
        elif os.getenv("POD_NAMESPACE") is None:
            return browser.launch(headless=False, slow_mo=100)
        else:
            return browser.launch(headless=True, slow_mo=100)


@pytest.fixture(scope="session")
def browser_instance(playwright):
    """
    instantiate browser instance for test cases
    """
    browser = browser_type(playwright, "chromium")
    yield browser
    browser.close()


def get_add_device_expected_responses():
    data_file = os.path.join(
        AUTOMATION_DIRECTORY,
        "configs",
        "activate_device_direct_test_data",
        "add_test_data.json",
    )
    with open(data_file) as data_output:
        test_data_json = json.load(data_output)
    return test_data_json


class SkipTest:
    @staticmethod
    def skip_if_triton():
        if "triton" in ExistingUserAcctDevices.login_page_url:
            log.info("skipping env {}".format(ExistingUserAcctDevices.login_page_url))
            pytest.skip("triton env is SKIPPED")

    @staticmethod
    def skip_if_polaris():
        if "polaris" in ExistingUserAcctDevices.login_page_url:
            log.info("skipping env {}".format(ExistingUserAcctDevices.login_page_url))
            pytest.skip("polaris env is SKIPPED")

    @staticmethod
    def skip_if_mira():
        if "mira" in ExistingUserAcctDevices.login_page_url:
            log.info("skipping env {}".format(ExistingUserAcctDevices.login_page_url))
            pytest.skip("mira env is SKIPPED")

    @staticmethod
    def skip_if_triton_lite():
        if "triton-lite" in ExistingUserAcctDevices.login_page_url:
            log.info("skipping env {}".format(ExistingUserAcctDevices.login_page_url))
            pytest.skip("triton-lite env is SKIPPED")

    @staticmethod
    def skip_if_pavo():
        if "pavo" in ExistingUserAcctDevices.login_page_url:
            log.info("skipping env {}".format(ExistingUserAcctDevices.login_page_url))
            pytest.skip("pavo env is SKIPPED")


@pytest.fixture(scope="class")
def adi_app_api_session(app_api_key=None, app_api_secret=None):
    api_key = (
        ExistingUserAcctDevices.test_data[
            "brnf_existing_acct_existing_devices_client_id"
        ],
    )
    api_secret = (
        ExistingUserAcctDevices.test_data[
            "brnf_existing_acct_existing_devices_client_secret"
        ],
    )
    if app_api_key and app_api_secret:
        api_key = app_api_key
        api_secret = app_api_secret
    adi_app_api = ActivateInventory(
        host=ExistingUserAcctDevices.app_api_hostname,
        sso_host=ExistingUserAcctDevices.sso_hostname,
        client_id=api_key,
        client_secret=api_secret,
    )
    return adi_app_api


class SubscriptionData:
    def __init__(self, device_type):
        subscription_data = {
            "IAP": {"subs_type": "CENTRAL_AP", "part_number": "JW242AR"},
            "SWITCH": {"subs_type": "CENTRAL_SWITCH", "part_number": "JL255A"},
            "GATEWAY": {"subs_type": "CENTRAL_GW", "part_number": "7005-RW"},
        }
        if device_type in subscription_data.keys():
            self.subscription_type = subscription_data[device_type]["subs_type"]
            self.part_number = subscription_data[device_type]["part_number"]
        else:
            raise ValueError(f"Unexpected device type: '{device_type}'")
