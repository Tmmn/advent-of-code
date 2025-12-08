import requests
from pathlib import Path
import datetime
import json
import argparse


# downloads files and creates template
# inspired by @danpfister (https://github.com/danpfister/advent-of-code/tree/main)
class AOCDownloader:

    def __init__(self, args) -> None:
        self.root_dir = Path(__file__).parent
        self.today = datetime.date.today()
        self.args = args
        self.day = self.args.day if self.args.day is not None else self.today.day
        self.year = self.args.year if self.args.year is not None else self.today.year
        self.day_dir = self.root_dir / f"{self.year}" / f"{self.day:0>2}"
        self.template = self.read_template()

        self.create_folder()
        self.get_input()
        self.create_new_py()
        self.create_example()

    def get_session_cookie(self):
        try:
            with open(self.root_dir / 'config.json', 'r') as config_file:
                data = json.load(config_file)
            return data['session_cookie']
        except:
            print("reading config.json failed!")
            raise

    def read_template(self):
        try:
            with open(self.root_dir / 'template.py', 'r') as template_file:
                template = template_file.readlines()
        except:
            print("reading python template failed!")
            raise
        return template

    def create_folder(self):
        if not self.day_dir.exists():
            self.day_dir.mkdir()
            return
        print(f"folder {self.day:0>2} already exists")

    def get_input(self):
        text_file_path = self.day_dir / f"{self.day:0>2}.txt"
        if not text_file_path.is_file():
            url = f"https://adventofcode.com/{self.year}/day/{self.day}/input"
            cookies = {'session': self.get_session_cookie()}
            params = {
                "User-Agent": 'https://github.com/Tmmn/advent-of-code',
            }
            try:
                request = requests.get(url=url, cookies=cookies, params=params)
                text_file_path.write_text(request.text)
                print(f"downloaded input file to {text_file_path}")
            except Exception as e:
                print("aoc request failed!")
                raise requests.RequestException(e)
            return
        print("input file for day already exists")

    def create_new_py(self):
        py_file_path = self.day_dir / f"{self.day:0>2}.py"
        if not py_file_path.is_file():
            with open(py_file_path, "w", encoding="utf-8") as file:
                file.writelines(self.template)
            print(f"created python file at {py_file_path}")
            return
        print("python file for current day already exists")

    def create_example(self):
        example_file_path = self.day_dir / f"ex{self.day:0>2}.txt"
        if not example_file_path.is_file():
            with open(example_file_path, "w"):
                print(f"created example file at {example_file_path}")
            return
        print("example file for current day already exists")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Input downloader for Advent of Code")
    parser.add_argument('-d', '--day', help="force download of specific day", default=None, required=False, type=int)
    parser.add_argument('-y', '--year', help="force download of specific year", default=None, required=False, type=int)
    arguments = parser.parse_args()
    AOCDownloader(args=arguments)
