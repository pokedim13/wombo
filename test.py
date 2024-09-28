# styles
# GET https://dream.ai/_next/data/3cjhS-p1RUbbLXCBWDDJ7/create.json

# create task
# POST https://paint.api.wombo.ai/api/v2/tasks


import re
from httpx import Client

class Dream: 
    def __init__(self):
        self.client = Client()
        self.auth = Auth(self)
        self.style = Style(self)
        self.api = API(self)

    def generate(self, text: str, style: int, timeout: int = 60, check_for: int = 3):
        ...


class Auth:
    urls = {
        "js_filename": "https://dream.ai/create",
        "google_key": "https://dream.ai/_next/static/chunks/pages/_app-{js_filename}.js",
        "auth_key": "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
    }

    def __init__(self, dream: Dream):
        self.dream = dream

    def _get_js_filename(self) -> str:
        response = self.dream.client.get(self.urls.get("js_filename"))
        js_filename = re.findall(r"_app-(\w+)", response.text)
        return js_filename[0]
    
    def _get_google_key(self) -> str:
        js_filename = self._get_js_filename()
        url = self.urls.get("google_key").format(js_filename=js_filename)
        response = self.dream.client.get(url)
        key = re.findall(r'"(AI\w+)"', response.text)
        return key[0]
    
    def _get_auth_key(self) -> str:
        response = self.dream.client.post(
            self.urls.get("auth_key"),
            params={"key": self._get_google_key()},
            json={"returnSecureToken": True},
            timeout=20,
        )
        result = response.json()
        _auth_token = result.get("idToken")
        return _auth_token

class Style:
    def __init__(self, dream: Dream):
        self.dream = dream

    @property
    def url(self):
        response = self.dream.client.get('https://dream.ai/')
        regex = re.findall(r'/_next/static/([a-zA-Z0-9-]+)/_ssgManifest.js', response.text)
        return f"https://dream.ai/_next/data/{regex[0]}/create.json"

    def _get_styles(self):
        return self.dream.client.get(self.url).json()

class API:
    url = "https://paint.api.wombo.ai/api/v2/tasks"

    def __init__(self, dream: Dream):
        self.dream = dream

    def _headers_gen(self, auth_key: str):
        return {
            "authorization": f"bearer {auth_key}",
            "x-app-version": "WEB-2.0.0",
        }
    
    def _data_gen(self, text: str, style: int):
        return {
            "is_premium": False,
            "input_spec": {
                "aspect_ratio": "old_vertical_ratio",
                "prompt": text,
                "style": style,
                "display_freq": 10
            }
        }

    def create_task(self, text: str, style: int = 84):
        response = self.dream.client.post(
            url=self.url,
            headers=self._headers_gen(self.dream.auth._get_auth_key()),
            json=self._data_gen(text=text, style=style),
            timeout=20
        ).json()
        return response

    def check_task(self, task_id: str):
        response = self.dream.client.get(self.url+f"/{task_id}", timeout=10).json()
        return response

dream = Dream()
print(dream.style._get_styles())

