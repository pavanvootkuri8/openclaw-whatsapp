from flask import Flask, render_template
import yaml
import os

app = Flask(__name__)

CONFIG_PATH = "/app/config/config.yaml"  # inside container
DATA_PATH = "/app/data/jobs.yaml"        # store scraped jobs

@app.route("/")
def home():
    jobs = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH) as f:
            jobs = yaml.safe_load(f) or []
    return render_template("index.html", jobs=jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
