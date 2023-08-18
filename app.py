import flask
import os
from src.url_manager import URLManager
from src.proxy_manager import ProxyManager
from src.indexer import Indexer
from src.sheet_manager import SpreadsheetManager
from src.progress_manager import ProgressManager
from src.constants import URL_TO_SHEETS, SERVICE_ACCOUNT_FILENAME

app = flask.Flask(__name__)


proxy_manager = None
spreadsheet_manager = None
url_manager = None
index_checker = None
fail_count = 0

@app.route("/",methods=['GET','POST'])
def index():
    """
        Homepage route
    """
    ProgressManager.update_progress("All Systems Running")
    return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS)


@app.route("/load-proxy", methods=["POST"])
def load_proxy():
    """
        The Main function that is ran to check the urls.
        This route is called by the UI when the user clicks the "Start" button
        Renders a done page when finished, with a message, or an error page if something went wrong
    """
    global proxy_manager
    try:
        # pull proxies from text file
        ProgressManager.update_progress("Starting App ...")
        proxy_file = flask.request.files["proxy-file"]
        proxies = proxy_file.read().decode("utf-8").split("\n")
        proxy_manager = ProxyManager(proxies)
    except Exception as e:
        print(e)
        ProgressManager.update_progress("Failed to load proxies: " + str(e),False)

    return flask.redirect(flask.url_for('load_sheets'))


@app.route('/load-sheet')
def load_sheets():
    global spreadsheet_manager,url_manager
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
    return flask.redirect(flask.url_for('check_index'))

@app.route('/check-index')
def check_index():
    global index_checker,fail_count
    try:
        # run the checks
        if index_checker == None:
            index_checker = Indexer(proxy_manager, url_manager, spreadsheet_manager)

        if fail_count > 10:
            raise Exception("Failed more than 10 times")
        
        if url_manager.has_more_urls():
            url, is_indexed, status = index_checker.process()
            if status == 'failed':
                fail_count +=1
            
            return flask.redirect(flask.url_for('check_index'))
        
        ProgressManager.update_progress("Checks Complete")
        # save unindexed
        spreadsheet_manager.save_unindexed_to_sheets()
    except Exception as e:
        print(e)
        ProgressManager.update_progress("Failed to run checks: " + str(e),False)

    ProgressManager.update_progress("Done!", is_working=True)
    return flask.render_template("done.html", message=ProgressManager.done_message)



@app.route("/api",methods=['GET','POST'])
def return_data():
    """
        Api for realtime updates for user, this is called by the frontend
    """
    return flask.jsonify(
        progress=ProgressManager.progress, is_working=ProgressManager.is_working
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
