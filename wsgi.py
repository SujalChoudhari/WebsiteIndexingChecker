import os
from app import app

"""
The entry point for the flask app.
It uses heroku's port if available, otherwise it uses port 5000
"""
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
