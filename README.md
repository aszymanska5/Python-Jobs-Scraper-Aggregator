# 🐐 Robota.tej – Job Offer Aggregator

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-orange)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)

**Robota.tej** is an ETL (Extract, Transform, Load) application and a web service designed to aggregate job offers from the IT market in Greater Poland (Poznań area). The system automatically fetches announcements from popular job boards, processes the data, and presents it in a clean, user-friendly interface.

## 🚀 Key Features

* **Multi-Source Scraping:** Fetches data from 3 major platforms: **OLX, Praca.pl, RocketJobs**.
* **Data Analysis:** Uses `Pandas` for data cleaning, normalization, and duplicate removal.
* **Server-Side Filtering:** Advanced filtering and sorting logic implemented entirely in Python (Backend), with **no JavaScript** used for business logic (Strict Requirement).
* **Market Analytics:** Built-in module for keyword extraction (Text Mining) and source statistics.
* **Clean Architecture:** Strict separation between the Data Collection Layer (Scraper) and the Presentation Layer (Web App).

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask, Jinja2
* **Database:** SQLite3
* **Data Science:** Pandas, NumPy (for statistics)
* **Scraping:** BeautifulSoup4, Requests
* **Frontend:** HTML5, CSS3 (Custom CSS, Responsive Design)

## 🏗️ Project Architecture

The project follows the **Separation of Concerns** principle:

1.  **App A (Collector - `main.py`):**
    * Orchestrates dedicated modules from the `collectors/` package.
    * Transforms raw HTML data into `pandas.DataFrame`.
    * Loads unique records into the SQLite database.
2.  **App B (Web Server - `run_server.py`):**
    * Reads processed data from the database.
    * Handles HTTP routing and request processing.
    * Renders HTML templates using Jinja2.
3.  **Business Logic (`analytics.py`):**
    * Handles keyword extraction and statistical analysis, keeping the views clean.

### File Structure

```text
robota_tej/
│
├── collectors/             # Python package containing scraper modules
│   ├── scraper_olx.py
│   ├── scraper_pracapl.py
│   └── scraper_rocketjobs.py
│
├── data/                   # Directory for the SQLite database
├── static/                 # CSS styles and static assets
├── templates/              # HTML templates (Jinja2)
│
├── analytics.py            # Analytics module (keyword mining, stats)
├── config.py               # Central configuration (paths, constants)
├── db_manager.py           # Data Access Object (DAO) layer
├── main.py                 # Entry point for the Scraping Pipeline
├── run_server.py           # Entry point for the Flask Web App
├── setup_db.py             # Database initialization script
└── requirements.txt        # Project dependencies
```

## ⚙️ Installation & Usage

To run the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/aszymanska5/Python-Jobs-Scraper-Aggregator.git
    cd Python-Jobs-Scraper-Aggregator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the database:**
    ```bash
    python setup_db.py
    ```

4.  **Fetch offers (Run Scrapers):**
    Execute the scraper to populate the database (this may take approx. 30-60 seconds).
    ```bash
    python main.py
    ```

5.  **Run the Web Server:**
    ```bash
    python run_server.py
    ```

6.  **Open the application:**
    Go to: `http://127.0.0.1:5001` in your browser.

## 📊 Features Overview

* **Dashboard:** List of job offers with pagination, sorting, and source filtering.
* **Statistics:** Charts showing technology popularity (keywords) and job board market share.

## 📝 About

Project realized as a final assignment for the course: *Python Applications in Economic Analysis*.