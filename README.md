
# Flask Auth & RBAC with Analytics

This is a production-ready Flask application featuring a complete user authentication system, Role-Based Access Control (RBAC), and an admin-only analytics dashboard.

## Features

* **User Authentication**: Secure user registration, login, and logout functionality. Passwords are fully hashed.
* **Role-Based Access Control (RBAC)**: Two distinct user roles: 'User' and 'Admin'.
* **Protected Routes**: Certain pages are only accessible to logged-in users.
* **Admin-Only Dashboard**: A special `/analytics` page is restricted to Admin users, demonstrating RBAC.
* **Activity Tracking**: The application records key user activities (registration, login) for analysis.

## Tech Stack

* **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Migrate
* **Database**: SQLite (for development), compatible with PostgreSQL for production.
* **Testing**: Pytest
* **Deployment**: Gunicorn, Docker

---

## Setup and Installation

### Prerequisites

* Python 3.8+
* A virtual environment tool (`venv`)

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd flask_rbac_analytics
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add a secret key:
    ```
    SECRET_KEY='a_very_strong_random_secret_key'
    ```

5.  **Initialize and upgrade the database:**
    ```bash
    # Set the Flask app environment variable
    # macOS/Linux: export FLASK_APP=run.py
    # Windows: set FLASK_APP=run.py

    flask db init  # Run this only once
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

6.  **Seed the database with default roles:**
    ```bash
    flask seed-roles
    ```

---

## How to Run

### Running the Development Server
```bash
flask run