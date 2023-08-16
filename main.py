import flask, os
import bs4, gspread
import requests
import numpy as np

app = flask.Flask(__name__)
gc = gspread.service_account(filename="service_account.json")

URL_TO_SHEETS = "https://docs.google.com/spreadsheets/d/1up6bYQj2X5XoYfS9aN8zAT5oz8dFQIGZlXCr_Madgug/edit#gid=1700410190"
api = gc.open_by_url(URL_TO_SHEETS)
SEARCH_API_KEY = os.environ.get("API_KEY")
SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID")
BASE_URL_FOR_SEARCH = f"https://www.googleapis.com/customsearch/v1?key={{api_key}}&cx={{search_engine_id}}&q=site:{{search_query}}"
MAX_SEARCH_COUNT = 2
PROGRESS = "All Systems Running"


@app.route("/")
def index():
    update_progress("All Systems Running")
    return flask.render_template("index.html", url_to_sheets=URL_TO_SHEETS)


@app.route("/check", methods=["POST"])
def check():
    # get the xml url

    all_urls = get_url_from_xml(flask.request.form["xml-url"])
    current_search_engine_id = (
        flask.request.form["search-engine-id"]
        if flask.request.form["search-engine-id"] != ""
        else SEARCH_ENGINE_ID
    )
    current_api_key_for_google_search = (
        flask.request.form["api-key"]
        if flask.request.form["api-key"] != ""
        else SEARCH_API_KEY
    )

    upper_limit_for_indexer = (
        int(flask.request.form["max-search-count"])
        if flask.request.form["max-search-count"] != ""
        else MAX_SEARCH_COUNT
    )
    check_executor_function(
        current_api_key_for_google_search,
        current_search_engine_id,
        upper_limit_for_indexer,
        all_urls,
    )

    update_progress("Process complete")
    return flask.redirect(flask.url_for("index"))


@app.route("/api")
def return_data():
    return flask.jsonify(progress=PROGRESS)


def update_progress(_progress):
    global PROGRESS
    PROGRESS = _progress


def check_executor_function(
    api_key_for_google_search, search_engine_id, upper_limit_for_indexer, all_urls
):
    un_indexed_urls = np.array(api.get_worksheet(0).get_all_values()).flatten()
    indexed_urls = np.array(api.get_worksheet(1).get_all_values()).flatten()
    total_urls = np.concatenate([un_indexed_urls, indexed_urls])

    to_add_indexed_urls = []
    to_add_unindexed_urls = []

    update_progress(f"Checking only top {upper_limit_for_indexer} new urls")

    count = 0
    for url in all_urls:
        if count >= upper_limit_for_indexer:
            break
        if url not in total_urls:
            is_indexed, status = check_for_indexing(
                api_key_for_google_search, search_engine_id, url
            )
            count += 1
            if is_indexed:
                to_add_indexed_urls.append(url)
                
            else:
                to_add_unindexed_urls.append(url)

            if status == "error":
                update_progress(
                    "429 error hit, stopping the process. Wait for 24 hrs or use another api key"
                )
            
            update_progress(f"Checked {count} urls. Indexed: {len(to_add_indexed_urls)}, Unindexed: {len(to_add_unindexed_urls)}")

    update_progress("Adding the urls to the sheet")
    add_new_indexed_urls(to_add_indexed_urls)
    add_new_unindexed_urls(to_add_unindexed_urls)


def add_new_indexed_urls(urls):
    indexed_sheet = api.get_worksheet(1)
    for url in urls:
        indexed_sheet.append_row([url])


def add_new_unindexed_urls(urls):
    unindexed_sheet = api.get_worksheet(0)
    for url in urls:
        unindexed_sheet.append_row([url])


def check_for_indexing(api_key, cx, search_query):
    responce = requests.get(
        BASE_URL_FOR_SEARCH.format(
            api_key=api_key, search_engine_id=cx, search_query=search_query
        )
    )

    print(responce.status_code)
    responce_as_json = responce.json()

    if responce.status_code == 200:  # everything is fine
        items = responce_as_json["items"]
        links = []
        for item in items:
            link = item["link"]
            links.append(link)
            # check if the results have the search query, if yes add it to the indexed list
            print(link, "=" , search_query)
            if search_query in link:
                return True, "checked"

    elif responce.status_code == 429:  # if 429 error hits
        return False, "error"

    else:  # link is not indexed
        return False, "checked"


def get_url_from_xml(xml_url):
    update_progress("Retrieving the XML file...")

    if not xml_url.endswith(".xml"):
        return [xml_url]

    res = requests.get(xml_url)
    soup = bs4.BeautifulSoup(res.text, features="xml")
    urls = soup.find_all("loc")
    result_urls = []
    for url in urls:
        url = url.text
        if url.endswith(".xml"):
            update_progress("Found Xml files in the sitemap. Retrieving the urls...")
            result_urls.extend(get_url_from_xml(url))
        else:
            result_urls.append(url)

    update_progress("Done retrieving the urls")
    return result_urls


if __name__ == "__main__":
    app.run(debug=True)