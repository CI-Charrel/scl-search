from flask import Flask,make_response
from flask_cors import CORS
from scl_search.search_utility import SEARCH
import json

search = Flask(__name__)
CORS(search)


@search.route("/")
def index():
    return "Welcome to SCL Search"


@search.route("/autocompletion/<string:keyword>")
def autocompletion(keyword):
    resp_data = {}
    instance = SEARCH()
    try:
        resp_data["data"] = instance.autocompletion(keyword)
        resp_data["status"] = "SUCCESS"
    except Exception as err:
        resp_data["status"] = "FAILED"

    resp = make_response(json.dumps(resp_data), 200)
    return resp


@search.route("/search/<string:keyword>")
def fti_search(keyword):
    resp_data = {}
    instance = SEARCH()
    try:
        resp_data["data"] = instance.fulltextsearch(keyword)
        resp_data["status"] = "SUCCESS"

    except Exception as err:
        resp_data["status"] = "FAILED"

    resp = make_response(json.dumps(resp_data), 200)
    return resp


if __name__ == "__main__":
    search.run()
    # http://127.0.0.1:13563/autocompletion/keyword
    # http://127.0.0.1:13563/search/keyword