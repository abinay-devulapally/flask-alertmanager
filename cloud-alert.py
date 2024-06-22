from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tabulate import tabulate
import uuid
import logging
# Importing from logging directly
from logging import FileHandler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alerts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure logging to file
log_handler = FileHandler('flask-alert.log')
log_handler.setLevel(logging.DEBUG)
log_format = '%(asctime)s - %(levelname)s - %(message)s'
log_handler.setFormatter(logging.Formatter(log_format))
app.logger.addHandler(log_handler)

# SQLAlchemy logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class Alert(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    time_raised = db.Column(db.DateTime, default=datetime.utcnow)
    severity = db.Column(db.String(50), nullable=False)
    host = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(200), nullable=False)
    is_alarm = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String(50), default='active')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@app.errorhandler(409)
def conflict(error):
    return jsonify({'error': 'Conflict', 'message': str(error)}), 409

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

@app.route('/alerts', methods=['POST'])
def create_alert():
    try:
        data = request.get_json()
        alert = Alert(
            severity=data['severity'],
            host=data['host'],
            details=data['details'],
            is_alarm=data['is_alarm'],
            status=data.get('status', 'active')
        )
        existing_alert = Alert.query.filter_by(
            severity=alert.severity,
            host=alert.host,
            details=alert.details,
            is_alarm=alert.is_alarm,
            status=alert.status
        ).first()
        if existing_alert:
            return jsonify({'message': 'Duplicate alert not added'}), 409

        db.session.add(alert)
        db.session.commit()

        if alert.status == 'cleared':
            app.logger.debug(f"Alert created with status 'cleared': {alert}")
            db.session.delete(alert)
            db.session.commit()
            app.logger.debug(f"Alert deleted with ID {alert.id}")
            return jsonify({'message': 'Alert cleared immediately after creation'}), 200

        return jsonify({
            'id': alert.id,
            'time_raised': alert.time_raised.isoformat(),
            'severity': alert.severity,
            'host': alert.host,
            'details': alert.details,
            'is_alarm': alert.is_alarm,
            'status': alert.status
        }), 201
    except KeyError as e:
        return jsonify({'error': 'Bad request', 'message': f'Missing required field: {e}'}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating alert: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.route('/clear-alert', methods=['POST'])
def clear_alert():
    try:
        data = request.get_json()
        
        # Validate input data
        if not all(k in data for k in ('severity', 'host', 'details', 'is_alarm', 'status')):
            return jsonify({'message': 'Missing required fields'}), 400
        
        alert = Alert(
            severity=data['severity'],
            host=data['host'],
            details=data['details'],
            is_alarm=data['is_alarm'],
            status=data['status']
        )

        # Check if status is 'cleared'
        if alert.status == 'cleared':
            # Check for existing active alert
            existing_alert = Alert.query.filter_by(
                severity=alert.severity,
                host=alert.host,
                details=alert.details,
                is_alarm=alert.is_alarm,
                status='active'
            ).first()

            if existing_alert:
                app.logger.debug(f"Deleting active alert with ID {existing_alert.id}")
                db.session.delete(existing_alert)
                db.session.commit()
                return jsonify({'message': 'Alert cleared and deleted from active list'}), 200
            else:
                app.logger.debug(f"No active alert found to clear for: {alert}")
                return jsonify({'message': 'No matching active alert found to clear'}), 404

        return jsonify({
            'id': alert.id,
            'time_raised': alert.time_raised.isoformat(),
            'severity': alert.severity,
            'host': alert.host,
            'details': alert.details,
            'is_alarm': alert.is_alarm,
            'status': alert.status
        }), 201
    except KeyError as e:
        return jsonify({'error': 'Bad request', 'message': f'Missing required field: {e}'}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error clearing alert: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.route('/alerts', methods=['GET'])
def get_alerts():
    try:
        severity = request.args.get('severity')
        host = request.args.get('host')
        query = Alert.query
        if severity:
            query = query.filter_by(severity=severity)
        if host:
            query = query.filter_by(host=host)
        alerts = query.all()
        return jsonify([{
            'id': alert.id,
            'time_raised': alert.time_raised.isoformat(),
            'severity': alert.severity,
            'host': alert.host,
            'details': alert.details,
            'is_alarm': alert.is_alarm,
            'status': alert.status
        } for alert in alerts])
    except Exception as e:
        app.logger.error(f"Error fetching alerts: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.route('/alerts/<int:alert_id>', methods=['PUT'])
def update_alert(alert_id):
    try:
        data = request.get_json()
        alert = Alert.query.get_or_404(alert_id)
        alert.severity = data['severity']
        alert.host = data['host']
        alert.details = data['details']
        alert.is_alarm = data['is_alarm']
        db.session.commit()
        return jsonify({'message': 'Alert updated'}), 200
    except KeyError as e:
        return jsonify({'error': 'Bad request', 'message': f'Missing required field: {e}'}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating alert: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.route('/alerts/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    try:
        alert = Alert.query.get(alert_id)
        if alert:
            app.logger.debug(f"Deleting alert with ID {alert_id}")
            db.session.delete(alert)
            db.session.commit()
            return jsonify({'message': 'Alert deleted'}), 200
        else:
            app.logger.debug(f"Alert with ID {alert_id} not found")
            return jsonify({'message': 'Alert not found'}), 404
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting alert: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.cli.command("list-alerts")
def list_alerts():
    """List all alerts."""
    try:
        alerts = Alert.query.all()
        headers = ['ID', 'Time Raised', 'Severity', 'Host', 'Details', 'Is Alarm', 'Status']
        table = [(
            alert.id,
            alert.time_raised,
            alert.severity,
            alert.host,
            alert.details,
            alert.is_alarm,
            alert.status
        ) for alert in alerts]
        print(tabulate(table, headers=headers, tablefmt='grid'))
    except Exception as e:
        app.logger.error(f"Error listing alerts: {str(e)}")
        print(f'Error: {str(e)}')

@app.cli.command("list-alarms")
def list_alarms():
    """List only alarms."""
    try:
        alarms = Alert.query.filter_by(is_alarm=True).all()
        headers = ['ID', 'Time Raised', 'Severity', 'Host', 'Details', 'Is Alarm', 'Status']
        table = [(
            alarm.id,
            alarm.time_raised,
            alarm.severity,
            alarm.host,
            alarm.details,
            alarm.is_alarm,
            alarm.status
        ) for alarm in alarms]
        print(tabulate(table, headers=headers, tablefmt='grid'))
    except Exception as e:
        app.logger.error(f"Error listing alarms: {str(e)}")
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8080)
