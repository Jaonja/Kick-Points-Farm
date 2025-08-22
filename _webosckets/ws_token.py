from curl_cffi import requests

class KickPoints:
    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers = {
            "accept": "application/json",
            "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": f"Bearer {token}",
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

            # without that im getting "Request blocked by security policy."
            'x-client-token': 'e1393935a959b4020a4491574f6490129f678acdaa92760471263db43487f823',
        }
    
    def get_ws_token(self) -> str:
        response = self.session.get("https://websockets.kick.com/viewer/v1/token")
        # {'data': {'token': '01K37ET4T6SRF85R6DD6XNFJGK'}, 'message': 'OK'}
        return response.json()['data']['token']