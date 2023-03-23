import requests
import json
import jwt


class MSAPI:
    """
    A class for accessing certani Microsoft APIs
    """

    def __init__(self, token=None, email=None) -> None:
        """
        Initializes the MSAPI class

        Args:
            token (str): Microsoft Teams authentication token
            email (str): User's email
        """
        self.token = token
        self.email = email
        self.scope = self._get_email_scope() if email != None else None

    def _get_email_scope(self) -> str:
        """
        Retrieve the scope of an email address

        This is done by checking if the email that is to checked has the same domain as
        the email address inside the user's authenthication token (JWT)

        Return:
            str: Scope of the email address. Will be 'internal' or 'external'
        """
        try:
            decoded_jwt = jwt.decode(
                self.token,
                audience="https://api.spaces.skype.com",
                options={"verify_signature": False},
            )
        except jwt.exceptions.ExpiredSignatureError:
            return "JWT has expired"
        except jwt.exceptions.InvalidTokenError:
            return "Invalid JWT"

        jwt_email_domain = decoded_jwt["unique_name"].split("@")[1].lower()
        email_domain = self.email.split("@")[1].lower()

        if jwt_email_domain == email_domain:
            return "internal"
        else:
            return "external"

    def get_user_data(self) -> dict:
        """
        Retrieve information about a user who is present in Azure AD or Microsoft Office 365

        Returns:
            dict: JSON repsonse from the API response
        """
        TEAMS_API_URL = "https://teams.microsoft.com/api/mt/emea/beta/users"
        if self.scope == "external":
            headers = {
                "Host": "teams.microsoft.com",
                "Authorization": f"Bearer {self.token}",
                "X-Ms-Client-Version": "1418/1.0.0.1823021323",
            }

            r = requests.get(
                f"{TEAMS_API_URL}/{self.email}/externalsearchv3?includeTFLUsers=true",
                headers=headers,
            )
            data = r.json()

            try:
                return data[0]
            except IndexError:
                return {}

        else:
            headers = {
                "Host": "teams.microsoft.com",
                "Authorization": f"Bearer {self.token}",
                "Content-Length": str(len(self.email)),
            }

            r = requests.post(
                f"{TEAMS_API_URL}/searchV2?includeDLs=true&includeBots=true&enableGuest=true&source=allTrue&skypeTeamsInfo=true",
                headers=headers,
                data=self.email,
            )
            data = r.json()

            try:
                return data["value"][0]
            except IndexError:
                return {}

    def get_user_presence(self, mri: str) -> dict:
        """
        Retrieve the presence data of a user in Microsoft Teams

        Args:
            token (str): Microsoft Teams authentication token
            mri (str): Microsoft Teams user's MRI (Messaging Routing Identifier)

        Returns:
            dict: JSON data conaining the user's availability and device type
        """
        payload = json.dumps([{"mri": f"{mri}"}])

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        r = requests.post(
            "https://presence.teams.microsoft.com/v1/presence/getpresence/",
            headers=headers,
            data=payload,
        )
        
        data = r.json()[0]
        
        presence_data = {
            "availability": data.get("presence").get("availability"),
            "devicieType": data.get("presence").get("deviceType")
        }
        
        return presence_data

    def get_tenant_info(self, identifier: str) -> dict:
        """
        Retrieve information about a Azure AD tenant

        Args:
            identifier (str): Tenant domain (example.com) or an email address (user@example.com)

        Returns:
            dict: JSON repsonse from the API endpoint
        """
        try:
            r = requests.get(f"https://login.microsoftonline.com/getuserrealm.srf?login={identifier}")
            return r.json()

        except requests.exceptions.RequestException:
            return {}
