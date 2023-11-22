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


def filter_suites_by_owner(path: str, owners_object: dict, owners_ids) -> Tuple[Dict[str, str | list], List[str]]:
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
                elif 'owners' in data and any(owner['name'] in owners_object['owners'] for owner in data['owners']):
                    with contextlib.suppress(KeyError):
                        suites_list[file_name] = [owners_ids[i['email']] for i in data['owners']]
    return suites_list, invalid_files_list


def collect_test_names_from_suites(suites_list: Dict[str, str | list], skip_folders: list) -> Dict[str, Dict[str, Any]]:
    suites_dict = {}

    for suite_file, owners in suites_list.items():
        full_paths = find_file_path(PATH, suite_file, skip_folders)

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


def count_test_and_suites(suites_dict: Dict[str, Dict[str, Any]]) -> Tuple[int, int]:
    t_count = 0
    s_count = 0
    for feature_obj in suites_dict.values():
        for feature_name, tests in feature_obj.items():
            for s_name, s_data in tests.items():
                t_count += len(s_data['test_name'])
                s_count += 1
    return t_count, s_count


def find_file_path(root_dir: str, file_name: str, skip_folders) -> list:
    path_list = []
    for dir_path, folder, filenames in os.walk(root_dir):
        if any(skip_folder in dir_path.split(os.sep) for skip_folder in skip_folders):
            continue
        if file_name in filenames:
            path_list.append(os.path.join(dir_path, file_name))
    return path_list


def find_suites_without_tests(suites_with_tests: Dict[str, Any], all_suite_list: Dict[str, str]) -> List[str]:
    return [i for i in all_suite_list if i not in suites_with_tests]


def get_owner_object(args):
    if args.json_file_path:
        target_dir = Path(args.json_file_path)
        if not target_dir.is_file():
            print("The target directory doesn't exist")
            raise SystemExit(1)

        owners_list = load_json_file(str(target_dir))
    else:
        owners_list = {
            "owners": args.owners,
            "exclude_cycles": args.exclude_cycles,
            "page_title": args.page_title,
            "parent_id": args.parent_id,
            "user": args.user,
            "token": args.token
        }
        if not owners_list.get('owners'):
            print(f"Check your Json, the format should be as below\n {json.loads(json_format_example)}")
            raise SystemExit(1)
    return owners_list


def prepare_page(suites, test_count, suite_count):
    page = ''
    for suite_name, suite_data in suites.items():
        page_creator = Page(suite_name, suite_data)
        page += page_creator.create_page()

    return f"""
     <p>The purpose of this document is to give an overview of all the tests reviewed by security-inline team.</p>
     <p>There are total of {test_count} test in {suite_count} suites</p>
     <p><ac:structured-macro ac:name=\"toc\"/></p>
     <p>{page}</p>
     """


def send_to_confluence(owners_list, final_html_content):
    client = confluence_connection(owners_list['user'], owners_list['token'])
    update_page(client, owners_list['parent_id'], owners_list['page_title'], final_html_content)


def main(args):
    owners_list = get_owner_object(args)
    owners_ids = load_json_file(os.path.join(PATH, 'qa_resources/infra/reporting', 'email_to_jira_account.json'))
    suite_list, invalid_files = filter_suites_by_owner(
        os.path.join(PATH, 'qa_resources', 'suite_owner'), owners_list, owners_ids)
    suites = collect_test_names_from_suites(suite_list, owners_list['exclude_cycles'])
    test_count, suite_count = count_test_and_suites(suites)
    final_html_content = prepare_page(suites, test_count, suite_count)
    send_to_confluence(owners_list, final_html_content.replace('\n', ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Command-line arguments
    parser.add_argument("--json_file_path", help="Path to the JSON file containing configuration and owner details.")
    parser.add_argument("--owners", nargs='*', help="List of owners.")
    parser.add_argument("--exclude_cycles", nargs='*', help="List of cycles to exclude.")
    parser.add_argument("--page_title", help="Title of the page.")
    parser.add_argument("--parent_id", help="Parent ID for the page.")
    parser.add_argument("--user", help="User for authentication.")
    parser.add_argument("--token", help="Token for authentication.")

    arguments = parser.parse_args()

    main(arguments)
