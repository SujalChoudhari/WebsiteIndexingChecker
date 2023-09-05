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
    - The spreadsheet must have two sheets (worksheets) named `Sitemaps` and `Unindexed`.
    If there are no sheets with those names, they will be created.
    - The spreadsheet must be shared with the service account email address. This is found in the `SERVICE_ACCOUNT` file.

    # Note:
    - While saving the unindexed urls, it will delete the older urls and replace them with the new ones.
    - The spreadsheet is updated in realtime, so you can watch the progress of the script by opening the spreadsheet.

    """

    def __init__(self, url_to_sheet: str):
        self.google_sheet_account = gspread.service_account("service_account.json")
        self.spreadsheet = self.google_sheet_account.open_by_url(url_to_sheet)
        self.unindexed_urls = []
        self.sitemap_sheet = None
        self.unindexed_sheet = None
        self.unindexed_count_sheet = None
        self.setup_sheets()

    def setup_sheets(self):
        for sheet in self.spreadsheet.worksheets():
            if "sitemap" in sheet.title.lower():
                self.sitemap_sheet = sheet
            elif "unindex" in sheet.title.lower():
                self.unindexed_sheet = sheet
            elif "count" in sheet.title.lower():
                self.unindexed_count_sheet = sheet

        if self.sitemap_sheet is None:
            self.sitemap_sheet = self.spreadsheet.add_worksheet("Sitemaps", 100, 2)

        if self.unindexed_sheet is None:
            self.unindexed_sheet = self.spreadsheet.add_worksheet("Unindexed", 100, 1)

        if self.unindexed_count_sheet is None:
            self.unindexed_count_sheet = self.spreadsheet.add_worksheet("Count", 100, 3)

    def add_unindexed_url(self, urls: str):
        self.unindexed_urls.append(urls)

    def get_sitemaps(self) -> list[str]:
        sitemaps = np.array(self.sitemap_sheet.col_values(1)).flatten()
        return sitemaps.tolist()

    def save_unindexed_to_sheets(self, status: str):
        self.update_unindexed_sheet_with(self.unindexed_urls, status)

    def update_unindexed_sheet_with(self, list_of_urls: list, status: [str]):
        if len(list_of_urls) == 0:
            return
        self.unindexed_sheet.clear()  # Clear the existing content
        print("Updating unindexed sheet with:", list_of_urls)
        # Convert the list of URLs into a two-dimensional list using numpy
        urls_2d = np.array(list_of_urls).reshape(-1, 1).tolist()
        self.unindexed_sheet.append_row([status])
        self.unindexed_sheet.append_rows(urls_2d)

    def get_count_sheet_as_dict(self) -> dict:
        # Read data from the sheet
        data = self.unindexed_count_sheet.get_all_values()

        # Extract headers and rows
        _ = data[0]
        rows = data[1:]

        # Convert the data into a dictionary
        count_sheet_dict = {}
        for row in rows:
            link = row[0]
            status = row[1]
            count = row[2]
            count_sheet_dict[link] = {"status": status, "count": count}

        return count_sheet_dict


    def save_count_data_dict_to_sheet(self, data_dict: dict):
        # Clear the existing data in the sheet
        self.unindexed_count_sheet.clear()

        # Write the headers back to the sheet
        headers = ['Link', 'Current Status', 'Count']
        self.unindexed_count_sheet.append_row(headers)

        # Create a 2D array to hold the data
        rows = []
        for link, info in data_dict.items():
            row_data = [link, info['status'], info['count']]
            rows.append(row_data)

        # Use append_rows to add all rows in a single API call
        self.unindexed_count_sheet.append_rows(rows)
