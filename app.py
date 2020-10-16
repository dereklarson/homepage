import os
import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.send_from_directory("./", "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 8000), debug=True)
