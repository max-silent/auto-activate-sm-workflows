import logging

import allure
import pytest

from automation_svc_ui.local_libs.activate_bridge.activate_bridge_utils import ActivateBridgeUtils
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils


@allure.parent_suite("activate-sm-workflows")
@allure.suite("activate bridge")
class TestActivateBridge:
    log = logging.getLogger(__name__)

    @pytest.mark.order(1)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220709)
    def test_post_bridge_login(self, post_bridge_login_user):
        """
        Test case verifies that the login response for a user is 'success' after posting bridge login credentials.
        """
        self.log.info(post_bridge_login_user)
        status_expected = 200
        assert post_bridge_login_user[0] == status_expected
        assert post_bridge_login_user[1]['response'] == 'success'

    @pytest.mark.order(2)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220710)
    def test_inventory_query_with_limit_offset(self, init_bridge_object):
        """
        Perform inventory query
        :param inventory_query: action param type, limit, offset
        :return: bool
        """
        action_param = 'query'
        limit = 2
        offset = 0
        create_test = ActivateBridgeUtils()
        inventory_query_status, inventory_query = create_test.inventory_query(action_param=action_param, limit=limit,
                                                                              offset=offset,
                                                                              init_bridge_object=init_bridge_object)
        self.log.info(inventory_query)
        status_expected = 200
        assert inventory_query_status == status_expected
        assert inventory_query['message']['code'] == 0
        assert inventory_query['info']['api'] == 'inventory'
        assert 'devices updated' in inventory_query['message']['text']

    @pytest.mark.order(3)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220711)
    def test_inventory_query_without_limit_offset(self, init_bridge_object):
        """
        Test to perform inventory query when values are None
        """
        create_test = ActivateBridgeUtils()
        inventory_query_status, inventory_query = create_test.inventory_query(init_bridge_object=init_bridge_object)
        self.log.debug(inventory_query)
        status_expected = 200
        assert inventory_query_status == status_expected
        assert inventory_query['message']['code'] == 0
        assert inventory_query['info']['api'] == 'inventory'
        assert 'devices updated' in inventory_query['message']['text']

    @pytest.mark.order(4)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1221625)
    def test_get_all_rules_by_folder(self, init_bridge_object):
        """
        Test case for retrieving all rules within a folder.
        """
        create_test = ActivateBridgeUtils()
        get_all_rules_status, get_all_rules = create_test.get_all_rules_by_folder(init_bridge_object=init_bridge_object)
        self.log.info(get_all_rules)
        status_expected = 200
        assert get_all_rules_status == status_expected
        assert get_all_rules['message']['code'] == '0'
        assert get_all_rules['info']['api'] == 'rules'
        assert 'rules returned' in get_all_rules['message']['text']

    @pytest.mark.order(5)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1221616)
    @pytest.mark.testrail(id=1221622)
    def test_create_and_delete_folder(self, init_bridge_object):
        """
        User provided folder name
        1. create_test.create_default_folder("my-folder-123"), a random folder name is generated
        2. Check if the folder exist
        3. Delete the created folder
        """
        user_folder_name = RandomGenUtils.random_string_of_chars(length=7, lowercase=False, uppercase=True, digits=True)
        create_test = ActivateBridgeUtils()
        create_folder_status, create_folder_response = create_test.create_folder(user_folder_name=user_folder_name,
                                                                                 init_bridge_object=init_bridge_object)
        self.log.info(create_folder_response)
        status_expected = 200
        assert create_folder_status == status_expected
        assert user_folder_name in create_folder_response['folder']['folderName']
        assert create_folder_response['folder']['folderName'] != ""
        assert create_folder_response['folder']['folderId'] != ""

        # Get Folder
        _, get_folder_by_query = create_test.get_all_folders_by_query(init_bridge_object=init_bridge_object)
        get_id, get_folder = None, None
        for folder in get_folder_by_query['folders']:
            if folder['id'] == create_folder_response['folder']['folderId']:
                get_id = folder['id']
                get_folder = folder['folderName']
                break
        if get_id:
            self.log.info(f"ID {get_id} exists. Corresponding folder: {get_folder}")
            self.log.info(f"Folder name exist {user_folder_name} in {create_folder_response}")

            # Delete folder
            id = [get_id]
            self.log.info("Cleaning up the folder")
            folder_status_code, folder_response = create_test.delete_created_folder(folderId=id,
                                                                                    init_bridge_object=init_bridge_object)
            assert folder_status_code == status_expected, "Folder deletion failed"
            assert "1folders deleted" in folder_response['message']['text']
            assert folder_response['folders'][0]['id'] == get_id
        else:
            self.log.info("Folder doesn't exist. Test case failed")
            assert False

    @pytest.mark.order(6)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1221617)
    def test_get_all_folders_by_query(self, init_bridge_object):
        """
        Test to get the all the folders by query with parameter = 'queryFid'
        """
        create_test = ActivateBridgeUtils()
        get_folder_by_query_status, get_folder_by_query = create_test.get_all_folders_by_query(
            init_bridge_object=init_bridge_object)
        self.log.info(get_folder_by_query)
        status_expected = 200
        assert get_folder_by_query_status == status_expected
        assert get_folder_by_query['info']['api'] == "folder"

    @pytest.mark.order(7)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1221634)
    def test_post_bridge_logout(self, init_bridge_object):
        """
        Test case verifies that a bridge logout can be successfully performed.
        """
        create_test = ActivateBridgeUtils()
        logout_status = create_test.bridge_logout(init_bridge_object=init_bridge_object)
        status_expected = 200
        self.log.info(logout_status)
        assert logout_status == status_expected

    @pytest.mark.order(8)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1416336)
    def test_access_to_resource_deny_after_user_logout(self, init_bridge_object):
        """
        In this test we are getting all folders by query after logout. As user is logout, it should not able to perform any action.
        """
        create_test = ActivateBridgeUtils()
        get_folder_by_query_status, get_folder_by_query = create_test.get_all_folders_by_query(
            init_bridge_object=init_bridge_object)
        self.log.info(f"{get_folder_by_query_status}, {get_folder_by_query}")
        assert get_folder_by_query is None
        assert not get_folder_by_query_status

    @pytest.mark.order(9)
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220707)
    def test_bridge_login_user2(self, post_bridge_login_user2):
        """
        Test case for validating the successful login response for user 2.

        This test case verifies that the login response for user 2 is 'success'
        after performing a bridge login using the specified credentials and
        the initialized ActivateBridgeHelper object.

        :param init_bridge_object (ActivateBridgeHelper): An instance of the ActivateBridgeHelper class.
        :param  post_bridge_login_user2 (dict): A dictionary containing the response data of the bridge login request for user 2.
        """
        self.log.info(post_bridge_login_user2)
        status_expected = 200
        assert post_bridge_login_user2[0] == status_expected
        assert post_bridge_login_user2[1]['response'] == 'success'
