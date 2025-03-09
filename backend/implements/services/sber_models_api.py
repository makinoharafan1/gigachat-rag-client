from typing import List
import requests
import uuid
from datetime import datetime

from services.external_models_api import ExternalModelsAPIService


class SberModelsAPI(ExternalModelsAPIService):
    
    def __init__(self, authorization_key: str, certificate_path: str):
        super().__init__()
        self.authorization_key = authorization_key
        self.certificate_path = certificate_path
        self.access_token = None
        self.expires_at = None

    
    def update_access_token(self):
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        payload={
            'scope': 'GIGACHAT_API_PERS'
        }

        unique_id = str(uuid.uuid4())
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': unique_id,
            'Authorization': f'Basic {self.authorization_key}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=self.certificate_path).json()

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

        if self.check_expires_time() :
            self.update_access_token()


        url = "https://gigachat.devices.sberbank.ru/api/v1/models"

        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=self.certificate_path).json()
        
        result = []

        for model in response["data"]:
            result.append(model["id"])
        
        return result