# suite_explorer

# Script can be triggered in 2 ways:
    1. From command line with all argument below
    python3 main.py --owners "Eden Ben Ezri" "Tomer Girhish" "Alon Ben Avraham" "Samah Jumah" "Zafrir Yakir" "Yevgeny Farber" --exclude_cycles conf_ci conf_doron --page_title YevgenyTesting --parent_id 2780823557 --user yevgeny.farber@catonetworks.com --token your_token
    
    2. From command line with path to json:
    python3 main.py --json_file_path /path/to/your/json_file.json

# JSON format example

```javascript
{
  "owners" :
    [
    "Eden Ben Ezri",
    "Tomer Girhish",
    "Alon Ben Avraham",
    "Samah Jumah",
    "Zafrir Yakir",
    "Yevgeny Farber"
  ],
  "exclude_cycles": [
    "conf_ci",
    "conf_doron"
  ],
  "page_title": "Page Title",
  "parent_id": "2780823557",
  "user": "your.mail@catonetworks.com",
  "token": "your_token"
}
```