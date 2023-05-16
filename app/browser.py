import json

from datetime import datetime
from pathlib import Path


class DirectoryBrowser:
    def get_saved_files_list(self):
        target_dir = f"{Path.cwd()}/app/logs"

        filenames = [file.name for file in Path(target_dir).iterdir() if file.is_file() and file.name[-5:] == '.json']
        sorted_filenames = sorted(filenames, key=lambda x: datetime.strptime(x[:-5], '%d.%m.%Y'), reverse=True)
        return sorted_filenames

    def save_new_file(self, date: str, content) -> bool:
        target_dir = f"{Path.cwd()}/app/logs"
        print(f"Prepared to save loaded data to file: {date}.json")
        with open(f"{target_dir}/{date}.json", "w", encoding="utf-8") as file:
            json.dump(content, file)