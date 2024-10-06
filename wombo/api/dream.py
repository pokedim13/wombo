import re
from time import sleep

from httpx import Client

from wombo.base import BaseDream
from wombo.models import StyleModel, TaskModel


class Dream(BaseDream):
    class Style(BaseDream.Style):
        @property
        def url(self) -> str:
            response = self.dream._client.get("https://dream.ai/")
            regex = re.findall(r"/_next/static/([a-zA-Z0-9-]+)/_ssgManifest.js", response.text)
            return f"https://dream.ai/_next/data/{regex[0]}/create.json"
        
        def _get_styles(self) -> StyleModel:
            response = self.dream._client.get(self.url).json().get("pageProps").get("artStyles")
            styles: StyleModel = self.dream._get_model(StyleModel, response)
            self._save_styles(styles)
            return styles

    class Auth(BaseDream.Auth):
        def _get_js_filename(self) -> str:
            response = self.dream._client.get(self.urls.get("js_filename"))
            js_filename = re.findall(r"_app-(\w+)", response.text)
            return js_filename[0]
        def _get_google_key(self) -> str:
            js_filename = self._get_js_filename()
            url = self.urls.get("google_key").format(js_filename=js_filename)
            response = self.dream._client.get(url)
            key = re.findall(r'"(AI\w+)"', response.text)
            return key[0]  
        def _get_auth_key(self) -> str:
            response = self.dream._client.post(
            self.urls.get("auth_key"),
                params={"key": self._get_google_key()},
                json={"returnSecureToken": True},
                timeout=20,
            )
            result = response.json()
            _auth_token = result.get("idToken")
            return _auth_token
        
    class API(BaseDream.API):
        def create_task(self, text: str, style: int = 115) -> TaskModel:
            response = self.dream._client.post(
                url=self.url,
                headers=self._headers_gen(self.dream.auth._get_auth_key()),
                json=self._data_gen(text=text, style=style),
                timeout=20
            ).json()
            model: TaskModel = self.dream._get_model(TaskModel, response)
            return model

        def check_task(self, task_id: str) -> TaskModel:
            response = self.dream._client.get(self.url+f"/{task_id}", timeout=10).json()
            model: TaskModel = self.dream._get_model(TaskModel, response)
            return model

    def __init__(self):
        super().__init__()
        self._client = Client()   

    def generate(self, text: str, style: int = 115, timeout: int = 60, check_for: int = 3) -> TaskModel:
        task = self.api.create_task(text=text, style=style)
        for _ in range(timeout, 0, -check_for):
            check_task = self.api.check_task(task.id)
            if check_task.result is not None:
                return check_task
            sleep(check_for)
        else:
            raise TimeoutError