#!/usr/bin/python3

from rich.console import Console
from rich.table import Table
from rich import box
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import re
# source: https://github.com/victorgarric/pip_search/blob/master/pip_search/pip_search.py


class Package_Repo_Handler:

    def search(self, query: str, pages):
        api_url = 'https://pypi.org/search/'
        snippets = []
        s = requests.Session()
        for page in range(pages):
            params = {'q': query, 'page': page}
            r = s.get(api_url, params=params)
            soup = BeautifulSoup(r.text, 'html.parser')
            snippets += soup.select('a[class*="snippet"]')
            if not hasattr(s, 'start_url'):
                s.start_url = r.url.rsplit('&page', maxsplit=1).pop(0)

        table = Table(box=box.ROUNDED)
        table.add_column('Package', style='bold blue', no_wrap=True)
        table.add_column('Version', style='yellow')
        table.add_column('Released', style='bold green')
        table.add_column('Description', style='cyan')
        for snippet in snippets:
            package = re.sub(
                r"\s+", " ", snippet.select_one('span[class*="name"]').text.strip())
            version = re.sub(
                r"\s+", " ", snippet.select_one('span[class*="version"]').text.strip())
            released = re.sub(
                r"\s+", " ", snippet.select_one('span[class*="released"]').text.strip())
            description = re.sub(
                r"\s+", " ", snippet.select_one('p[class*="description"]').text.strip())
            table.add_row(f'{package}', version, released,
                          description, end_section=True)

        console = Console()
        console.print(table)
        return


if __name__ == "__main__":
    package_repo_handler = Package_Repo_Handler()
    package_repo_handler.search("^pandas")
