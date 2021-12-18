#!/usr/bin/python3
import asyncio
import json
import os
from pprint import pprint
import re
from rich.console import Console
from rich.table import Table
from rich import box
from time import sleep


class Package_Search_Handler:

    def __init__(self):
        self.matching_results = {}
        self.base_search = {}

    def refined_search(self, reg_search, pages=2):
        # search_json = os.popen(
        #     f"scala ./pip-search.jar {reg_search}").read().strip()
        # search_dictionary = json.loads(search_json)
        # self.prettify_search(search_dictionary)
        print(os.getcwd())
        return

    def prettify_search(self, package_info_dictionary):
        table = Table(box=box.ROUNDED)
        table.add_column('Package', style='bold blue', no_wrap=True)
        table.add_column('Version', style='blue')
        # table.add_column('Released', style='bold green')
        table.add_column('Description', style='bold cyan')
        for (package_name, package_info) in package_info_dictionary.items():
            package = package_name
            version = package_info["Version"]
            description = package_info["Description"]
            table.add_row(f'{package}', version, description)

        console = Console()
        console.print(table)
        return

    def _remove_regex(self, search):
        """Allows you to used regex in your package search"""
        plain_search = ""
        for i in search:
            pattern = "[a-zA-Z1-9]"
            result = re.match(pattern, i)
            if result:
                plain_search += i

        return plain_search

    def _matching_searches1(self, reg_search):
        df = self.base_search
        regex = re.compile(reg_search)
        self.matching_results = df[regex.match(
            df["Name"].str)].sort_values(by="Name")

    def _matching_searches(self, hm, reg_search):
        hm1 = {}
        for i in range(len(hm["name"])):
            name = hm["name"][i]
            version = hm["version"][i]
            release = hm["release"][i]
            description = hm["description"][i]
            hm1[name] = {
                "version": version,
                "release": release,
                "description": description
            }

        for key, value in hm1.items():
            if re.match(reg_search, key):
                self.matching_results[key] = value


if __name__ == "__main__":
    package_repo = Package_Search_Handler()
    reg_search = "pandas"
    pages = 1
    package_repo.refined_search(reg_search)
    # package_repo.refined_search(reg_search, pages)
    # df = package_repo.to_data_frame()
    # print(df)
