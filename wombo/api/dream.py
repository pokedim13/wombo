import asyncio
import time

from httpx import AsyncClient, Client, Response

from wombo.base import BaseDream
from wombo.models import ArtStyleModel, TaskModel


class Dream(BaseDream):
    class Style(BaseDream.Style["Dream"]):
        @property
        def url(self) -> str:
            response = self.dream._client.get(url=self.dream.base_url)
            return self.regex(response)
        
        def get_styles(self) -> ArtStyleModel:
            response: Response = self.dream._client.get(self.url)
            response = response.json().get("pageProps").get("artStyles")
            return self.dream._get_model(ArtStyleModel, response)

    class Auth(BaseDream.Auth["Dream"]):
        def _get_js_filename(self) -> str:
            response = self.dream._client.get(self.urls.get("js_filename"))
            js_filename = self._regex_js_filename(response)
            return js_filename[0]
        
        def _get_google_key(self) -> str:
            js_filename = self._get_js_filename()
            url = self.urls.get("google_key").format(js_filename=js_filename)
            response = self.dream._client.get(url)
            key = self._regex_google_key(response)
            return key[0]
        
        def _get_auth_key(self) -> str:
            if self.dream.token is not None:
                return self.dream.token
            response = self.dream._client.post(
                self.urls.get("auth_key"),
                params={"key": self._get_google_key()},
                json={"returnSecureToken": True},
            )
            result = response.json()
            self.dream.token = result.get("idToken")
            return self.dream.token

    class API(BaseDream.API["Dream"]):
        def create_task(self, text: str, 
                        style: int = 115, 
                        ratio: str = "old_vertical_ratio", 
                        premium: bool = False, 
                        display_freq: int = 10) -> TaskModel:
            response = self.dream._client.post(
                self.url,
                headers=self.dream._headers_gen(self.dream.auth._get_auth_key()),
                json=self._data_gen(text, style, ratio, premium, display_freq),
            )
            response = response.json()
            model: TaskModel = self.dream._get_model(TaskModel, response)
            return model
        
        def check_task(self, task_id: str) -> TaskModel:
            response = self.dream._client.get(f"{self.url}/{task_id}")
            response = response.json()
            model: TaskModel = self.dream._get_model(TaskModel, response)
            return model

        def tradingcard(self, task_id: str) -> str:
            response = self.dream._client.post(
                f"https://paint.api.wombo.ai/api/tradingcard/{task_id}",
                headers=self.dream._headers_gen(self.dream.auth._get_auth_key())
            )
            response = response.text
            return response

    class Profile(BaseDream.Profile["Dream"]):
        def gallery(self, 
                    task_id: str, is_public: bool = True, 
                    name: str = "", is_prompt_visible: str = True,
                    tags: list = None) -> Response:
            response = self.dream._client.post(
                f"{self.url}/gallery",
                headers=self.dream.api._headers_gen(self.dream.auth._get_auth_key()),
                json={
                    "task_id": task_id,
                    "is_public": is_public,
                    "name": name,
                    "is_prompt_visible": is_prompt_visible,
                    "tags": tags
                }
            )
            response = response.json()
            return response
        
        def delete(self, id_list: list) -> Response:
            response = self.dream._client.post(
                f"{self.url}/gallery/multi-delete",
                headers=self.dream.api._headers_gen(self.dream.auth._get_auth_key()),
                json={
                    "id_list": id_list
                }
            )
            return response

        def edit(self, profile_bio: str = "", website_link: str = "") -> Response:
            response = self.dream._client.patch(
                f"{self.url}/users",
                headers=self.dream.api._headers_gen(self.dream.auth._get_auth_key()),
                json={
                    "profile_bio": profile_bio,
                    "website_link": website_link
                }
            )
            return response

    def __init__(self, token: str = None) -> None:
        super().__init__(token)
        self._client = Client(follow_redirects=True, timeout=20)

    def generate(self, text: str,
                 style: int = 115,
                 ratio: str = "old_vertical_ratio",
                 premium: bool = False, 
                 display_freq: int = 10,
                 timeout: int = 60,
                 check_for: int = 3) -> TaskModel:
        task = self.api.create_task(text=text, style=style, 
                                    ratio=ratio, premium=premium, display_freq=display_freq)
        for _ in range(timeout, 0, -check_for):
            task = self.api.check_task(task.id)
            if task.result is not None:
                return task
            time.sleep(check_for)
        else:
            raise TimeoutError("Generate timeout")


class AsyncDream(BaseDream):
    class Style(BaseDream.Style["Dream"]):
        @property
        async def url(self) -> str:
            response = await self.dream._client.get(url=self.dream.base_url)
            return self.regex(response)
        
        async def get_styles(self) -> ArtStyleModel:
            response: Response = await self.dream._client.get(await self.url)
            response = response.json().get("pageProps").get("artStyles")
            return self.dream._get_model(ArtStyleModel, response)

    class Auth(BaseDream.Auth["Dream"]):
        async def _get_js_filename(self) -> str:
            response = await self.dream._client.get(self.urls.get("js_filename"))
            js_filename = self._regex_js_filename(response)
            return js_filename[0]
        
        async def _get_google_key(self) -> str:
            js_filename = await self._get_js_filename()
            url = self.urls.get("google_key").format(js_filename=js_filename)
            response = await self.dream._client.get(url)
            key = self._regex_google_key(response)
            return key[0]
        
        async def _get_auth_key(self) -> str:
            if self.dream.token is not None:
                return self.dream.token
            response = await self.dream._client.post(
                self.urls.get("auth_key"),
                params={"key": await self._get_google_key()},
                json={"returnSecureToken": True},
            )
            result = response.json()
            self.dream.token = result.get("idToken")
            return self.dream.token

    class API(BaseDream.API["Dream"]):
        async def create_task(self, text: str, 
                        style: int = 115, 
                        ratio: str = "old_vertical_ratio", 
                        premium: bool = False, 
                        display_freq: int = 10) -> TaskModel:
            response = await self.dream._client.post(
                self.url,
                headers=self.dream._headers_gen(await self.dream.auth._get_auth_key()),
                json=self._data_gen(text, style, ratio, premium, display_freq),
            )
            response = response.json()
            model: TaskModel = self.dream._get_model(TaskModel, response)
            return model
        
        async def check_task(self, task_id: str) -> TaskModel:
            response = await self.dream._client.get(f"{self.url}/{task_id}")
            response = response.json()
            model: TaskModel = self.dream._get_model(TaskModel, response)
            return model

        async def tradingcard(self, task_id: str) -> str:
            response = await self.dream._client.post(
                f"https://paint.api.wombo.ai/api/tradingcard/{task_id}",
                headers=self.dream._headers_gen(await self.dream.auth._get_auth_key())
            )
            response = response.text
            return response

    class Profile(BaseDream.Profile["Dream"]):
        async def gallery(self, 
                    task_id: str, is_public: bool = True, 
                    name: str = "", is_prompt_visible: str = True,
                    tags: list = None) -> Response:
            response = await self.dream._client.post(
                f"{self.url}/gallery",
                headers=self.dream.api._headers_gen(await self.dream.auth._get_auth_key()),
                json={
                    "task_id": task_id,
                    "is_public": is_public,
                    "name": name,
                    "is_prompt_visible": is_prompt_visible,
                    "tags": tags
                }
            )
            response = response.json()
            return response
        
        async def delete(self, id_list: list) -> Response:
            response = await self.dream._client.post(
                f"{self.url}/gallery/multi-delete",
                headers=self.dream.api._headers_gen(await self.dream.auth._get_auth_key()),
                json={
                    "id_list": id_list
                }
            )
            return response

        async def edit(self, profile_bio: str = "", website_link: str = "") -> Response:
            response = await self.dream._client.patch(
                f"{self.url}/users",
                headers=self.dream.api._headers_gen(await self.dream.auth._get_auth_key()),
                json={
                    "profile_bio": profile_bio,
                    "website_link": website_link
                }
            )
            return response

    def __init__(self, token: str = None) -> None:
        super().__init__(token)
        self._client = AsyncClient(follow_redirects=True, timeout=20)

    async def generate(self, text: str,
                 style: int = 115,
                 ratio: str = "old_vertical_ratio",
                 premium: bool = False, 
                 display_freq: int = 10,
                 timeout: int = 60,
                 check_for: int = 3) -> TaskModel:
        task = await self.api.create_task(text=text, style=style, 
                                    ratio=ratio, premium=premium, display_freq=display_freq)
        for _ in range(timeout, 0, -check_for):
            task = await self.api.check_task(task.id)
            if task.result is not None:
                return task
            await asyncio.sleep(check_for)
        else:
            raise TimeoutError("Generate timeout")