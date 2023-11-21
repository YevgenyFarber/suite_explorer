import contextlib
import os
import json
from pathlib import Path
import argparse
from typing import List, Tuple, Dict, Optional, Any
from contextlib import suppress

from confluence_connector import confluence_connection
from page_actions import update_page
from page_creator import Page

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


def filter_suites_by_owner(path: str) -> Tuple[Dict[str, str | list], List[str]]:
    suites_list: Dict[str, str | list] = {}
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
                    with contextlib.suppress(KeyError):
                        suites_list[file_name] = [OWNERS_IDS[i['name']] for i in data['owners']]
    return suites_list, invalid_files_list


def collect_test_names_from_suites(suites_list: Dict[str, str | list]) -> Dict[str, Dict[str, Any]]:
    suites_dict = {}

    for suite_file, owners in suites_list.items():
        full_paths = find_file_path(PATH, suite_file)

        for path in full_paths:
            data = load_json_file(path)
            if not data or 'trafficTestGroups' not in data or not data.get('group_name'):
                continue

            group_name = data['group_name']
            feature_name = data.get('feature_name', '')
            suites_dict.setdefault(group_name, {}).setdefault(feature_name, {})
            suite_entry = suites_dict[group_name][feature_name].setdefault(suite_file, {
                'test_name': [],
                'path': '',
                'owners': owners
            })

            suite_entry['test_name'].extend(i['name'] for i in data['trafficTestGroups'])

            new_path = path.replace(f'{PATH}tests/', '').replace(f'/suites/{suite_file}', '')
            if suite_entry['path']:
                suite_entry['path'] += f"<br />{new_path}"
            else:
                suite_entry['path'] = new_path

    return suites_dict


def find_file_path(root_dir: str, file_name: str) -> list:
    path_list = []
    for dir_path, _, filenames in os.walk(root_dir):
        if file_name in filenames:
            path_list.append(os.path.join(dir_path, file_name))
    return path_list


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
    OWNERS_IDS = owners_list
    suite_list, invalid_files = filter_suites_by_owner(os.path.join(PATH, 'qa_resources', 'suite_owner'))
    suites = collect_test_names_from_suites(suite_list)
    page = ''
    count = 0
    with open("result_object.json", 'w', encoding='UTF-8') as fp:
        json.dump(suites, fp, indent=4, ensure_ascii=False)
    for suite_name, suite_data in suites.items():
        page_creator = Page(suite_name, suite_data)
        page += page_creator.create_page()

    final_html_content = f"""
     <p>The purpose of this document is to give an overview of all the tests reviewed by security-inline team.</p>
     <p><ac:structured-macro ac:name=\"toc\"/></p>
     <p>{page}</p>
     """

    client = confluence_connection('yevgeny.farber@catonetworks.com', 'ATATT3xFfGF0VLt_CaxpIUEk2GmbWbAdOY650omxMFAicxRJ6KokUUQ-lwY4P5u3M7MGwLexB7wRQzi4ntgIgJwPX-tPMtLrVk88bVDqbLdP8oMQWb8rgut23E1WEEIXGqpay80L9iN33Q1tBeHFCKIQWT-etTMKqBFCDQ0FLPdSVCbXm0mVt0A=1009B3C6')
    update_page(client, '2780823557', 'YevgenyTesting', final_html_content)
    print()
    # with open("myfile.txt", "a") as f:
    #     for suite, tests in suites.items():
    #         f.write('\n')
    #         f.write(f'{suite} - {tests["path"]} - {tests["owners"]}\n')
    #         for test_name in tests['test_name']:
    #             f.write(f'\t{test_name}\n')
    #         count += len(tests['test_name'])
    #     f.write('\n')
    #     f.write(f'Total suites count: {len(suites)}\n')
    #     f.write(f'Total tests count: {count}')
