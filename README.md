# 🐐 Robota.tej – Job Offer Aggregator

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-orange)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)

**Robota.tej** is an advanced ETL (Extract, Transform, Load) application and web service designed to aggregate job offers from the IT market in Greater Poland (Poznań area). The system automatically fetches announcements from multiple job boards, processes the data using Pandas, and presents it through a clean, user-friendly web interface with built-in market analytics.

## 🚀 Key Features

* **Multi-Source Scraping:** Aggregates data from major platforms: **OLX, Praca.pl, RocketJobs, and NoFluffJobs**.
* **Data Analysis & Mining:** Utilizes `Pandas` for data cleaning, normalization, and automated duplicate removal based on unique URLs.
* **Dynamic Market Analytics:** Features a module for technology popularity analysis (keyword mining) and job board market share statistics.
* **Strict Server-Side Logic:** All filtering, sorting, and pagination logic is implemented entirely in Python/Flask. No JavaScript is used for business logic, meeting strict academic requirements for this project.
* **Data Export:** Built-in functionality to export the current database state to an Excel (.xlsx) file for further offline analysis.

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask, Jinja2
* **Database:** SQLite3 (with custom REGEXP implementation for advanced filtering)
* **Data Science:** Pandas, NumPy
* **Scraping:** BeautifulSoup4, Requests (includes User-Agent rotation and anti-scraping delays)
* **Frontend:** HTML5, CSS3 (Custom responsive design, strictly no inline styles)

## 🏗️ Project Architecture

The project adheres to the **Separation of Concerns** principle through a two-app architecture:

1.  **App A (Collector - `main.py`):**
    * Orchestrates modules from the `collectors/` package.
    * Transforms raw HTML data into `pandas.DataFrame` structures.
    * Loads unique records into the SQLite database.
2.  **App B (Web Server - `run_server.py`):**
    * Handles HTTP routing and request processing.
    * Executes advanced SQL queries for data filtering.
    * Renders dynamic templates using the Jinja2 engine.
3.  **Business Logic & DAO (`analytics.py` & `db_manager.py`):**
    * `analytics.py`: Performs keyword extraction and statistical calculations.
    * `db_manager.py`: Implements the Data Access Object (DAO) pattern for secure database communication.

### File Structure

```text
robota_tej/
│
├── collectors/             # Python package with dedicated scraper modules
│   ├── scraper_nofluff.py
│   ├── scraper_olx.py
│   ├── scraper_pracapl.py
│   └── scraper_rocketjobs.py
│
├── data/                   # Directory for the SQLite database file
├── static/                 # External CSS styles (style.css)
├── templates/              # Jinja2 HTML templates (index.html, stats.html)
│
├── analytics.py            # Data mining and statistical analysis module
├── config.py               # Central configuration (paths, constants, URLs)
├── db_manager.py           # Database management and DAO layer
├── main.py                 # Entry point for the Scraping Pipeline (App A)
├── run_server.py           # Entry point for the Flask Web App (App B)
├── setup_db.py             # Database schema initialization script
└── requirements.txt        # Project dependencies
```
## ⚙️ Installation & Usage

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

4.  **Fetch job offers (Run Scrapers):**
    ```bash
    python main.py
    ```

5.  **Start the Web Server:**
    ```bash
    python run_server.py
    ```

6.  **Access the application:**
    Open `http://127.0.0.1:5000` in your browser.

## 📝 About

This project was developed as a final assignment for the course: *Python Applications in Economic Analysis*. It focuses on clean code principles, automated data acquisition, and semantic data analysis.
