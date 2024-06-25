# Project Description

This project is a Flask application for managing cloud alerts. It includes functionality to create, clear, update, and delete alerts, as well as list all alerts or only alarms. Alerts are stored in a SQLite database using SQLAlchemy. The application also logs alerts to a file and provides error handling for various HTTP status codes.

## Installation

1. Clone the repository.
2. Build the Docker container using `docker-compose up --build`.
3. Access the application at `http://localhost:8080`.

# Local Set-up

## Setting up a Python Virtual Environment (venv)

A Python virtual environment (venv) allows you to isolate Python environments for different projects, preventing dependency conflicts. Here's how to set it up:

### Prerequisites

Ensure Python 3.3+ is installed on your system.

### Create and Activate

1. **Create venv:**

   - Windows:

     ```bash
     python -m venv venv
     ```

   - macOS/Linux:
     ```bash
     python3 -m venv venv
     ```

2. **Activate venv:**

   - Windows:

     ```bash
     venv\Scripts\activate
     ```

   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

### Usage

While venv is active:

- pip install -r requirements.txt

Certainly! Here's the text formatted for a README file:

### Setting `FLASK_APP` Environment Variable

#### Linux/Mac:

```bash
export FLASK_APP=cloud-alert.py
```

#### Windows (Command Prompt):

```bash
set FLASK_APP=cloud-alert.py
```

#### Windows (PowerShell):

```bash
$env:FLASK_APP = "cloud-alert.py"
```

### Deactivate

To exit venv:

```bash
deactivate
```

### Delete venv

If needed, delete the `venv` directory after deactivating.

## Usage

To use the application, you can interact with the following endpoints:

- `POST /alerts`: Create a new alert by providing JSON data with severity, host, details, is_alarm, and optional status.
- `POST /clear-alert`: Clear an alert by providing JSON data with severity, host, details, is_alarm, and status as 'cleared'.
- `GET /alerts`: Get a list of alerts with optional query parameters for filtering by severity and host.
- `PUT /alerts/<alert_id>`: Update an existing alert by providing JSON data with new values.
- `DELETE /alerts/<alert_id>`: Delete an alert by its ID.

## Configuration

Ensure the following environment variables are set:

- `FLASK_ENV`: Set to 'development' for Flask environment mode.
- `SQLALCHEMY_DATABASE_URI`: Connection URI for the PostgreSQL database.

## License

Feel free to customize this template to suit your project's specific needs.
