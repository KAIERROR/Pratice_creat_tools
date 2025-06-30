def valid_date(date_str):
    import re
    return re.match(r"^\d{4}/\d{2}/\d{2}$", date_str) is not None

def load_tasks(filename):
    import json
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks, filename):
    import json
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)