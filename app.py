# Import the Flask dependency.
from flask import Flask

# Create a new Flask app instance, called app - singular version of something.
app = Flask(__name__)

# Create routes
@app.route('/')
def hello_world():
    return 'Hello world'

#To run:
# Open Anaconda Powershell
# set FLASK_APP=app.py
# flask run







