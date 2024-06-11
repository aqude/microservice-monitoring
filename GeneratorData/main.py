import requests
import random
from faker import Faker
from multiprocessing import Process

fake = Faker(locale="ru_RU")

SERVICE_LINK = "http://127.0.0.1:8000/"


def generate_valid_data():
    return {
        "timestamp": fake.iso8601(),
        "full_name": fake.name(),
        "user_id": str(fake.random_number(digits=6, fix_len=True)),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "address": fake.address(),
        "date_of_birth": fake.date_of_birth().isoformat(),
        "gender": random.choice(["мужчина", "женщина"]),
        "event_type": random.choice(["login", "logout", "purchase"]),
        "event_description": fake.sentence(),
        "text": fake.text()
    }


def send_data():
    data = generate_valid_data()
    print(f"Data: {data}")
    try:
        response = requests.post(SERVICE_LINK, json=data)
        print(f"Response: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    processes = []
    # send_data()

    while True:
        # for _ in range(10):
        #     p = Process(target=send_data)
        #     p.start()
        #     processes.append(p)
        #
        # for p in processes:
        #     p.join()

        send_data()