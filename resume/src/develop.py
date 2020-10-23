import flask
import os

# import subprocess
# from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


port = 8765
app = flask.Flask(__name__)
app.debug = True


class CreatePDF(LoggingEventHandler):
    def dispatch(self, event):
        os.system("./makepdf.sh")


@app.route("/")
def show_index():
    return flask.send_from_directory(".", "index.html")


@app.route("/pdf/")
def show_static_pdf():
    return flask.send_from_directory("../build", "my_resume.pdf")


if __name__ == "__main__":
    # observer = Observer()
    # observer.schedule(CreatePDF(), "src", recursive=False)
    # observer.start()
    app.run(host="0.0.0.0", port=os.environ.get("PORT", port))
