import logging
import time
from enum import Enum
from typing import List, Optional

from hpe_glcp_automation_lib.libs.audit_logs.ui.audit_logs_page import AuditLogs

log = logging.getLogger(__name__)


class LogsEventType(Enum):
    """Enum-class containing supported types of Audit Logs events to be verified and related table fields values,
    assigned with them.
    """

    SUBSCRIPTION = {"category": "Subscription Management",
                    "description_template": ["Subscription key {subscr_key} is assigned to device serial: {serial_no}",
                                             "Serial: {serial_no} op: DEVICE_SUBSCRIPTION_ASSIGNED"]}
    CLAIM = {"category": "Device Management",
             "description_template": ["Device with serial {serial_no} and mac {mac} is added to account.",
                                      "Device with serial {serial_no} and mac {mac} is added to workspace."]}
    ASSIGN = {"category": "Device Management",
              "description_template": "Device with serial {serial_no} is assigned to application {app_short_name}"}
    UNASSIGN = \
        {"category": "Device Management",
         "description_template": "Device with serial {serial_no} is unassigned from application {app_short_name}"}

    @property
    def category(self):
        """Expected value in 'Category' field of Audit Logs table.
        """
        return self.value["category"]

    def expected_description(self, **kwargs):
        """Expected value in 'Description' field of Audit Logs table.

        :param kwargs: key-value pairs to be used for formatting description template for chosen event type.
            Following keys are expected:
                - 'serial_no' - for any type of event;
                - 'mac', 'app_short_name', 'subscr_key' - for some types of events.
        :return: list of valid text values; at least one of them is expected to be present in 'Description' field
            of Audit Logs table.
        """
        if isinstance(self.value["description_template"], list):
            description_templates = self.value["description_template"]
        else:
            description_templates = [self.value["description_template"]]
        expected_description_list = []
        for template in description_templates:
            expected_description_list.append(template.format(**kwargs))
        return expected_description_list


class AuditLogsVerifier:
    """
    Audit Logs verifications class.
    """

    @staticmethod
    def check_device_events(audit_logs_page: AuditLogs, event_types: List[LogsEventType], device_details: dict,
                            tries=5, **kwargs):
        """Check that device event details are present at Audit Logs page.

        :param audit_logs_page: instance of AuditLogs page-object class.
        :param event_types: list of log event types to be verified.
        :param device_details: dictionary with device details. Following keys are required for this method:
            "device_type", "serial_no", "mac".
        :param tries: number of tries until record with expected description appeared at Audit Logs table.
        :param kwargs: additional key-value pairs to be used for formatting of template for expected value.
            E.g.:
                - 'app_short_name' key is needed for 'LogsEventType.ASSIGN', 'LogsEventType.UNASSIGN' events.
                - 'subscr_key' key is needed for 'LogsEventType.SUBSCRIPTION' event.
        """
        device_serial_number = device_details.get("serial_no")
        log.info(f"Playwright: verifying audit logs of '{device_details.get('device_type')}' device "
                 f"with id '{device_serial_number}'...")
        description_data = device_details.copy()
        description_data.update(kwargs)
        expected_descriptions = []
        for log_event in event_types:
            audit_logs_page.search_for_text(device_serial_number, changed_rows_timeout=10)
            for i in range(tries):
                log.info(f"Playwright: verifying audit logs for event '{log_event.name}'.")
                if i > 0:
                    log.info(f"Retrying attempt: {i}.")
                    audit_logs_page.clear_search_field(changed_rows_timeout=10)
                    time.sleep(5)
                    audit_logs_page.search_for_text(device_serial_number, changed_rows_timeout=10)
                expected_descriptions = log_event.expected_description(**description_data)
                log.info(f"Expected 'Category': {log_event.category}")
                log.info(f"Expected 'Description': {expected_descriptions}")
                description_text = _choose_existing_value(audit_logs_page, "Description", expected_descriptions)
                if not description_text:
                    continue
                audit_logs_page \
                    .should_have_row_with_values_in_columns({"Category": log_event.category,
                                                             "Description": description_text}) \
                    .open_row_details("Description", description_text) \
                    .should_audit_log_item_have_details(description_text) \
                    .close_detail_dialog()
                break
            else:
                raise AssertionError(f"Not found rows with any of expected text values "
                                     f"at 'Description' column: '{expected_descriptions}'.")
            audit_logs_page.clear_search_field(changed_rows_timeout=10)

    @staticmethod
    def get_matched_log_events_count(audit_logs_page: AuditLogs, event_types: [LogsEventType], device_details: dict,
                                     **kwargs):
        """Get and return list of log-events count for each log-event, specified in 'event_types' and
        displayed in table. Order of numbers in returned list match to log-event types order in 'event_types' argument.

        :param audit_logs_page: instance of AuditLogs page-object class.
        :param event_types: list of log event types to be counted.
        :param device_details: dictionary with device details. Following keys are required for this method:
            "device_type", "serial_no", "mac".
        :param kwargs: additional key-value pairs to be used for formatting of template for expected value.
            E.g.:
                - 'app_short_name' key is needed for 'LogsEventType.ASSIGN', 'LogsEventType.UNASSIGN' events.
                - 'subscr_key' key is needed for 'LogsEventType.SUBSCRIPTION' event.
        :return: list of integers, representing counts of found records per specified log-event type.
        """
        device_serial_number = device_details.get("serial_no")
        events_count = []
        audit_logs_page.search_for_text(device_serial_number, changed_rows_timeout=10)
        for event_type in event_types:
            log.info(f"Playwright: getting count of log events for '{event_type.name}' event "
                     f"of '{device_details.get('device_type')}' device with id '{device_serial_number}'.")
            description_data = device_details.copy()
            description_data.update(kwargs)
            expected_descriptions = event_type.expected_description(**description_data)
            description_text = _choose_existing_value(audit_logs_page, "Description", expected_descriptions)
            if description_text:
                log_event_rows = audit_logs_page.table_utils.get_rows_indices_by_values_in_columns(
                    {"Category": event_type.category, "Description": description_text})
                events_count.append(len(log_event_rows))
            else:
                events_count.append(0)
        audit_logs_page.clear_search_field(changed_rows_timeout=10)
        return events_count

    @staticmethod
    def check_matched_log_event_count(audit_logs_page: AuditLogs, event_type: LogsEventType, device_details: dict,
                                      rows_count: int, **kwargs):
        """Verify count of log-event records of specified type in Audit Logs.

        :param audit_logs_page: instance of AuditLogs page-object class.
        :param event_type: log-event type, whose count is to be verified.
        :param device_details: dictionary with device details. Following keys are required for this method:
            "device_type", "serial_no", "mac".
        :param rows_count: expected count of rows with corresponding log-event.
        :param kwargs: additional key-value pairs to be used for formatting of template for expected value.
            E.g.:
                - 'app_short_name' key is needed for 'LogsEventType.ASSIGN', 'LogsEventType.UNASSIGN' events.
                - 'subscr_key' key is needed for 'LogsEventType.SUBSCRIPTION' event.
        :return: None if check successful or AssertionError otherwise.
        """
        device_serial_number = device_details.get("serial_no")
        log.info(f"Playwright: verifying audit logs for event '{event_type.name}' "
                 f"of '{device_details.get('device_type')}' device with id '{device_serial_number}'...")
        audit_logs_page.search_for_text(device_serial_number, changed_rows_timeout=10)
        description_data = device_details.copy()
        description_data.update(kwargs)
        expected_descriptions = event_type.expected_description(**description_data)
        log.info(f"Expected 'Category': {event_type.category}")
        log.info(f"Expected 'Description': {expected_descriptions}")
        description_text = _choose_existing_value(audit_logs_page, "Description", expected_descriptions)
        if not description_text:
            raise AssertionError(
                f"Not found rows with expected text values at 'Description' column: '{expected_descriptions}'.")
        audit_logs_page.should_matched_rows_count_be(
            {"Category": event_type.category, "Description": description_text}, count=rows_count)
        audit_logs_page.clear_search_field(changed_rows_timeout=10)


def _choose_existing_value(page, table_column: str, values_list: List[str]) -> Optional[str]:
    for value in values_list:
        log.info(f"Playwright: looking for description '{value}' in table.")
        matching_rows_indices = page.table_utils.get_rows_indices_by_text_in_column(table_column, value)
        if matching_rows_indices:
            return value
