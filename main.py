import flask
import gspread

from src.url_manager import URLManager
from src.proxy_manager import ProxyManager
from src.indexer import Indexer
from src.sheet_manager import SpreadsheetManager
from src.progress_manager import ProgressManager
from src.helpers import URL_TO_SHEETS, SERVICE_ACCOUNT_FILENAME


app = flask.Flask(__name__)
gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILENAME)
api = gc.open_by_url(URL_TO_SHEETS)


@app.route("/")
def index():
    ProgressManager.update_progress("All Systems Working")
    return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS)


@app.route("/check", methods=["POST"])
def check():
    try:
        # pull proxies from text file
        ProgressManager.update_progress("Starting...")
        proxy_file = flask.request.files["proxy-file"]
        proxies = proxy_file.read().decode("utf-8").split("\n")
        proxy_manager = ProxyManager(proxies)
        ProgressManager.update_progress("Proxies Loaded")
    except Exception as e:
        ProgressManager.update_progress("Failed to load proxies: " + str(e),False)
        return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS, error=f"Failed to load proxies: {e}")

    try:
        # pull sitemaps from the spreadsheet
        ProgressManager.update_progress("Loading Spreadsheet ...")
        spreadsheet_manager = SpreadsheetManager(SERVICE_ACCOUNT_FILENAME, URL_TO_SHEETS)

        # get all urls from the sitemaps as a manager
        ProgressManager.update_progress("Loading URLs ...")
        url_manager = URLManager(spreadsheet_manager)
        url_manager.process()
    except Exception as e:
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
        ProgressManager.update_progress("Failed to run checks: " + str(e),False)
        return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS, error=f"Failed to run checks: {e}")

    ProgressManager.update_progress("Done!", is_working=True)
    return flask.render_template("done.html", message=ProgressManager.done_message)


@app.route("/api")
def return_data():
    return flask.jsonify(
        progress=ProgressManager.progress, is_working=ProgressManager.is_working
    )


if __name__ == "__main__":
    app.run(debug=True)
