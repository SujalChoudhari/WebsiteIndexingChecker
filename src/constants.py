import os
URL_TO_SHEETS = os.environ.get("URL_TO_SHEETS","https://docs.google.com/spreadsheets/d/1up6bYQj2X5XoYfS9aN8zAT5oz8dFQIGZlXCr_Madgug/edit#gid=1700410190")
SERVICE_ACCOUNT_FILENAME = os.environ.get("SERVICE_ACCOUNT_FILENAME","service_account.json")
INDEXING_SEARCH_STRING = "https://www.google.com/search?q=site:{}&num=1"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Accept-Language": "en-US,en;q=0.9",
}
