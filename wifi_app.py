from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    risk = None
    ssid = None

    if request.method == "POST":
        ssid = request.form["ssid"]

        try:
            df = pd.read_csv("wifi_dataset.csv")
            df_filtered = df[df["SSID"] == ssid]

            if df_filtered.empty:
                result = "No dataset info"
                risk = "Unknown"
            else:
                auth_types = df_filtered["Authentication"].nunique()
                risk_score = 0

                if auth_types > 1:
                    risk_score += 50

                if risk_score >= 50:
                    result = "Suspicious"
                else:
                    result = "Legitimate"

                risk = f"{risk_score}%"

        except:
            result = "Dataset not found"
            risk = "Error"

    return render_template("index.html", result=result, risk=risk, ssid=ssid)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)