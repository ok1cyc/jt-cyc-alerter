import requests

class Alerter:
    def __init__(self, url, topic, silence_period):
        """
        Initialize the Alerter with a target URL, topic for notifications, and silence period.
        
        :param url: The base URL of the notification service (e.g., "https://ntfy.ok1cyc.net:8031")
        :param topic: The topic to post alerts to (e.g., "ham")
        :param silence_period: The number of minutes to increase the timestamp after sending an alert
        """
        self.url = url
        self.topic = topic
        self.silence_period = silence_period

    def shoot_alert(self, callsign, alert_list_maintainer):
        """
        Send an alert for the specified callsign.
        
        :param callsign: The callsign to alert on.
        :param alert_list_maintainer: An instance of AlertListMaintainer to get alert data.
        """
        # Retrieve alert data for the callsign
        alert_data = alert_list_maintainer.get_data(callsign)
        
        # If there's alert data, proceed to send the alert
        if alert_data:
            message = alert_data[0]  # Assuming the message is stored as the first element in alert_data

            # Construct the full URL for the POST request
            target_url = f"{self.url}/{self.topic}"
            
            # Send the POST request with the message as data
            response = requests.post(target_url, data=message.encode('utf-8'))
            
            # Print the response status for confirmation or debugging
            if response.status_code == 200:
                print(f"Alert sent successfully for callsign '{callsign}' with message: '{message}'")
                # Increase the timestamp for the alerted callsign by silence period
                alert_list_maintainer.increase_timestamp(callsign, self.silence_period)
            else:
                print(f"Failed to send alert for callsign '{callsign}'. Status code: {response.status_code}")
