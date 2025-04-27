# 📚 Student Assessment and Performance Tracker

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Relational%20DB-blue.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-In_Progress-important.svg)]()

---

## 📖 Project Description
**Student Performance Tracker** is a web-based application built for International Children's School Lekki, to automate the computation, tracking, and analysis of student academic performance.  
It helps teachers quickly enter scores, track students’ progress across academic terms, generate reports, and flag underperforming students for timely intervention.

---

## 📜 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [License](#license)

---

## 🚀 Features
- Manual entry or bulk upload of student scores via Excel/CSV
- Automatic computation of grades and averages
- Centralized student records using PostgreSQL
- Trend analysis and academic performance tracking
- Server-side visualization of trends using Matplotlib, Seaborn, or Plotly
- Early warning system to detect and highlight students at risk
- Export analyzed data to Power BI dashboards via REST API

---

## 🛠️ Installation

Follow these steps to set up **Student Performance Tracker** locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Maryam-20/student-performance-tracker.git
   cd gradeSystem
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   - Ensure PostgreSQL is installed and running.
   - Create a database and update `DATABASES` settings in `settings.py`.

5. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

---

## 📸 Usage

1. **Login to the Admin Portal or Teacher Dashboard**
2. **Enter Student Scores:**
   - Manually add scores via a web form OR
   - Upload Excel/CSV files.
3. **Automatic Computation:**
   - Grades, averages, and positions are auto-calculated.
4. **Visualize Performance:**
   - Access trend graphs and underperformance alerts.
5. **Export Data to Power BI:**
   - Sync computed data to Power BI via API for interactive dashboards.

**Example Screenshot:**

> ![Dashboard Screenshot](assets/dashboard_sample.png)

---

## 🧰 Technologies Used

- **Backend**
  - Python 3.10+
  - Django 4.x
  - Django ORM (for database interactions)

- **Frontend**
  - HTML5/CSS3
  - JavaScript
  - (Optionally) React.js for enhanced UI

- **Database**
  - PostgreSQL (Relational Structure)

- **Data Processing and Computation**
  - Numpy
  - Pandas

- **Visualization**
  - Matplotlib / Seaborn /

- **External Integrations**
  - Power BI REST API (for advanced reporting and dashboard automation)

---

## 📝 License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---