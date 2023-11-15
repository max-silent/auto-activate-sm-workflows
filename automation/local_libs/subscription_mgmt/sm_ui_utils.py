import logging

from hpe_glcp_automation_lib.libs.sm.ui.device_subscriptions import DeviceSubscriptions

log = logging.getLogger(__name__)


class SmVerifier:
    """
    Subscription Management verifications class.
    """

    @staticmethod
    def check_device_subscription(dev_subscr_page: DeviceSubscriptions, device_details: dict):
        """Check that device subscription details are present at Device Subscriptions page.

        :param dev_subscr_page: instance of DeviceSubscriptions page-object class.
        :param device_details: dictionary with device details. "subscription_key" key is required for this method.
        """
        subscription_key = device_details["subscription_key"]
        dev_subscr_page \
            .wait_for_loaded_table() \
            .search_for_text(subscription_key) \
            .should_have_rows_count(1) \
            .should_have_row_with_values_in_columns({"Subscription Key": subscription_key})
