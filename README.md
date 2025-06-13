 MTN MoMo SMS Data Dashboard
Overview
This project is a fullstack enterprise-level application designed to process, store, and visualize mobile transaction data from MTN MoMo SMS messages in XML format. The goal is to extract meaningful insights from ~1600 real-world SMS entries using backend processing, relational databases, and a web-based frontend dashboard.

🛠️ Tech Stack
Backend: Python (XML Parsing, Data Cleaning, Logging)

Database: SQLite / MySQL / PostgreSQL

Frontend: HTML, CSS, JavaScript

(Optional) API: Flask / FastAPI / NodeJS

🔍 Key Features
✅ Backend: Data Processing
XML Parsing using xml.etree.ElementTree, lxml, or BeautifulSoup

Categorization of SMS into:

Incoming Money

Payments to Code Holders

Mobile Transfers

Bank Transactions

Airtime & Utility Payments

Internet/Bundle Purchases

Cleaning & Normalization: Dates, amounts, missing values

Logging: Unprocessed or invalid messages are logged for review

🗄️ Database
Schema Design: Optimized for transaction types

Data Insertion: Cleaned data stored with integrity checks

📊 Frontend: Dashboard
Search & Filter: By type, amount, and date

Visualizations:

Transaction volumes by type

Monthly summaries

Distribution charts

Details View: Expand to view full transaction info

🔗 (Optional) API
RESTful API to serve data to frontend dynamically

