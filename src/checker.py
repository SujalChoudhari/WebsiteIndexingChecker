import flask

from src.url_manager import URLManager
from src.proxy_manager import ProxyManager
from src.indexer import Indexer
from src.sheet_manager import SpreadsheetManager
from src.progress_manager import ProgressManager
from src.constants import URL_TO_SHEETS, SERVICE_ACCOUNT_FILENAME

def checker():
    """
        Main Runner function called when user presses `Start` button.
        This organizes the flow of the program
        Checks for any errors and updates the progress manager
    """
    try:
        # pull proxies from text file
        ProgressManager.update_progress("Starting App ...")
        proxy_file = flask.request.files["proxy-file"]
        proxies = proxy_file.read().decode("utf-8").split("\n")
        proxy_manager = ProxyManager(proxies)
    except Exception as e:
        print(e)
        ProgressManager.update_progress("Failed to load proxies: " + str(e),False)
        return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS, error=f"Failed to load proxies: {e}")

    try:
        # pull sitemaps from the spreadsheet
        ProgressManager.update_progress("Loading Spreadsheet ...")
        spreadsheet_manager = SpreadsheetManager(SERVICE_ACCOUNT_FILENAME, URL_TO_SHEETS)

        # get all urls from the sitemaps as a manager
        ProgressManager.update_progress("Parsing URLs (this may take a while) ...")
        url_manager = URLManager(spreadsheet_manager)
        url_manager.process()
    except Exception as e:
        print(e)
        ProgressManager.update_progress("Failed to load spreadsheet: " + str(e),False)
        return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS, error=f"Failed to load spreadsheet: {e}")

    try:
        # run the checks
        index_checker = Indexer(proxy_manager, url_manager, spreadsheet_manager)
        index_checker.process()
        ProgressManager.update_progress("Checks Complete")

        # save unindexed
        spreadsheet_manager.save_unindexed_to_sheets()
    except Exception as e:
        print(e)
        ProgressManager.update_progress("Failed to run checks: " + str(e),False)
        return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS, error=f"Failed to run checks: {e}")

    ProgressManager.update_progress("Done!", is_working=True)
