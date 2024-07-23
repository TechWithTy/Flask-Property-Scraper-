# Project README

## Overview

This project is a Flask web application that scrapes real estate data and displays it in a user-friendly interface. Users can view, search, filter, and sort property listings. Additionally, they can download the data in Excel format.

## Features

1. **Data Scraping**: Scrapes property data based on location, listing type, and date range.
2. **Data Display**: Displays property data in a grid layout with responsive design using Tailwind CSS.
3. **Search and Filter**: Allows searching and filtering of property listings.
4. **Pagination**: Supports pagination to navigate through multiple pages of listings.
5. **Carousel**: Displays property images in a carousel with lazy loading.
6. **Download Data**: Provides an option to download the property data in Excel format.

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/tailwind-flask-starter.git
    cd tailwind-flask-starter
    ```

2. **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Application**:
    ```sh
    flask run
    ```

5. **Run the tailwind server**:
``` npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch```
## Usage

### Scraping Data

To scrape property data, navigate to `/scrape` endpoint with the required query parameters:

- `location`: Location to scrape data from (default: 'San Diego, CA')
- `listing_type`: Type of listing (default: 'sold')
- `past_days`: Number of past days to consider (default: 30)
- `page`: Page number for pagination (default: 1)
- `per_page`: Number of properties per page (default: 10)

Example:
```sh
curl -G -d "location=San Diego, CA" -d "listing_type=sold" -d "past_days=30" -d "page=1" -d "per_page=10" http://127.0.0.1:5000/scrape
```

### Searching Data

To search property data, use the `/search` endpoint with optional query parameters:

- `query`: Search term
- `sort_by`: Attribute to sort by (e.g., 'price', 'beds')
- `order`: Sort order ('asc' or 'desc')
- `filter_by`: Attribute to filter by (e.g., 'city')
- `filter_value`: Value to filter by

Example:
```sh
curl -G -d "query=Rancho Bernardo" -d "sort_by=price" -d "order=desc" -d "filter_by=city" -d "filter_value=San Diego" http://127.0.0.1:5000/search
```

### Downloading Data

To download property data, use the `/download` endpoint.

Example:
```sh
curl -O http://127.0.0.1:5000/download
```

## Code Changes

### `app.py`

- **Scrape Endpoint**: Added functionality to scrape property data and save it as `results.json`.
- **Search Endpoint**: Implemented search functionality with filtering, sorting, and pagination. It checks if `results.json` exists, scrapes data if it doesn't, and returns both HTML and JSON responses.
- **Download Endpoint**: Added an endpoint to download property data in Excel format.

```python
@app.route("/scrape", methods=["GET"])
def scrape():
    # Scrape data and save as JSON
    # ...

@app.route("/search", methods=["GET"])
def search():
    # Search, filter, sort, and paginate data
    # ...

@app.route("/download")
def download():
    # Download data as Excel file
    # ...
```

### `results.html`

- **Grid Layout**: Updated to display property listings in a responsive grid layout using Tailwind CSS.
- **Pagination**: Added pagination controls.
- **Carousel**: Implemented image carousel with lazy loading.
- **Search Bar**: Added search bar in the navbar to perform searches.

```html
<!-- Search Bar in Navbar -->
<form method="GET" action="/search">
    <input type="text" name="query" placeholder="Search..." />
    <button type="submit">Search</button>
</form>

<!-- Property Grid -->
<div class="grid-container">
    {% for property in properties %}
    <div class="property-card">
        <!-- Carousel and Property Details -->
    </div>
    {% endfor %}
</div>

<!-- Pagination -->
<div class="flex justify-center mt-5">
    <nav aria-label="Page navigation">
        <ul class="inline-flex items-center -space-x-px">
            <!-- Pagination Controls -->
        </ul>
    </nav>
</div>
```

### `utility.py`

- **Utility Functions**: Added functions for sorting and filtering properties.

```python
def sort_properties(df, sort_by, order='asc'):
    # Sorting logic
    return df

def filter_properties(df, filter_by, filter_value):
    # Filtering logic
    return df
```

## License

This project is licensed under the MIT License.

## Acknowledgments

- Tailwind CSS for styling
- Flask for the web framework
- Flowbite for UI components

---

Feel free to reach out if you have any questions or need further assistance.

---

### Note:

This README provides an overview and instructions for the project. Adjust the content and links as per your project's actual details.