# Defualts packages
import os

# For flask
from flask import Flask
from threading import Thread

# ----____Flask____----
app = Flask('')

@app.route('/')
def home():
    # Create new reddit object to update post every 5 min
    return ":D"

def run():
    app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ____----Flask----____