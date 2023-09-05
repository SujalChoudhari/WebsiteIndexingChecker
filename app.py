import threading
import time
import flask
from src.url_manager import URLManager
from src.proxy_manager import ProxyManager
from src.indexer import Indexer
from src.sheet_manager import SpreadsheetManager
from src.progress_manager import ProgressManager
from src.constants import URL_TO_SHEETS

app = flask.Flask(__name__)
check_lock = threading.Lock()

HAS_ERROR = False
ERROR = None

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Homepage route
    """
    global HAS_ERROR
    HAS_ERROR = False
    ProgressManager.update_progress("Working ...")
    return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS)


@app.route("/working", methods=["POST"])
def check():
    """
    The Main function that is ran to check the urls.
    This route is called by the UI when the user clicks the "Start" button
    Renders a done page when finished, with a message, or an error page if something went wrong
    """
    proxy_file = None
    if "proxy-file" in flask.request.files:
        proxy_file = flask.request.files["proxy-file"]

    def checker(proxy_file):
        """
        Main Runner function called when user presses `Start` button.
        This organizes the flow of the program
        Checks for any errors and updates the progress manager
        """
        global HAS_ERROR, ERROR
        proxy_manager = None
        spreadsheet_manager = None
        url_manager = None
        index_checker = None
        try:
            # pull proxies from text file
            ProgressManager.update_progress("Starting App ...", True)
            proxies = []
            if proxy_file is not None:
                proxies = proxy_file.read().decode("utf-8").split("\n")
            proxy_manager = ProxyManager(proxies)
        except Exception as exception:
            print("Proxy File Error: ", exception)
            ProgressManager.update_progress("Failed to load proxies: " + str(exception), False)
            HAS_ERROR = True
            ERROR = "Failed to load proxies: " + str(exception)
            return

        try:
            # pull sitemaps from the spreadsheet
            ProgressManager.update_progress("Loading Spreadsheet ...")
            spreadsheet_manager = SpreadsheetManager(URL_TO_SHEETS)

            # get all urls from the sitemaps as a manager
            ProgressManager.update_progress("Parsing URLs (this may take a while) ...")
            url_manager = URLManager(spreadsheet_manager)
            url_manager.process()
        except Exception as exception:
            print("Spreadsheet Error: ", exception)
            ProgressManager.update_progress(
                "Failed to load spreadsheet: " + str(exception), False
            )
            HAS_ERROR = True
            ERROR = "Failed to load spreadsheet: " + str(exception)
            return

        try:
            # run the checks
            ProgressManager.update_progress("Checking URLs ...")
            index_checker = Indexer(proxy_manager, url_manager, spreadsheet_manager)
            done_status = index_checker.process()
            if not done_status:
                HAS_ERROR = True
                ERROR = "Failed to run checks: failed multiple times"
            else:
                HAS_ERROR = False
                ERROR = None

            ProgressManager.update_progress("Checks Complete")
            # save unindexed
            spreadsheet_manager.save_unindexed_to_sheets("Checks Completed")
            ProgressManager.is_working = "False"

        except Exception as exception:
            print("Checker Error: ", exception)
            HAS_ERROR = True
            ERROR = "Failed to run checks: " + str(exception)
            ProgressManager.update_progress("Failed to run checks: " + str(exception), False)
            return

        ProgressManager.is_working = "False"
        time.sleep(6)
        ProgressManager.is_working = "True"

    if check_lock.acquire(blocking=False):  # Attempt to acquire the lock
        try:
            check_thread = threading.Thread(target=checker, args=(proxy_file,))
            check_thread.start()
            return flask.render_template("worker.html", url_to_sheets=URL_TO_SHEETS)
        finally:
            check_lock.release()  # Release the lock after thread execution
    else:
        return (
            "Please Wait, Another thread is already running.",
            503,
        )  # Service Unavailable


@app.route("/api", methods=["GET", "POST"])
def return_data():
    """
    Api for realtime updates for user, this is called by the frontend
    """
    return flask.jsonify(
        progress=ProgressManager.progress, is_working=ProgressManager.is_working
    )


@app.route("/done")
def done():
    if HAS_ERROR:
        return flask.render_template(
            "error.html",
            url_to_sheets=URL_TO_SHEETS,
            message="There was some errors while running:" if ERROR is None else ERROR,
        )
    return flask.render_template(
        "done.html", url_to_sheets=URL_TO_SHEETS, message=ProgressManager.done_message
    )
