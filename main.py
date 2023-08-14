import flask, os
import bs4
import requests

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/check', methods=['POST'])
def query():
    search_query = flask.request.form['query']
    api_key = os.environ.get("API_KEY")
    search_engine_id = os.environ.get("SEARCH_ENGINE_ID")
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={search_query}"
    res = requests.get(url).json()

    items = res["items"]
    for item in items:
        link = item["link"]
        print(link)
        if search_query in link:
            print("found") 
            break

    # not indexed
    

    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
