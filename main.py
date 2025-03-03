from flask import Flask, request, jsonify
import random
import numpy as np
import markdown.extensions.fenced_code
import tools.sql_queries as queries
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

app = Flask(__name__)

# Render the markdown
@app.route("/")
def readme ():
    readme_file = open("ABOUT.md", "r")
    return markdown.markdown(readme_file.read(), extensions = ["fenced_code"])

# ENDPOINTS SQL
# ------------------------------------------

# SQL get everything
@app.route("/sql/all")
def sql ():
    return jsonify(queries.get_everything())

# SQL get everything from ONE speaker
@app.route("/sql/all/<name>")
def everything_from_speaker (name):
    return jsonify(queries.get_everything_from_speaker(name))

# SQL get everything from MULTIPLE speakers
@app.route("/sql/all/<name1>&<name2>&<name3>&<name4>")
def everything_from_multiple_speaker (name1,name2,name3,name4):
    return jsonify(queries.get_everything_from_multiple_speaker(name1,name2,name3,name4))

# SQL get only comms from ONE speaker
@app.route("/sql/comms/<name>")
def lines_from_speakers (name):
    return jsonify(queries.get_just_comms(name))

# SQL get only comms from MULTIPLE speakers
@app.route("/sql/comms/<name1>&<name2>&<name3>&<name4>")
def lines_from_multiple_speakers (name1, name2, name3, name4):
    return jsonify(queries.get_just_multiple_comms(name1, name2, name3, name4))


# SENTIMENT ANALYSIS
# ----------------------------------------

# SENTIMENT ANALYSIS from ONE speaker
@app.route("/sa/<name>")
def sa_from_speaker (name):
    everything = queries.get_just_comms(name)
    #return jsonify(everything)
    return jsonify([sia.polarity_scores(i["comms"])["compound"] for i in everything])

# SENTIMENT ANALYSIS from MULTIPLE speakers
@app.route("/sa/<name1>&<name2>&<name3>&<name4>")
def sa_from_multiple_speakers (name1, name2, name3, name4):
    everything = queries.get_just_multiple_comms(name1, name2, name3, name4)
    #return jsonify(everything)
    return jsonify([sia.polarity_scores(i["comms"])["compound"] for i in everything])

# POST AND DELETE
# -----------------------------------------

# POST
@app.route("/insertrow", methods=["POST"])
def try_post ():
    # Decoding params
    my_params = request.args
    mission_time = my_params["mission_time"]
    comms = my_params["comms"]
    speaker = my_params["speaker"]

    # Passing to my function: do the insert
    queries.insert_one_row(mission_time, comms, speaker)
    return f"Query succesfully inserted"

# DELETE
@app.route("/deleterow", methods=["POST"])
def try_delete ():
    # Decoding params
    my_params = request.args
    speaker = my_params["speaker"]

    # Passing to my function: remove
    queries.delete_one_row(speaker)
    return f"Query succesfully deleted"

if __name__ == "__main__":
    app.run(port=9000, debug=True)