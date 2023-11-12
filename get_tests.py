import os
import json
from pathlib import Path
import argparse


from typing import List, Tuple, Dict, Optional, Any
from contextlib import suppress

PATH: str = f'{str(Path.home())}/work/qa/'
OWNERS_LIST = None

json_format_example = '''{
  "owners": [
    "name1", "name2"
  ]
}
'''


def is_json_file(file_name: str) -> bool:
    return os.path.splitext(file_name)[1].lower() == '.json'


def load_json_file(full_path: str) -> Optional[Any]:
    with suppress(json.JSONDecodeError), open(full_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    return None


def save_json_file(full_path: str, data: json) -> Optional[Any]:
    with suppress(json.JSONDecodeError), open(full_path, 'w', encoding='utf-8') as file:
        return json.dump(data, file, indent=2, ensure_ascii=False)
    return None


def filter_suites_by_owner(path: str) -> Tuple[List[str], List[str]]:
    suites_list: List[str] = []
    invalid_files_list: List[str] = []
    for dir_path, _, file_names in os.walk(path):
        for file_name in file_names:
            if is_json_file(file_name):
                full_path = os.path.join(dir_path, file_name)
                data = load_json_file(full_path)
                if data is None:
                    print(f"Invalid JSON format in file: {full_path}")
                    invalid_files_list.append(file_name)
                elif 'owners' in data and any(owner['name'] in OWNERS_LIST for owner in data['owners']):
                    suites_list.append(file_name)
    return suites_list, invalid_files_list


def get_all_owners_and_suites(path: str) -> Tuple[Dict[str, str], List[str]]:
    suites_list: Dict[str, str] = {}
    invalid_files_list: List[str] = []
    for dir_path, _, file_names in os.walk(path):
        for file_name in file_names:
            if is_json_file(file_name):
                full_path = os.path.join(dir_path, file_name)
                data = load_json_file(full_path)
                if data is None:
                    print(f"Invalid JSON format in file: {full_path}")
                    invalid_files_list.append(file_name)
                else:
                    suites_list[file_name] = ', '.join([f"{i['name']} - {i['email']}" for i in data['owners']])
    return suites_list, invalid_files_list


def collect_test_names_from_suites(suites_list: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    suites_dict: Dict[str, Dict[str, Any]] = {}
    test_name_missing = []
    for suite_file, owners in suites_list.items():
        if full_path := find_file_path(PATH, suite_file):
            data = load_json_file(full_path)
            save_json_file(full_path, data)
            if data and 'trafficTestGroups' in data:
                try:
                    suites_dict[suite_file] = {
                        'test_name': [i['name'] for i in data['trafficTestGroups']],
                        'path': full_path.replace(
                            f'{PATH}tests/', '').replace(
                            f'/suites/{suite_file}', ''),
                        'owners': owners
                    }
                except KeyError:
                    test_name_missing.append(suite_file)
    return suites_dict


def find_file_path(root_dir: str, file_name: str) -> Optional[str]:
    return next(
        (
            os.path.join(dir_path, file_name)
            for dir_path, _, filenames in os.walk(root_dir)
            if file_name in filenames
        ),
        None,
    )


def find_suites_without_tests(suites_with_tests: Dict[str, Any], all_suite_list: Dict[str, str]) -> List[str]:
    return [i for i in all_suite_list if i not in suites_with_tests]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("path")

    args = parser.parse_args()

    target_dir = Path(args.path)

    if not target_dir.is_file():
        print("The target directory doesn't exist")
        raise SystemExit(1)

    owners_list = load_json_file(str(target_dir))
    if not owners_list.get('owners'):
        print(f"Check your Json, the format should be as below\n {json.loads(json_format_example)}")
        raise SystemExit(1)
    OWNERS_LIST = owners_list['owners']
    suite_list, invalid_files = get_all_owners_and_suites(os.path.join(PATH, 'qa_resources', 'suite_owner'))
    # suite_list, invalid_files = filter_suites_by_owner(os.path.join(PATH, 'qa_resources', 'suite_owner'))
    suites = collect_test_names_from_suites(suite_list)
    suites_without_tests = find_suites_without_tests(suites, suite_list)
    count = 0
    with open("myfile.txt", "a") as f:
        for suite, tests in suites.items():
            f.write('\n')
            f.write(f'{suite} - {tests["path"]} - {tests["owners"]}\n')
            for test_name in tests['test_name']:
                f.write(f'\t{test_name}\n')
            count += len(tests['test_name'])
        f.write('\n')
        f.write(f'Total suites count: {len(suites)}\n')
        f.write(f'Total tests count: {count}')
    print()
