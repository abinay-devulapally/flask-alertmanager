import requests
import random
import string
import json

# Adjust the URL according to your Flask application's host and port
url = 'http://localhost:8080/alerts'

# Function to generate random dummy alerts
def generate_dummy_alert():
    severity = random.choice(['low', 'medium', 'high'])
    host = 'host-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    details = 'Details about alert ' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    is_alarm = random.choice([True, False])
    status = 'active'  # Change status to 'cleared' to test clearing logic

    alert = {
        'severity': severity,
        'host': host,
        'details': details,
        'is_alarm': is_alarm,
        'status': status
    }
    return alert

# Number of dummy alerts to create
num_alerts = 5

# Create and send random dummy alerts
for _ in range(num_alerts):
    alert_data = generate_dummy_alert()
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(alert_data))
        if response.status_code == 201:
            print(f"Created alert: {alert_data}")
        else:
            print(f"Failed to create alert: {alert_data} - Status code: {response.status_code}")
            print(f"Response content: {response.content}")
    except requests.exceptions.RequestException as e:
        print(f"Error creating alert: {alert_data} - {e}")
