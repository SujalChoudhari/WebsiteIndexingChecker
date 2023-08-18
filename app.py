import flask
from src.progress_manager import ProgressManager
from src.constants import URL_TO_SHEETS
from src.checker import checker

app = flask.Flask(__name__)

@app.route("/")
def index():
    """
        Homepage route
    """
    ProgressManager.update_progress("All Systems Running")
    return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS)



@app.route("/check", methods=["POST"])
def check():
    """
        The Main function that is ran to check the urls.
        This route is called by the UI when the user clicks the "Start" button
        Renders a done page when finished, with a message, or an error page if something went wrong
    """
    checker() # this is the function that does the work
    return flask.render_template("done.html", message=ProgressManager.done_message)



@app.route("/api")
def return_data():
    """
        Api for realtime updates for user, this is called by the frontend
    """
    return flask.jsonify(
        progress=ProgressManager.progress, is_working=ProgressManager.is_working
    )



app.run(debug=True)