# Website Index Checker App

Welcome to the **Website Index Checker** app! This repository contains code that enables you to check if the URLs listed in a given sitemap are indexed by Google. This README provides instructions for team members on how to work with this app.

## Getting Started

To get started with the **Website Index Checker** app, follow these steps:

### 1. Modify Sheets URL
In the `constants.py` file, you will find a section where you need to modify the URLs related to Google Sheets and indexing search. Open the `constants.py` file and update the following variables:

```python
URL_TO_SHEETS = "https://docs.google.com/spreadsheets/d/1up6bYQj2X5XoYfS9aN8zAT5oz8dFQIGZlXCr_Madgug/edit#gid=1700410190"
INDEXING_SEARCH_STRING = "https://www.google.com/search?q=site:{}&num=1"
```
Also add the email of the google sheets api service account with the sheets. This is required to give the service account access to the sheet. 
*EMAIL can be found in service_account.json*
 
Replace the existing URLs with your own Google Sheets URL and indexing search string. Make sure to follow the correct format for URLs.

### 2. Update Service Account for Google Sheets API

The **Website Index Checker** app uses the gspread library to interact with Google Sheets API. You will need to provide a `service_account.json` file for authentication. Replace the existing `service_account.json` file in the root directory with your own service account JSON file. This file should be obtained from the Google Cloud Console.

sample file 
```js
{
    "type": "service_account",
    "project_id": "em...608",
    "private_key_id": "991d8f.....6e3d",
    "private_key": "-----BEGIN PRIVATE KEY-----\nM.....TA=\n-----END PRIVATE KEY-----\n",
    "client_email": "sit...am.gserviceaccount.com",
    "client_id": "103...5",
    "auth_uri": "htt...2/auth",
    "token_uri": "http...token",
    "auth_provider_x509_cert_url": "https:/...rts",
    "client_x509_cert_url": "http...t.com",
    "universe_domain": "go..om"
}
```

### 3. Dependencies and Hosting

The app is built using Flask, Requests, BeautifulSoup4, and gspread. It is hosted on Heroku using Gunicorn. Make sure you have the required dependencies installed. You can install the dependencies using the following command:

```bash
pip install -r requirements.txt
```

### 4. Running the App

Once you have set up the necessary configurations, you can run the app locally. Use the following command to start the Flask app:

```bash
python wsgi.py

# OR

flask run
```

The app will start running locally, and you can access it by navigating to `http://127.0.0.1:5000/` in your web browser.

## How the App Works

The **Website Index Checker** app checks if the URLs listed in the specified sitemap are indexed by Google. It does this by sending search queries to Google and checking if the URLs appear in the search results. The app uses a specific User-Agent and language settings for these requests.

## Questions or Issues

If you have any questions or encounter any issues while working with the app, please contact [@SujalChoudhari](https://github.com/SujalChoudhari).
Happy indexing!
