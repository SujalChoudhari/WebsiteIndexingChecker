import gspread
import numpy as np
import os
from src.helpers import URL_TO_SHEETS


class SpreadsheetManager:
    def __init__(self, filename: str, url_to_sheet: str):
        self.gc = gspread.service_account(filename=filename)
        self.spreadsheet = self.gc.open_by_url(url_to_sheet)
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

    def get_sitemaps(self) -> list[str]:
        sitemaps = np.array(self.sitemap_sheet.get_values()).flatten()
        return sitemaps.tolist()

    def update_unindexed_sheet(self, data: list):
        self.unindexed_sheet.clear()  # Clear the existing content
        self.unindexed_sheet.append_rows(data)  # Append the new data


if __name__ == "__main__":
    # Example usage
    filename = "service_account.json"
    url_to_sheet = URL_TO_SHEETS

    manager = SpreadsheetManager(filename, url_to_sheet)

    # Getting sitemaps
    sitemaps = manager.get_sitemaps()
    print("Sitemaps:", sitemaps)

    # Updating unindexed sheet
    manager.update_unindexed_sheet([["url1"], ["url2"]])
