
import os
import csv
import requests

from dotenv import load_dotenv

load_dotenv()

OKTA_DOMAIN = os.environ["OKTA_DOMAIN"].rstrip("/")
OKTA_TOKEN = os.environ["OKTA_API_TOKEN"]

session = requests.Session()

session.headers.update({
    "Authorization": f"SSWS {OKTA_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
})


def get_all_users():
    users = []
    url = f"{OKTA_DOMAIN}/api/v1/users?limit=200"

    while url:
        response = session.get(url, timeout=30)
        response.raise_for_status()

        users.extend(response.json())

        # Okta provides pagination through the Link header.
        url = response.links.get("next", {}).get("url")

    return users


def export_users_to_csv(users):
    with open(
        "okta_users.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "User ID",
            "First Name",
            "Last Name",
            "Email",
            "Status"
        ])

        for user in users:
            profile = user.get("profile", {})

            writer.writerow([
                user.get("id"),
                profile.get("firstName"),
                profile.get("lastName"),
                profile.get("email"),
                user.get("status")
            ])


if __name__ == "__main__":
    users = get_all_users()

    export_users_to_csv(users)

    print(f"Successfully exported {len(users)} users.")
