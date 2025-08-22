from curl_cffi import requests

class KickUtility:
    def __init__(self, username: str):
        self.session = requests.Session()
        self.session.headers = {
            "accept": "application/json",
            "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "cluster": "v2",
            "origin": "https://kick.com",
            "priority": "u=1, i",
            "referer": "https://kick.com/",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        }
        self.username = username

    def get_stream_id(self) -> int:
        response = self.session.get(f"https://kick.com/api/v2/channels/{self.username}/videos")
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve stream ID for {self.username}: {response.text}")
        
        data = response.json()
        
        live_stream = next((stream for stream in data if stream['is_live'] == True), None)
        
        if not live_stream:
            return None
            
        return live_stream['id']
    
    def get_channel_id(self) -> int:
        response = self.session.get(f"https://kick.com/api/v2/channels/{self.username}/videos")
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve channel ID for {self.username}: {response.text}")
        
        return response.json()[0]['channel_id']