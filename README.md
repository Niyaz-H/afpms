# Sustainable Agile Factory Production Management System (A-FPMS)

This project is a comprehensive Full Stack application built with Python/Django and Django REST Framework (DRF). It is designed to simulate a real-world challenge for a Full Stack Django Developer role.

The application, the **"Sustainable Agile Factory Production Management System" (A-FPMS)**, focuses on optimizing small-batch garment manufacturing to reduce overproduction and promote sustainability.

## Features

*   **Role-Based Authentication:** Custom user roles for "Factory Manager" and "Demand Planner" with appropriate permissions.
*   **Database Modeling:** A comprehensive database schema with optimized queries using `select_related` and `prefetch_related`.
*   **REST API:** A robust REST API built with DRF for managing production batches, with token-based authentication.
*   **Advanced Django Features:** Implementation of signals, custom management commands, and caching.
*   **LLM Simulation:** A simulated service for demand forecasting.
*   **Front-end:** A user-friendly front-end built with Django Templates and styled with Tailwind CSS.
*   **Deployment Ready:** The application is containerized with Docker and includes a plan for deployment to AWS.

## Getting Started

### Prerequisites

*   Python 3.10+
*   Django 5.2+
*   Django REST Framework 3.15+

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Niyaz-H/afpms.git
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the database migrations:
    ```bash
    py manage.py migrate
    ```
4.  Create a superuser:
    ```bash
    py manage.py createsuperuser
    ```
5.  Run the development server:
    ```bash
    py manage.py runserver
    ```

The application will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Running the Custom Management Command

To generate a sustainability report, run the following command:
```bash
py manage.py generate_sustainability_report