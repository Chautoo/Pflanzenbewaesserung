# API request 'POST' 'GET'

import urllib.request
import json
import base64

from dotenv import load_dotenv
from json.decoder import JSONDecodeError
import os


class LaravelAPIClient:
    def __init__(self, env_path="../.env"):
        load_dotenv(dotenv_path=env_path)

        self.user = os.getenv("API_USER")
        self.password = os.getenv("API_PASSWORD")
        self.base_url = os.getenv("API_URL")

        # if a variable is not available
        if not all([self.user, self.password, self.base_url]):
            raise ValueError("Missing environment variables in .env file")

        # Basic Auth Header
        credentials = f"{self.user}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

    # HTTP Reqeust for all methods
    def request(self, method, endpoint, data=None):
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        if data is not None:
            data = json.dumps(data).encode('utf-8')

        # crete HTTP request
        req = urllib.request.Request(
            url=url,
            data=data,
            headers=self.headers,
            method=method.upper()
        )

        # Execute request
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                raw = response.read().decode()
                try:
                    return json.loads(raw)
                except JSONDecodeError:
                    return {
                        "error": "invalid_json",
                        "message": "The API response could not be interpreted as JSON.",
                        "raw_response": raw
                    }

        # Error handling
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            return {
                "error": "http_error",
                "code": e.code,
                "reason": e.reason,
                "message": error_body
            }

        except urllib.error.URLError as e:
            return {
                "error": "network_error",
                "reason": str(e.reason)
            }

        except Exception as e:
            return {
                "error": "unexpected_exception",
                "message": str(e)
            }

    # Methoden
    def get(self, endpoint):
        return self.request("GET", endpoint)

    def post(self, endpoint, data):
        return self.request("POST", endpoint, data)

    def put(self, endpoint, data):
        return self.request("PUT", endpoint, data)

    def delete(self, endpoint):
        return self.request("DELETE", endpoint)
