import os
import json
import pandas as pd
from flask import Flask, render_template, send_file, request, jsonify
from homeharvest import scrape_property

app = Flask(__name__)

app.jinja_env.globals.update(min=min, max=max)


def save_results(properties_df):
    os.makedirs('data', exist_ok=True)
    with open('data/results.json', 'w') as f:
        json.dump(properties_df.to_dict(orient='records'), f, default=str)

def sort_properties(properties_df, sort_by, order):
    ascending = True if order == 'asc' else False
    return properties_df.sort_values(by=sort_by, ascending=ascending)

def filter_properties(properties_df, filter_by, filter_value):
    try:
        return properties_df[properties_df[filter_by] == filter_value]
    except KeyError:
        return properties_df  # If the filter property doesn't exist, return the unfiltered DataFrame


@app.route("/")
def index():
    return render_template("index.html")

import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/scrape", methods=["GET"])
def scrape():
    location = request.args.get('location', 'San Diego, CA')
    listing_type = request.args.get('listing_type', 'sold')
    past_days = int(request.args.get('past_days', 30))
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    output_format = request.args.get('format', 'json')  # Default to 'json'

    properties_df = scrape_property(
        location=location,
        listing_type=listing_type,
        past_days=past_days
    )
    total_properties = len(properties_df)
    total_pages = (total_properties + per_page - 1) // per_page
    properties = properties_df.iloc[(
        page - 1) * per_page: page * per_page].to_dict(orient='records')

    os.makedirs('data', exist_ok=True)
    with open('data/results.json', 'w') as f:
        json.dump(properties, f, default=str)

    response = {
        'page': page,
        'total_pages': total_pages,
        'total_properties': total_properties,
        'properties': properties
    }

    # Debug log to check which response is being returned
    logging.debug(f"Response format: {output_format}")
    logging.debug(f"Response data: {response}")

    # Return JSON if the format is 'json', otherwise render the HTML template
    if output_format == 'json':
        return jsonify(response)
    else:
        return render_template("results.html", properties=properties, page=page, total_pages=total_pages)

@app.route("/search", methods=["GET"])
def search():
    location = request.args.get('location', 'San Diego, CA')
    listing_type = request.args.get('listing_type', 'sold')
    past_days = int(request.args.get('past_days', 30))
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    query = request.args.get('query', '')
    sort_by = request.args.get('sort_by', '')
    order = request.args.get('order', 'asc')
    filter_by = request.args.get('filter_by', '')
    filter_value = request.args.get('filter_value', '')
    output_format = request.args.get('format', 'json')  # Add parameter for output format

    # Scrape new data
    properties_df = scrape_property(
        location=location,
        listing_type=listing_type,
        past_days=past_days
    )

    # Save the scraped data
    save_results(properties_df)

    # Filtering
    if filter_by and filter_value:
        properties_df = filter_properties(
            properties_df, filter_by, filter_value)

    # Searching
    if query:
        properties_df = properties_df[
            properties_df.apply(lambda row: query.lower() in row.astype(
                str).str.lower().to_dict().values(), axis=1)
        ]

    # Sorting
    if sort_by:
        properties_df = sort_properties(properties_df, sort_by, order)

    total_properties = len(properties_df)
    total_pages = (total_properties + per_page - 1) // per_page
    properties = properties_df.iloc[(
        page - 1) * per_page: page * per_page].to_dict(orient='records')

    response = {
        'page': page,
        'total_pages': total_pages,
        'total_properties': total_properties,
        'properties': properties
    }

    # Return JSON if the format is 'json', otherwise render the HTML template
    if output_format == 'json':
        return jsonify(response)
    else:
        return render_template("search_results.html", properties=properties, page=page, total_pages=total_pages)



@app.route("/download")
def download():
    properties_df = scrape_property(
        location="San Diego, CA",
        listing_type="sold",
        past_days=30
    )

    properties_df['primary_photo'] = properties_df['primary_photo'].apply(
        lambda x: x[:2000] if isinstance(x, str) and len(x) > 2000 else x)
    properties_df = properties_df.drop(columns=['alt_photos'])

    file_path = 'data/results.xlsx'
    properties_df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


if __name__ == "__main__":
    app.run(debug=True)
