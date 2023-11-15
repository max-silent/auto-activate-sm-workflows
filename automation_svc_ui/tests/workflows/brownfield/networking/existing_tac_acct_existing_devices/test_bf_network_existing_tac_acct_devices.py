import logging

import allure
import pytest

from automation_svc_ui.conftest import ExistingUserAcctDevices
from automation_svc_ui.tests.workflows.brownfield.networking.existing_tac_acct_existing_devices \
    .brnf_network_existing_tac_acct_devices import WfExistingTacExistingDevices

log = logging.getLogger(__name__)


@pytest.mark.skipif("polaris" in ExistingUserAcctDevices.login_page_url, reason="Not supported on polaris.")
@pytest.mark.skipif("triton-lite" in ExistingUserAcctDevices.login_page_url, reason="Not supported on triton-lite.")
@pytest.mark.skipif("pavo" in ExistingUserAcctDevices.login_page_url, reason="Not supported on pavo.")
@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield TAC network devices service_centric_ui")
@allure.sub_suite("Brownfield TAC existing account existing network devices")
class TestExistingTACAccountExistingDevicesSvc:
    @pytest.mark.testrail(id=1220697)
    @pytest.mark.order(1)
    @pytest.mark.Regression
    def test_activate_folders_page_create_c1220697(self, browser_instance,
                                                   logged_in_storage_state,
                                                   device_folder_name):
        create_test = WfExistingTacExistingDevices()
        assert create_test.wf_tac_folders_page(browser_instance, logged_in_storage_state, device_folder_name)

    @pytest.mark.testrail(id=1220700)
    @pytest.mark.order(2)
    @pytest.mark.Regression
    def test_tac_add_rule_to_folder_c1220700(self,
                                             browser_instance,
                                             logged_in_storage_state,
                                             device_folder_name):
        """
        Test goes to TAC account 'Folder Details' page, creates a rule for that folder and verified creation was
        successful.
        Steps:
        1. Login to GLCP with TAC user credentials
        2. Open CCS manager menu
        3. Open particular account tab
        4. Open account's folders tab
        5. Open particular folder details page
        6. Add new rule to the folder
        7. Verify rule is in the list of folder's rules
        """
        create_test = WfExistingTacExistingDevices()
        assert create_test.wf_tac_create_rule_for_folder(browser_instance, logged_in_storage_state, device_folder_name)

    @pytest.mark.testrail(id=1220696)
    @pytest.mark.Regression
    @pytest.mark.order(3)
    def test_tac_move_devices_to_folder_c1220696(self,
                                                 browser_instance,
                                                 logged_in_storage_state,
                                                 device_folder_name,
                                                 movable_device_sn_iap,
                                                 movable_device_sn_gw,
                                                 movable_device_sn_sw):
        """
        Navigate to TAC account 'Customer Details' page of 'Devices' tab and move existing devices to other
        existing folder.

        Steps:
        1. Login to GLCP with TAC user credentials.
        2. Open CCS manager menu.
        3. Open particular account tab.
        4. Open account's devices tab.
        5. Select in table existing devices with specified serial numbers.
        6. Move selected devices to other folder with specified name.
        7. Verify device is in the list of folders' devices.
        """
        create_test = WfExistingTacExistingDevices()
        devices_serials = movable_device_sn_iap, movable_device_sn_gw, movable_device_sn_sw
        assert create_test.wf_verify_devices_on_device_tab(browser_instance, logged_in_storage_state,
                                                           device_folder_name,
                                                           devices_serials)

    # TODO: Create corresponding TC in testrail or remove.
    # @pytest.mark.testrail(id=1221615)
    # @pytest.mark.order(4)
    # @pytest.mark.Regression
    # def test_tac_move_devices_between_customers_default_to_custom_folder_C1221615(browser_instance,
    #                                                                               logged_in_storage_state,
    #                                                                               inter_customers_movable_devices,
    #                                                                               device_folder_name):
    #     """
    #     Test goes to TAC account 'Devices' page, moves 50 existing devices to other customer's custom folder and
    #     verifies that moving was successful.
    #     Steps:
    #     1. Login to GLCP with TAC user credentials
    #     2. Open CCS manager menu
    #     3. Open Devices page
    #     4. Move 50 existing devices from default folder of customer1 to custom folder of customer2
    #     5. Verify devices are present in specified folder of corresponding customer
    #     """
    #     create_test = WfExistingTacExistingDevices()
    #     assert create_test.wf_tac_move_devices_between_customers(browser_instance,
    #                                                              logged_in_storage_state,
    #                                                              inter_customers_movable_devices,
    #                                                              device_folder_name)

    @pytest.mark.testrail(id=1221615)
    @pytest.mark.order(4)
    @pytest.mark.Regression
    @pytest.mark.xfail(reason="Mira search by Customer ID issue: GLCP-45928")
    def test_tac_move_devices_to_aruba_factory_stock_default_folder_c1221615(self,
                                                                             browser_instance,
                                                                             logged_in_storage_state,
                                                                             inter_customers_movable_devices):
        """
        Test goes to TAC account 'Devices' page, moves 50 existing devices of customer1 to default folder
        of Aruba-Factory-Stock customer and verifies that moving was successful.
        Steps:
        1. Login to GLCP with TAC user credentials
        2. Open CCS manager menu
        3. Open Devices page
        4. Move 50 existing devices from default folder of customer1 to default folder of Aruba-Factory-Stock customer
        5. Verify devices are moved and not present at customer1
        """
        create_test = WfExistingTacExistingDevices()
        assert create_test.wf_tac_move_devices_to_aruba_f_stock(browser_instance,
                                                                logged_in_storage_state,
                                                                inter_customers_movable_devices,
                                                                initial_folder_name="default",
                                                                target_stock_folder_name="default"
                                                                )

    @pytest.mark.testrail(id=1221613)
    @pytest.mark.order(5)
    @pytest.mark.Regression
    def test_tac_move_devices_between_customers_default_to_default_folder_c1221613(self,
                                                                                   browser_instance,
                                                                                   logged_in_storage_state,
                                                                                   inter_customers_movable_devices):
        """
        Test goes to TAC account 'Devices' page, moves 50 existing devices to other customer's default folder
        and verifies that moving was successful.
        Steps:
        1. Login to GLCP with TAC user credentials
        2. Open CCS manager menu
        3. Open Devices page
        4. Move 50 existing devices from default folder of customer1 to default folder of customer2
        5. Verify devices are present in specified folder of corresponding customer
        """
        create_test = WfExistingTacExistingDevices()
        assert create_test.wf_tac_move_devices_between_customers(browser_instance,
                                                                 logged_in_storage_state,
                                                                 inter_customers_movable_devices,
                                                                 "default")

    @pytest.mark.testrail(id=1221614)
    @pytest.mark.order(6)
    @pytest.mark.Regression
    def test_tac_move_devices_between_customers_athena_f_to_athena_f_folder_c1221614(self,
                                                                                     browser_instance,
                                                                                     logged_in_storage_state,
                                                                                     athena_f_devices):
        """
        Test goes to TAC account 'Devices' page, tries to move 3 existing devices at athena-f folder
        to other customer's athena-f folder and verifies error alert appeared.
        Steps:
        1. Login to GLCP with TAC user credentials
        2. Open CCS manager menu
        3. Open Devices page
        4. Try to move 3 existing devices from athena-f folder of customer1 to athena-f folder of customer2
        5. Verify error appeared and devices are not moved.
        """
        create_test = WfExistingTacExistingDevices()
        cust1_athena_f_folder = ExistingUserAcctDevices.test_data[
            "brnf_existing_acct_new_devices_pcid1_athena_f_folder"]
        cust2_athena_f_folder = \
            ExistingUserAcctDevices.test_data["tac_existing_acct_existing_devices_pcid1_athena_f_folder"]
        assert create_test.wf_tac_move_devices_between_customers_to_athena_f(browser_instance,
                                                                             logged_in_storage_state,
                                                                             athena_f_devices,
                                                                             cust1_athena_f_folder,
                                                                             cust2_athena_f_folder)

    @pytest.mark.testrail(id=1220699)
    @pytest.mark.Regression
    @pytest.mark.order(7)
    def test_tac_edit_folder_c1220699(self,
                                      browser_instance,
                                      logged_in_storage_state,
                                      device_folder_name):
        """
        Test goes to TAC account 'Folder Details' page, edits that folder and verifies that edit was
        successful.
        Steps:
        1. Login to GLCP with TAC user credentials
        2. Open CCS manager menu
        3. Open particular account tab
        4. Open account's folders tab
        5. Open particular folder details page
        6. Edit current folder
        7. Verify folder has new attributes in the list of customers' folders
        """
        create_test = WfExistingTacExistingDevices()
        assert create_test.wf_tac_edit_folder(browser_instance, logged_in_storage_state, device_folder_name)

    @pytest.mark.testrail(id=1220701)
    @pytest.mark.Regression
    @pytest.mark.order(8)
    def test_tac_get_devices_in_folder_c1220701(self,
                                                browser_instance,
                                                logged_in_storage_state,
                                                device_folder_name,
                                                movable_device_sn_iap,
                                                movable_device_sn_gw,
                                                movable_device_sn_sw):
        """
        Test goes to TAC account 'Folder Details' page, and verified devices are shown on it.
        Steps:
        1. Login to GLCP with TAC user credentials
        2. Open CCS manager menu
        3. Open particular account tab
        4. Open account's folders tab
        5. Open particular folder details page
        6. Verify that particular device is in the folder
        """
        create_test = WfExistingTacExistingDevices()
        devices_serials = movable_device_sn_iap, movable_device_sn_gw, movable_device_sn_sw
        assert create_test.wf_verify_devices_on_folder_details(browser_instance, logged_in_storage_state,
                                                               device_folder_name, devices_serials)

    @pytest.mark.testrail(id=1220698)
    @pytest.mark.Regression
    @pytest.mark.order(9)
    def test_tac_delete_folder_c1220698(self,
                                        browser_instance,
                                        logged_in_storage_state,
                                        device_folder_name):
        """
        Test goes to TAC account 'Folder Details' page, deletes that folder and verifies deletion was
        successful.
        Steps:
        1. Login to GLCP with TAC user credentials
        2. Open CCS manager menu
        3. Open particular account tab
        4. Open account's folders tab
        5. Open particular folder details page
        6. Delete current folder
        7. Verify folder is not in the list of customers' folders
        """
        create_test = WfExistingTacExistingDevices()
        assert create_test.wf_tac_delete_folder(browser_instance, logged_in_storage_state, device_folder_name)

    @pytest.mark.testrail(id=1220695)
    @pytest.mark.Regression
    @pytest.mark.order(10)
    def test_tac_create_eval_subscription_c1220695(self,
                                                   eval_subscription):
        """
        Test generates eval subscription and verified it was successful.
        """
        assert eval_subscription, "Eval subscription creation was not completed successfully."
        assert eval_subscription.get("evaluation_type") == "EVAL" and eval_subscription.get(
            "subscription_tier") == "FOUNDATION_AP", \
            f"Failed: Eval subscription has wrong data. Actual response: {eval_subscription}"

    @pytest.mark.testrail(id=1220693)
    @pytest.mark.Regression
    @pytest.mark.order(11)
    def test_tac_modify_devices_quantity_subscription_c1220693(self,
                                                               eval_subscription,
                                                               brnf_sa_user_login_load_account):
        """
        Test updates eval subscriptions' devices quantity and verified it was successful.
        """
        quantity_increment = 10
        new_value = {"quantity": quantity_increment}
        create_test = WfExistingTacExistingDevices()
        updated_subscription = create_test.wf_modify_eval_subscription(brnf_sa_user_login_load_account,
                                                                       eval_subscription,
                                                                       new_value)
        assert updated_subscription, "Eval subscription was not updated successfully."
        assert updated_subscription.get("quantity") == (eval_subscription.get("quantity") + quantity_increment), \
            f"Failed: Subscription has wrong data.\n" \
            f"Actual devices quantity: {updated_subscription.get('quantity')}\n" \
            f"Expected devices quantity: {eval_subscription.get('quantity') + quantity_increment}"

    @pytest.mark.testrail(id=1220694)
    @pytest.mark.Regression
    @pytest.mark.order(12)
    def test_tac_modify_end_date_subscription_c1220694(self,
                                                       eval_subscription,
                                                       brnf_sa_user_login_load_account):
        """
        Test updates eval subscriptions' end date and verified it was successful.
        """
        end_date_increment = 31536000
        new_value = {"subscription_end": end_date_increment}
        create_test = WfExistingTacExistingDevices()
        updated_subscription = create_test.wf_modify_eval_subscription(brnf_sa_user_login_load_account,
                                                                       eval_subscription,
                                                                       new_value)
        assert updated_subscription, "Eval subscription was not updated successfully."
        assert updated_subscription.get("appointments").get("subscription_end") == (
                eval_subscription.get("appointments").get("subscription_end") + end_date_increment * 1000
        ), f"Failed: Subscription has wrong data.\n" \
           f"Actual end date (epoch): {updated_subscription.get('appointments').get('subscription_end')}\n" \
           f"Expected end date (epoch): " \
           f"{eval_subscription.get('appointments').get('subscription_end') + end_date_increment * 1000}"

    @pytest.mark.Regression
    @pytest.mark.order(13)
    @pytest.mark.parametrize("fixture_name", [
        pytest.param("eval_subscription", marks=[pytest.mark.testrail(id=1220692), pytest.mark.testrail(id=1340449)]),
        pytest.param("sw_brim_subscription", marks=pytest.mark.testrail(id=1221582)),
        pytest.param("service_brim_subscription", marks=pytest.mark.testrail(id=1340448))])
    def test_tac_transfer_subscription_c1220692(self,
                                                browser_instance,
                                                logged_in_storage_state,
                                                request,
                                                fixture_name,
                                                ):
        """
        Test transfer subscription and verified it was successful.
        """
        subscription_data = request.getfixturevalue(fixture_name)
        create_test = WfExistingTacExistingDevices()
        assert create_test.wf_transfer_subscription(
            browser_instance, logged_in_storage_state, subscription_data
        ), "Failed: Subscription was not transferred successfully, or has wrong data."

    @pytest.mark.Regression
    @pytest.mark.order(14)
    @pytest.mark.parametrize("subscription_key", [
        pytest.param("tac_existing_acct_existing_devices_pcid1_iap_eval_subs_key_assigned",
                     marks=pytest.mark.testrail(id=1340447)),
        pytest.param("tac_existing_acct_existing_devices_pcid1_gw_brim_subs_key_assigned",
                     marks=pytest.mark.testrail(id=1340446)),
    ])
    def test_tac_transfer_assigned_subscription_c1340447(self,
                                                         browser_instance,
                                                         logged_in_storage_state,
                                                         brnf_sa_user_login_load_account,
                                                         subscription_key):
        """
        Test transfer assigned subscription and verified its forbidden.
        """
        create_test = WfExistingTacExistingDevices()
        assigned_subs_key = ExistingUserAcctDevices.test_data[subscription_key]
        assigned_subscription_data = brnf_sa_user_login_load_account.get_cm_customer_subscriptions(
            subscription_key_pattern=assigned_subs_key
        )
        assert assigned_subscription_data, "There are no subscriptions in response."
        assert create_test.wf_verify_error_transferring_subscription(browser_instance,
                                                                     logged_in_storage_state,
                                                                     assigned_subscription_data[0]), \
            "Failed: Subscription was transferred successfully.\n" \
            "Expected result: error transferring subscription with device assignment."

    @pytest.mark.testrail(id=1220702)
    @pytest.mark.Regression
    @pytest.mark.order(15)
    def test_tac_add_alias_c1220702(self,
                                    browser_instance,
                                    logged_in_storage_state,
                                    customer_alias_name):
        """
        Test goes to TAC account 'Aliases' page, adds new alias and verifies addition was
        successful.
        Steps:
        1. Login to GLCP with TAC user credentials
        2. Open CCS manager menu
        3. Open particular account tab
        4. Open account's aliases tab
        5. Add new alias to the customer
        6. Verify alias is in the list of customers' aliases
        """
        create_test = WfExistingTacExistingDevices()
        assert create_test.wf_verify_add_alias(browser_instance, logged_in_storage_state, customer_alias_name)

    @pytest.mark.testrail(id=1220702)
    @pytest.mark.Regression
    @pytest.mark.order(16)
    def test_tac_delete_alias_c1220702(self,
                                       browser_instance,
                                       logged_in_storage_state,
                                       customer_alias_name):
        """
        Test goes to TAC account 'Aliases' page, deletes alias and verifies deletion was
        successful.
        Steps:
        1. Login to GLCP with TAC user credentials
        2. Open CCS manager menu
        3. Open particular account tab
        4. Open account's aliases tab
        5. Delete alias from the customer
        6. Verify alias is not in the list of customers' aliases
        """
        create_test = WfExistingTacExistingDevices()
        assert create_test.wf_verify_delete_alias(browser_instance, logged_in_storage_state, customer_alias_name)
