import numpy as np
import requests
import bs4
import time
from src.sheet_manager import SpreadsheetManager
from src.url_manager import URLManager
from src.proxy_manager import ProxyManager
from src.progress_manager import ProgressManager
from src.helpers import INDEXING_SEARCH_STRING


class Indexer:
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
            ProgressManager.update_progress("Progress: {}/{} Failed: {}".format(
                self.url_manager.current_url_index,
                len(self.url_manager.urls),
                fail_count
            ))

            url, is_indexed, status = self.check_next_url()
            ProgressManager.update_progress("URL " + url + " is indexed: " + str(is_indexed) + " Status: " + status)
            print("URL " + url + " is indexed: " + str(is_indexed) + " Status: " + status)
            if not is_indexed and status == "checked":
                self.sheet_manager.add_unindexed_url(url)

            if status == "failed":
                ProgressManager.update_progress("Failed to get response from url: " + url)
                fail_count += 1
            
            if fail_count > 10:
                ProgressManager.update_progress("Failed more than 10 times! Exiting Process...")
                ProgressManager.done_message = "Failed more than 10 times! Exiting Process..."
                return
            
            if self.url_manager.current_url_index % 20 == 0:
                ProgressManager.update_progress("Saving unindexed urls to sheets...")
                self.sheet_manager.save_unindexed_to_sheets()


    def check_next_url(self):
        current_url = self.url_manager.get_next_url()
        response = self.proxy_request(INDEXING_SEARCH_STRING.format(current_url))
        if response.status_code != 200:
            return current_url, False, "failed"
        
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        result = soup.find_all("a", href=True)
        result = [x["href"] for x in result]

        for url in result:
            if current_url in url:
                return current_url, True, "checked"

        return current_url, False, "checked"

    def proxy_request(self, url, **kwargs):
        while self.proxy_manager.get_remaining_proxies_amount() > 0:
            current_proxy = self.proxy_manager.get_proxy_for_request()

            if current_proxy is None:
                ProgressManager.update_progress("No proxies found! Using normal request...")
                return requests.get(url, **kwargs)

            print("Using Proxy: ", current_proxy["http"], end=" ")
            try:
                response = requests.get(url, proxies=current_proxy, timeout=8)
                if response.status_code == 200:
                    print("\tSuccess!")
                    self.proxy_manager.update_proxy()
                    return response
                else:
                    print("\tFailed!")
                    self.proxy_manager.update_proxy()
                    self.proxy_manager.current_proxy_failed()
            except Exception as e:
                print("\tFailed!")
                self.proxy_manager.current_proxy_failed()
                self.proxy_manager.update_proxy()

        print("No proxies left!")
        ProgressManager.update_progress("No proxies left! Using normal request...")
        time.sleep(1)
        response = requests.get(url, **kwargs)
        if response.status_code != 200:
            print("Failed to get response from url: ", url)
        return response
