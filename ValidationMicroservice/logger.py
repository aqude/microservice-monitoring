from datetime import datetime

from clickhouse_driver import Client

client = Client(host='localhost', port=9000)


class Logger:

    def __init__(self):
        self.client = client

    def new_event(self, service, event, text, error):
        try:
            date = datetime.now()
            data = {
                'timestamp': date,
                'service_name': service,
                'event': event,
                'text': text,
                'error': error
            }
            self.client.execute(
                'INSERT INTO logs_services (timestamp, service_name, event, text, error) VALUES',
                [data]
            )
        except Exception as e:
            print(f"Failed to log event: {e}")
