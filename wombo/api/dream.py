from wombo.base import BaseDream

import time, asyncio
from httpx import Response, Client, AsyncClient

from wombo.models import TaskModel, ArtStyleModel

class Dream(BaseDream):
    class Style(BaseDream.Style["Dream"]):
        def get_styles(self) -> ArtStyleModel:
            res = self.dream._request("GET", url=self._regex(self._url))
            return ArtStyleModel.model_validate(res.json().get("pageProps").get("artStyles"))

    class Auth(BaseDream.Auth["Dream"]):
        def _get_auth_key(self, new: bool = False):
            if self.dream._token is not None:
                if not new:
                    return self.dream._token
            
            res = self._get_js_filename()
            js_filename = self._regex_js_filename(res)

            url = self.urls.get("google_key").format(js_filename=js_filename[0])
            res = self._get_google_key(url)
            key = self._regex_google_key(res)
            
            res = self.dream._request("POST", 
                                      url=self.urls.get("auth_key"),
                                      params={"key": key},
                                      json={"returnSecureToken": True})
            res = res.json()
            self.dream._token = res.get("idToken")
            return self.dream._token
        
        def _new_auth_key(self):
            return self._get_auth_key(new=True)

    def __init__(self, token: str = None) -> None:
        super().__init__(token)
        self._client = Client(base_url=self._url, follow_redirects=True, timeout=20)

    def _request[Model](self, method: str, model: Model = None, **kwargs) -> Response | Model:
        res = self._client.request(method=method, **kwargs)
        if model is not None:
            return model.model_validate(res.json())
        return res
    
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
    class Style(BaseDream.Style["AsyncDream"]):
        async def get_styles(self) -> ArtStyleModel:
            res = await self.dream._request("GET", url=self._regex(await self._url))
            return ArtStyleModel.model_validate(res.json().get("pageProps").get("artStyles"))
        
    class Auth(BaseDream.Auth["AsyncDream"]):
        async def _get_auth_key(self, new: bool = False):
            if self.dream._token is not None:
                if not new:
                    return self.dream._token
            
            res = await self._get_js_filename()
            js_filename = self._regex_js_filename(res)

            url = self.urls.get("google_key").format(js_filename=js_filename[0])
            res = await self._get_google_key(url)
            key = self._regex_google_key(res)
            
            res = await self.dream._request("POST", 
                                      url=self.urls.get("auth_key"),
                                      params={"key": key},
                                      json={"returnSecureToken": True})
            res = res.json()
            self.dream._token = res.get("idToken")
            return self.dream._token

        def _new_auth_key(self):
            return self._get_auth_key(new=True)
        
    def __init__(self, token: str = None) -> None:
        super().__init__(token)
        self._client = AsyncClient(base_url=self._url, follow_redirects=True, timeout=20)

    async def _request[Model](self, method: str, model: Model = None, **kwargs) -> Response | Model:
        res = await self._client.request(method=method, **kwargs)
        if model is not None:
            return model.model_validate(res.json())
        return res
    
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