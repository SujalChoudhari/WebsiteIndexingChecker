import flask
import os
import threading
from src.url_manager import URLManager
from src.proxy_manager import ProxyManager
from src.indexer import Indexer
from src.sheet_manager import SpreadsheetManager
from src.progress_manager import ProgressManager
from src.constants import URL_TO_SHEETS, SERVICE_ACCOUNT_FILENAME

app = flask.Flask(__name__)

def checker(proxy_file):
    """
        Main Runner function called when user presses `Start` button.
        This organizes the flow of the program
        Checks for any errors and updates the progress manager
    """
    try:
        # pull proxies from text file
        ProgressManager.update_progress("Starting App ...")
        proxies = proxy_file.read().decode("utf-8").split("\n")
        proxy_manager = ProxyManager(proxies)
    except Exception as e:
        print(e)
        ProgressManager.update_progress("Failed to load proxies: " + str(e),False)

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

    try:
        # run the checks
        ProgressManager.update_progress("Checking URLs ...")
        index_checker = Indexer(proxy_manager, url_manager, spreadsheet_manager)
        index_checker.process()
        ProgressManager.update_progress("Checks Complete")

        # save unindexed
        spreadsheet_manager.save_unindexed_to_sheets()
    except Exception as e:
        print(e)
        ProgressManager.update_progress("Failed to run checks: " + str(e),False)

    ProgressManager.update_progress("Done!", is_working=False)

@app.route("/",methods=['GET','POST'])
def index():
    """
        Homepage route
    """
    ProgressManager.update_progress("All Systems Running")
    return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS)


@app.route("/working", methods=["POST"])
def check():
    """
        The Main function that is ran to check the urls.
        This route is called by the UI when the user clicks the "Start" button
        Renders a done page when finished, with a message, or an error page if something went wrong
    """
    proxy_file = flask.request.files["proxy-file"]
    check_thread = threading.Thread(target=checker,args=(proxy_file,))
    check_thread.start()
    return flask.render_template("worker.html",url_to_sheets=URL_TO_SHEETS)


@app.route("/api",methods=['GET','POST'])
def return_data():
    """
        Api for realtime updates for user, this is called by the frontend
    """
    return flask.jsonify(
        progress=ProgressManager.progress, is_working=ProgressManager.is_working
    )


@app.route('/done')
def done():
    return flask.render_template('done.html',url_to_sheets=URL_TO_SHEETS,message=ProgressManager.done_message)


@app.route('/worker')
def worker():
    return flask.render_template('worker.html',message=ProgressManager.done_message)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
