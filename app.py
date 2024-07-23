import os
import json
import pandas as pd
from flask import Flask, render_template, send_file
from homeharvest import scrape_property

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape")
def scrape():
    properties_df = scrape_property(
        location="San Diego, CA",
        listing_type="sold",
        past_days=30
    )
    properties = properties_df.to_dict(orient='records')
    
    os.makedirs('data', exist_ok=True)
    with open('data/results.json', 'w') as f:
        json.dump(properties, f, default=str)
    
    return render_template("results.html", properties=properties)

@app.route("/download")
def download():
    properties_df = scrape_property(
        location="San Diego, CA",
        listing_type="sold",
        past_days=30
    )
    file_path = 'data/results.xlsx'
    properties_df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    app.run(debug=True)
