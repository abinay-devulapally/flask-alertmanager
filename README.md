# Project Description

This project is a Flask application for managing cloud alerts. It includes functionality to create, clear, update, and delete alerts, as well as list all alerts or only alarms. Alerts are stored in a SQLite database using SQLAlchemy. The application also logs alerts to a file and provides error handling for various HTTP status codes.

## Installation

1. Clone the repository.
2. Build the Docker container using `docker-compose up --build`.
3. Access the application at `http://localhost:8080`.

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
