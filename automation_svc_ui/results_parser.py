import json
import logging
import os.path
import sys
from os import listdir
from os.path import isfile, join
from pathlib import Path

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.INFO)


def get_list_of_results_files(result_path):
    """
    This method iterates over given path and collect all files that have 'results.json' ending in their names
    :param result_path: Path where allure results files stored
    :return: List of filenames
    """
    return [f for f in listdir(result_path) if (isfile(join(result_path, f)) and "result.json" in f)]


def get_json_from_file(file_path):
    """
    This method converts file content into json object
    :param file_path: Path to the file (relative, from work directory), that need to be opened
    :return: Json object
    """
    return json.loads(Path(f"{file_path}").resolve().read_text())


def prepare_testrail_results_from_allure_json(source_dict):
    """
    This method generates TestRail compatible test result for particular test execution results
    E.g. {
    'case_id': 123,
    'status': 5,
    'comment': 'test_example test failed. AssertionError: ...',
    'description': 'This is example test case, that is ...'
    }
    :param source_dict: Json with test execution results (Allure format)
    :return: List with test execution result (json obj) , or empty (if test results don't have test case id)
    """
    test_case_ids = get_test_id_from_allure_result_dict(source_dict)
    test_results = []
    if source_dict["status"] == "passed":
        case_status = 1
    elif source_dict["status"] == "skipped":
        case_status = 3
    else:
        case_status = 5
    for test_id in test_case_ids:
        test_results.append({
            "case_id": test_id,
            "status_id": case_status,
            "comment": f"{source_dict.get('name')} test {source_dict['status']}. "
                       f"{source_dict.get('statusDetails', {}).get('message', '')}",
            "description": source_dict.get("description"),
        })
    return test_results


def get_test_id_from_allure_result_dict(source):
    """
    This method parses test's result tags to find test case id (like 'C123123' or 'testrail(id=123123))
    :param source: Json with test execution results (Allure format)
    :return: List of test case ID numbers (E.g. ['123123'])
    """
    ids = []
    for label in source.get("labels", {}):
        if label.get("value", "").startswith("C") and label.get("value")[1:].isdigit():
            ids.append(int(label["value"][1:]))
        elif label.get("value", "").startswith("testrail(id="):
            ids.append(int(label["value"].split("id=")[1][:-1]))
    return ids


def create_result_testrail_report(path):
    """
    This method generates one aggregated report for all tests within corresponding directory
    :param path:  Path where allure results files stored
    :return: Json object with TestRail tests execution results
    """
    results = []
    for file in get_list_of_results_files(path):
        test_results = prepare_testrail_results_from_allure_json(
            get_json_from_file(os.path.join(path, file))
        )
        for result in test_results:
            results.append(result)
    return {"results": results}


def write_down_report(report, result_path):
    """
    This method saves report file to corresponding path
    :param report: report Json object
    :param result_path: Path where report needs to be saved (by default in the Allure Results directory)
    """
    try:
        report_name = "test_rail_report.json"
        with open(f"{result_path}/{report_name}", "w") as f:
            f.write(json.dumps(report))
            log.info(
                f"TestRail report results was saved to '{result_path}/{report_name}' file successfully."
            )
    except Exception as e:
        log.info(e)
        pass


if __name__ == "__main__":
    filepath = None
    report_path = None
    default_results_path = Path("tmp/results").resolve()
    for index, arg in enumerate(sys.argv):
        if arg.startswith("--results_path"):
            if "=" in arg:
                filepath = Path(arg.split("=")[1]).resolve()
            else:
                filepath = Path(sys.argv[index + 1]).resolve()
        elif arg.startswith("--report_path"):
            if "=" in arg:
                report_path = Path(arg.split("=")[1]).resolve()
            else:
                report_path = Path(sys.argv[index + 1]).resolve()

    final_results_path = filepath if filepath else default_results_path
    final_report_path = report_path if report_path else default_results_path
    log.info(
        f"Starting to generate TestRail compatible report for '{final_results_path}' directory from Allure Results"
    )
    write_down_report(
        create_result_testrail_report(final_results_path), final_report_path
    )
