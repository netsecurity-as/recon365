#!/usr/bin/python3
#
# by Siddharth Dushantha 2023
#
import requests
import json
import jwt
import sys
import argparse


def get_user_data(token: str, email: str, scope: str):
    TEAMS_API_URL = "https://teams.microsoft.com/api/mt/emea/beta/users"
    if scope == "external":
        headers = {
            "Host": "teams.microsoft.com",
            "Authorization": f"Bearer {token}",
            "X-Ms-Client-Version": "1418/1.0.0.1823021323",
        }

        r = requests.get(
            f"{TEAMS_API_URL}/{email}/externalsearchv3?includeTFLUsers=true",
            headers=headers,
        )
        data = r.json()

        try:
            return data[0], data
        except IndexError:
            return None, data

    else:
        headers = {
            "Host": "teams.microsoft.com",
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(email)),
        }

        r = requests.post(
            f"{TEAMS_API_URL}/searchV2?includeDLs=true&includeBots=true&enableGuest=true&source=allTrue&skypeTeamsInfo=true",
            headers=headers,
            data=email,
        )
        data = r.json()

        try:
            return data["value"][0], data
        except IndexError:
            return None, data


def get_status(token: str, mri: str) -> tuple[str, str, any]:
    payload = json.dumps([{"mri": f"{mri}"}])

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    r = requests.post(
        "https://presence.teams.microsoft.com/v1/presence/getpresence/",
        headers=headers,
        data=payload,
    )
    data = r.json()
    availability = data[0]["presence"]["availability"]
    device_type = data[0]["presence"]["deviceType"]

    return device_type, availability, data


def get_scope(token: str, email: str) -> str:
    try:
        decoded_jwt = jwt.decode(
            token,
            audience="https://api.spaces.skype.com",
            options={"verify_signature": False},
        )
    except jwt.ExpiredSignatureError:
        return "JWT has expired"
    except jwt.InvalidTokenError:
        return "Invalid JWT"

    jwt_email = decoded_jwt["unique_name"].lower()
    jwt_email_domain = jwt_email.split("@")[1].lower()
    email_domain = email.split("@")[1].lower()

    if jwt_email_domain == email_domain:
        return "internal"
    else:
        return "external"


def print_raw_data(raw_data):
    try:
        json_str = json.dumps(raw_data, indent=4, sort_keys=True)
        print(json_str, end="\n\n")
    except TypeError:
        print(raw_data, end="\n\n")


def main():
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument(
        "--token",
        "-t",
        metavar="PATH",
        required=True,
        help="Path to file containing your Microsoft Teams JWT token",
    )

    parser.add_argument(
        "--email",
        "-e",
        metavar="EMAIL",
        required=True,
        help="Email address you'd like to fetch information for",
    )

    parser.add_argument(
        "--raw",
        "-r",
        action="store_true",
        default=False,
        help="Output raw data fetched from MS Teams API (it contains more info)",
    )

    args = parser.parse_args()

    jwt_file = args.token
    email = args.email
    raw = args.raw

    try:
        with open(jwt_file) as f:
            token = f.read().strip()
    except FileNotFoundError:
        print(f"ERROR: {jwt_file} could not be found")
        sys.exit()

    scope = get_scope(token, email)
    if scope not in ["external", "internal"]:
        print(f"ERROR: {scope}")
        sys.exit()

    data, raw_data = get_user_data(token, email, scope)

    if raw:
        print("== USER DATA JSON DUMP ==")
        print_raw_data(raw_data)
        if not "external":
            sys.exit()

    try:
        full_name = data["displayName"]
        email = data["email"]
        user_type = data["type"]
    except TypeError:
        print(f"ERROR: The user '{email}' couldn't be found")
        sys.exit(1)

    if "skype" in str(data):
        skype_id = data["skypeId"]
        print(
            f"{'Full Name': <15} {full_name}\n"
            f"{'Email Address': <15} {email}\n"
            f"{'Skype ID': <15} {skype_id}\n"
            f"{'User Type': <15} {user_type}\n"
        )
    else:
        object_id = data["objectId"]
        tenant_name = data.get("tenantName") or data.get("companyName")

        if scope == "external":
            tenant_id = data["tenantId"]
            mri = data["mri"]
            device_type, availability, raw_data = get_status(token, mri)
            if raw:
                print("== USER PRESENCE DATA ==")
                print_raw_data(raw_data)
                sys.exit()

            print(
                f"{'Full Name': <18} {full_name}\n"
                f"{'Email Address': <18} {email}\n"
                f"{'Tenant Name': <18} {tenant_name}\n"
                f"{'User Type': <18} {user_type}\n"
                f"{'Object ID': <18} {object_id}\n"
                f"{'Tenant ID': <18} {tenant_id}\n"
                f"{'Availability': <18} {availability}\n"
                f"{'Device Type': <18} {device_type}\n"
            )
        else:
            print(
                f"{'Full Name': <18} {full_name}\n"
                f"{'Email Address': <18} {email}\n"
                f"{'Tenant Name': <18} {tenant_name}\n"
                f"{'User Type': <18} {user_type}\n"
                f"{'Object ID': <18} {object_id}\n"
            )


if __name__ == "__main__":
    main()
