import flask
import gspread

from src.url_manager import URLManager
from src.proxy_manager import ProxyManager
from src.indexer import Indexer
from src.sheet_manager import SpreadsheetManager
from src.helpers import (
    URL_TO_SHEETS,
    SERVICE_ACCOUNT_FILENAME,
    PROGRESS,
)



app = flask.Flask(__name__)
gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILENAME)
api = gc.open_by_url(URL_TO_SHEETS)

@app.route("/")
def index():
    return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS)

@app.route("/check", methods=["POST"])
def check():
    # pull proxies from text file
    proxy_file = flask.request.files['proxy-file']
    proxies = proxy_file.read().decode("utf-8").split("\n")
    proxy_manager = ProxyManager(proxies)

    # pull sitemaps from the spreadsheet
    spreadsheet_manager = SpreadsheetManager(SERVICE_ACCOUNT_FILENAME, URL_TO_SHEETS)

    # get all urls from the sitemaps as a manager
    url_manager = URLManager(spreadsheet_manager)
    url_manager.process()
    
    # run the checks
    index_checker = Indexer(proxy_manager,url_manager,spreadsheet_manager)
    index_checker.process()

    # end
    
    return flask.redirect(flask.url_for("index"))

@app.route("/api")
def return_data():
    return flask.jsonify(progress=PROGRESS)

if __name__ == "__main__":
    app.run(debug=True)
