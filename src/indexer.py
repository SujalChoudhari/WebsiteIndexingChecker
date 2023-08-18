import re
import requests
import bs4
import numpy as np
from src.sheet_manager import SpreadsheetManager
from src.url_manager import URLManager
from src.proxy_manager import ProxyManager
from src.progress_manager import ProgressManager
from src.constants import INDEXING_SEARCH_STRING

class Indexer:
    """
    # Indexer
    The main worker class that checks if a url is indexed
    It loops thorugh the gathered urls and checks if they are indexed

    Checking process:
        - Get the next url from the url manager
        - Check if the url is indexed
            - use requests to get the html of the url
            - use bs4 to parse the html
            c. use regex to find the indexing string
        - If the url is indexed, mark it as indexed in the url manager
        - If the url is not indexed, mark it as not indexed in the url manager
        - If a proxy fails, mark it as failed in the proxy manager
        - If the proxy manager runs out of proxies, mark the url as failed in the url manager
        - If more than 5 urls fail in a row, stop the process, exit
    """
    def __init__(
        self,
        proxy_manager: ProxyManager,
        url_manager: URLManager,
        sheet_manager: SpreadsheetManager,
    ):
        self.url_manager = url_manager
        self.sheet_manager = sheet_manager
        self.proxy_manager = proxy_manager
        self.unindexed_urls = np.array([])
        self.current_proxy = None

    def process(self):
        fail_count = 0
        while self.url_manager.has_more_urls():
            ProgressManager.update_progress("Progress: {}/{}".format(
                self.url_manager.current_url_index,
                len(self.url_manager.urls)
            ))

            url, is_indexed, status = self.check_next_url()
            print("URL " + url + " is indexed: " + str(is_indexed) + " Status: " + status)
            if not is_indexed and status == "checked":
                self.sheet_manager.add_unindexed_url(url)

            if status == "end":
                break
            elif status == "checked":
                fail_count = 0
            elif status == "failed":
                fail_count += 1
            
            if fail_count > 5:
                ProgressManager.update_progress("Failed consistently more than 5 times! Exiting Process...")
                ProgressManager.done_message = "Failed consistently 5 times! Exiting Process..."
                return
            
            if self.url_manager.current_url_index % 50 == 0:
                ProgressManager.update_progress("Saving unindexed urls to sheets...")
                self.sheet_manager.save_unindexed_to_sheets()

    def check_next_url(self):
        current_url = self.url_manager.get_next_url()
        if current_url is None:
            return "none", False, "end"
        try:
            response = self.proxy_request(INDEXING_SEARCH_STRING.format(current_url))
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            not_indexed_regex = re.compile("did not match any documents")
            if soup(text=not_indexed_regex):
                return current_url, False, "checked"
            else:
                return current_url, True, "checked"
            
        except Exception as e:
            print("Error: ", e)
            return current_url, False, "failed"

    def proxy_request(self, url, **kwargs):
        fail_count = 0
        while True:
            current_proxy = self.proxy_manager.get_proxy_for_request()

            if current_proxy is None:
                ProgressManager.update_progress("All given proxy failed")
                return requests.get(url, **kwargs)

            print("\n\nUsing Proxy: ", current_proxy["http"])
            try:
                response = requests.get(url, proxies=current_proxy, timeout=8)
                if response.status_code == 200:
                    print("\tSuccess!")
                    self.proxy_manager.update_proxy()
                    return response
                else:
                    print("\tFailed!",response.status_code)
                    self.proxy_manager.update_proxy()
            except Exception as e:
                print("\tFailed!",e)
                fail_count += 1
                self.proxy_manager.update_proxy()

                if fail_count > 30:
                    return requests.get(url,timeout=8)