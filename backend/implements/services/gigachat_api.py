from typing import List
import requests
import uuid
import json
from datetime import datetime

from services.external_models_api import ExternalModelsAPIService


class GigaChatAPI(ExternalModelsAPIService):
    def __init__(self, authorization_key: str, certificate_path: str):
        super().__init__()
        self.authorization_key = authorization_key
        self.certificate_path = certificate_path
        self.access_token = None
        self.expires_at = None

    def update_access_token(self):
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        unique_id = str(uuid.uuid4())

        payload = {"scope": "GIGACHAT_API_PERS"}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": unique_id,
            "Authorization": f"Basic {self.authorization_key}",
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=self.certificate_path
        ).json()

        self.access_token = response["access_token"]
        self.expires_at = response["expires_at"]

    def check_expires_time(self) -> bool:
        if self.expires_at == None:
            return True

        timestamp_seconds = self.expires_at / 1000

        dt_given = datetime.fromtimestamp(timestamp_seconds)
        dt_now = datetime.now()

        if dt_now > dt_given:
            return True

        return False

    def get_model_list(self) -> List[str]:
        if self.check_expires_time():
            self.update_access_token()

        url = "https://gigachat.devices.sberbank.ru/api/v1/models"

        payload = {}
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        response = requests.request(
            "GET", url, headers=headers, data=payload, verify=self.certificate_path
        ).json()

        result = []

        for model in response["data"]:
            result.append(model["id"])

        return result

    def get_answer(self, query, system_prompt, documents) -> str:
        if self.check_expires_time():
            self.update_access_token()

        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        payload = json.dumps(
            {
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "system",
                        "content": f"{system_prompt}",
                    },
                    {
                        "role": "user",
                        "content": f"{query} + {documents}"
                    }
                ],
                "n": 1,
                "stream": False,
                "max_tokens": 512,
                "repetition_penalty": 1.0,
                "update_interval": 0,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=self.certificate_path
        ).json()

        return response
