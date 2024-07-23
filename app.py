import os
import json
import pandas as pd
from flask import Flask, render_template, send_file, request, jsonify
from homeharvest import scrape_property

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape", methods=["GET"])
def scrape():
    page = int(request.args.get('page', 1))
    per_page = 10  # Number of properties per page
    properties_df = scrape_property(
        location="San Diego, CA",
        listing_type="sold",
        past_days=30
    )
    total_properties = len(properties_df)
    total_pages = (total_properties + per_page - 1) // per_page
    properties = properties_df.iloc[(page - 1) * per_page: page * per_page].to_dict(orient='records')
    
    os.makedirs('data', exist_ok=True)
    with open('data/results.json', 'w') as f:
        json.dump(properties, f, default=str)

    if request.headers.get('Accept') == 'application/json':
        return jsonify({
            'properties': properties,
            'page': page,
            'total_pages': total_pages
        })
    
    return render_template("results.html", properties=properties, page=page, total_pages=total_pages)

@app.route("/download")
def download():
    properties_df = scrape_property(
        location="San Diego, CA",
        listing_type="sold",
        past_days=30
    )

    # Remove or truncate columns with URLs to avoid Excel URL length limit errors
    properties_df['primary_photo'] = properties_df['primary_photo'].apply(lambda x: x[:2000] if isinstance(x, str) and len(x) > 2000 else x)
    properties_df = properties_df.drop(columns=['alt_photos'])

    file_path = 'data/results.xlsx'
    properties_df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    app.run(debug=True)
