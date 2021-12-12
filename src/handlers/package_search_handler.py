#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint
import pandas as pd

pd.get_option("display.max_rows", 999)
# pd.set_option("display.max_colwidth", 85)
# pd.set_option("display.colheader_justify", "center")


class Package_Search_Handler:

    def __init__(self):
        self.matching_results = {}
        self.base_search = {}

    def refined_search(self, reg_search, pages=2):
        # for i in range(pages):
        #     base_search = self._fetch_packages(
        #         matching_results, search, i)
        # self.base_search.set_index('Name', inplace=True)
        # self._matching_searches1(self.base_search, reg_search)
        # return self.matching_results

        search_word = self._remove_regex(reg_search)
        self._fetch_packages1(
            self.matching_results, search_word, pages)
        self._matching_searches1(search_word)
        print(self.matching_results)

        # search_word = self._remove_regex(reg_search)
        # base_search = self._fetch_packages(
        #     self.matching_results, search_word, pages)
        # self._matching_searches(base_search, reg_search)
        # print(base_search)

        # pprint(self.matching_results)

    def _remove_regex(self, search):
        """Allows you to used regex in your package search"""
        plain_search = ""
        for i in search:
            pattern = "[a-zA-Z1-9]"
            result = re.match(pattern, i)
            if result:
                plain_search += i

        return plain_search

    def _fetch_packages1(self, matching_hm, search, page):
        """Does a basic search without regex"""
        html_doc = self._make_request(search, page)

        all_names = html_doc.find_all(class_="package-snippet__name")
        all_versions = html_doc.find_all(class_="package-snippet__version")
        all_releases = html_doc.find_all(class_="package-snippet__released")
        all_descriptions = html_doc.find_all(
            class_="package-snippet__description")

        all_names_strings = [x.string.strip() for x in all_names]
        all_versions_strings = [x.string.strip() for x in all_versions]
        all_releases_strings = [x.string.strip() for x in all_releases]
        all_description_strings = [x.string for x in all_descriptions]

        self.base_search = pd.DataFrame({
            "Name": all_names_strings,
            "Description": all_description_strings,
            "Version": all_versions_strings
        })

    def _fetch_packages(self, matching_hm, search, page):
        """Does a basic search without regex"""
        html_doc = self._make_request(search, page)

        all_names = html_doc.find_all(class_="package-snippet__name")
        all_versions = html_doc.find_all(class_="package-snippet__version")
        all_releases = html_doc.find_all(class_="package-snippet__released")
        all_descriptions = html_doc.find_all(
            class_="package-snippet__description")

        all_names_strings = [x.string.strip() for x in all_names]
        all_versions_strings = [x.string.strip() for x in all_versions]
        all_releases_strings = [x.string.strip() for x in all_releases]
        all_description_strings = [x.string for x in all_descriptions]

        hm = {
            "name": all_names_strings,
            "version": all_versions_strings,
            "release": all_releases_strings,
            "description": all_description_strings
        }
        return hm

    def _make_request(self, search, page):
        r = requests.get(f'https://pypi.org/search/?q={search}&page={page}')
        status = r.status_code
        print(f"STAUS REQUEST: {status}")
        html_text = r.text
        doc = BeautifulSoup(html_text, "html.parser")
        return doc

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
    reg_search = "pandas$"
    pages = 1
    package_repo.refined_search(reg_search)
    # package_repo.refined_search(reg_search, pages)
    # df = package_repo.to_data_frame()
    # print(df)
