import logging
from automation.conftest import ExistingUserAcctDevices
from hpe_glcp_automation_lib.libs.abridge.helpers.abridge_device_helper import ActivateBridgeHelper

log = logging.getLogger(__name__)

class ActivateBridgeUtils:
    def __init__(self):
        """
        Init Code goes here
        """

    def create_bridge_login(self, username, password_token, init_bridge_object):
        """
        Creates a bridge login using the specified payload.

        :param username: The username for the bridge login.
        :param password_token: The password token for the bridge login.
        :param init_bridge_object: An instance of the ActivateBridgeHelper class.
        :return: response if the bridge login is successful, False otherwise.
        :rtype: dict or bool
        """
        log.info(f"Username received: {username}")
        login_status, login_response = init_bridge_object.post_bridge_login(username=username, password_token=password_token)
        return login_status, login_response

    def bridge_logout(self, init_bridge_object):
        """
        Logs out from the bridge.

        :param init_bridge_object: An instance of the ActivateBridgeHelper class.
        :return: True if the bridge logout is successful, False otherwise.
        :rtype: int or bool
        """
        logout_status, logout_status_code = init_bridge_object.post_bridge_logout()
        if logout_status:
            return logout_status_code
        else:
            return False

    def inventory_query(self, init_bridge_object, **action_param):
        """
        Executes an inventory query

        :param init_bridge_object: An instance of the ActivateBridgeHelper class.
        :param action_param: **kwargs
        :return: response if the inventory query is successful, False otherwise.
        :rtype: dict or bool
        """
        inventory_query_status, inventory_query_response = init_bridge_object.inventory_query(**action_param)
        return inventory_query_status, inventory_query_response

    def create_folder(self, init_bridge_object, user_folder_name=None):
        """
        Creates a default folder.

        :param init_bridge_object: An instance of the ActivateBridgeHelper class.
        :param user_folder_name: name provided by user (Optional: None)
        :return: response if the folder creation is successful, False otherwise.
        :rtype: dict or bool
        """
        create_default_folder_status, create_default_folder_response = init_bridge_object.create_folder(user_folder_name=user_folder_name)
        return create_default_folder_status, create_default_folder_response

    def get_all_folders_by_query(self, init_bridge_object):
        """
        Retrieves folders based on a query.

        :param init_bridge_object: An instance of the ActivateBridgeHelper class.
        :return: response if the folder retrieval is successful
        :rtype: dict or bool
        """
        get_all_folder_status, get_all_folder_response = init_bridge_object.get_all_folders_by_query()
        return get_all_folder_status, get_all_folder_response

    def get_all_rules_by_folder(self, init_bridge_object):
        """
        Retrieves all rules associated with a folder.

        :param init_bridge_object: An instance of the ActivateBridgeHelper class.
        :return: response if the rule retrieval is successful, False otherwise.
        :rtype: dict or bool
        """
        get_all_rules_status, get_all_rules = init_bridge_object.get_all_rules_by_folder()
        return get_all_rules_status, get_all_rules

    def delete_created_folder(self, init_bridge_object, folderId):
        """
        Deletes a folder or a list of folders.

        :param: folderId (list): The ID or a list of IDs of the folders to be deleted. Defaults to None.
        :param: init_bridge_object (object): The initialization bridge object. Defaults to None.
        :return: status code and response of the delete operation.
        """
        log.info(f"Fetching folder Id: {folderId}")
        folder_id_list = []
        if folderId is not None:
            folder_id_list = [{'folderId': folderId} for folderId in folderId]
        log.info("Folder list: %s", folder_id_list)
        folder_status_code, folder_response = init_bridge_object.delete_created_folder(folderId=folder_id_list)
        return folder_status_code, folder_response