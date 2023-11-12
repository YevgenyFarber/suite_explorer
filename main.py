import os
import json
from json import JSONDecodeError

OWNERS_LIST = ['Eden Ben Ezri', 'Tomer Girhish', 'Alon Ben Avraham', 'Samah Jumah', 'Yevgeny Farber']
PATH = '/Users/yevgenyfarber/work/qa/'


def extract_suits_by_owner(path):
    suite_list = []
    invalid_files = []
    for dir_path, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.lower().endswith('.json'):
                full_path = os.path.join(dir_path, file_name)
                try:
                    with open(full_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    if 'owners' in data and any(owner['name'] in OWNERS_LIST for owner in data['owners']):
                        suite_list.append(file_name)
                except JSONDecodeError as e:
                    print(f"JSONDecodeError: {e} in file {full_path}")
                    invalid_files.append(file_name)
                except Exception as e:
                    print(f"Exception: {e} in file {full_path}")
                    invalid_files.append(file_name)
    return suite_list, invalid_files


def find_file_path(root_dir, file_name):
    return next(
        (
            os.path.join(dirpath, file_name)
            for dirpath, dirnames, filenames in os.walk(root_dir)
            if file_name in filenames
        ),
        None,
    )


def get_test_names(root_dir, suite_list):
    suites = {}
    for dir_path, dir_names, file_names in os.walk(PATH):
        for file_name in file_names:
            if file_name.lower().endswith('.json') and file_name in suite_list:
                full_path = os.path.join(dir_path, file_name)
                try:
                    with open(full_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    if 'trafficTestGroups' in data:
                        tests = [test['name'] for test in data['trafficTestGroups']]
                        suites[file_name] = tests
                except JSONDecodeError as e:
                    print(f"JSONDecodeError: {e} in file {file_name}")
                except Exception as e:
                    print(f"Exception: {e} in file {file_name}")
    return suites


# Usage
if __name__ == '__main__':
    suite_list, invalid_files = extract_suits_by_owner('/Users/yevgenyfarber/work/qa/qa_resources/suite_owner')
    suites = get_test_names(PATH, suite_list)
    for suite, tests in suites.items():
        print(f"Suite: {suite} has tests: {tests}")
    if invalid_files:
        print(f"Invalid files encountered: {invalid_files}")
