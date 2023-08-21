import numpy as np
import gspread
from src.constants import URL_TO_SHEETS


class SpreadsheetManager:
    """
        # SpreadsheetManager
        SpreadsheetManager is a class that manages the spreadsheet.  
        It is a wrapper for the gspread library, specifically to manage the particular spreadsheet.
        It is responsible for getting the sitemap urls from the spreadsheet named `Sitemaps`
        It is also responsible for saving the unindexed urls to the spreadsheet named `Unindexed`

        # Requirements
        - The spreadsheet must have two sheets (worksheets) named `Sitemaps` and `Unindexed`. If there are no sheets with those names, they will be created.
        - The spreadsheet must be shared with the service account email address. This is found in the `SERVICE_ACCOUNT` file.

        # Note:
        - While saving the unindexed urls, it will delete the older urls and replace them with the new ones.
        - The spreadsheet is updated in realtime, so you can watch the progress of the script by opening the spreadsheet.

    """
    def __init__(self, url_to_sheet: str):
        self.gc = gspread.service_account("service_account.json")
        self.spreadsheet = self.gc.open_by_url(url_to_sheet)
        self.unindexed_urls = []
        self.sitemap_sheet = None
        self.unindexed_sheet = None
        self.setup_sheets()

    def setup_sheets(self):
        for sheet in self.spreadsheet.worksheets():
            if "sitemap" in sheet.title.lower():
                self.sitemap_sheet = sheet
            elif "unindex" in sheet.title.lower():
                self.unindexed_sheet = sheet

        if self.sitemap_sheet == None:
            self.sitemap_sheet = self.spreadsheet.add_worksheet("Sitemaps", 100, 1)

        if self.unindexed_sheet == None:
            self.unindexed_sheet = self.spreadsheet.add_worksheet("Unindexed", 100, 1)

    def add_unindexed_url(self, urls: str):
        self.unindexed_urls.append(urls)

    def get_sitemaps(self) -> list[str]:
        sitemaps = np.array(self.sitemap_sheet.get_values()).flatten()
        return sitemaps.tolist()

    def save_unindexed_to_sheets(self):
        self.update_unindexed_sheet_with(self.unindexed_urls)


    def update_unindexed_sheet_with(self, list_of_urls: list):
        if(len(list_of_urls) == 0):
            return
        self.unindexed_sheet.clear()  # Clear the existing content
        print("Updating unindexed sheet with:", list_of_urls)
        # Convert the list of URLs into a two-dimensional list using numpy
        urls_2d = np.array(list_of_urls).reshape(-1, 1).tolist()
        self.unindexed_sheet.append_rows(urls_2d)


if __name__ == "__main__":
    # Example usage
    filename = "service_account.json"
    url_to_sheet = URL_TO_SHEETS

    manager = SpreadsheetManager(filename, url_to_sheet)

    # Getting sitemaps
    sitemaps = manager.get_sitemaps()
    print("Sitemaps:", sitemaps)

    # Updating unindexed sheet
    manager.update_unindexed_sheet_with([["url1"], ["url2"]])
