import re
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from httpx import Response

from wombo.models import ArtStyleModel, TaskModel

T = TypeVar("T", bound="BaseDream")
class BaseDream(ABC):
    class Style(ABC, Generic[T]):
        def __init__(self, dream: T) -> None:
            self.dream = dream

        @staticmethod
        def _regex(responce: Response) -> str:
            """The regex is needed to get a file containing all the styles."""
            regex = re.findall(r"/_next/static/([a-zA-Z0-9-]+)/_ssgManifest.js", responce.text)
            return f"https://dream.ai/_next/data/{regex[0]}/create.json"

        @property
        def _url(self) -> Response:
            """Getting a link to styles."""
            return self.dream._request("GET", url="/")

        @abstractmethod
        def get_styles(self) -> ArtStyleModel:
            """Function of getting styles."""

    class Auth(ABC, Generic[T]):
        urls = {
            "js_filename": "create",
            "google_key": "_next/static/chunks/pages/_app-{js_filename}.js",
            "auth_key": "https://identitytoolkit.googleapis.com/v1/accounts:signUp",
        }
        def __init__(self, dream: T) -> None:
            self.dream = dream

        @staticmethod
        def _regex_js_filename(response: Response) -> str:
            return re.findall(r"_app-(\w+)", response.text)

        @staticmethod
        def _regex_google_key(response: Response) -> str:
            key = re.findall(r'"(AI\w+)"', response.text)
            return key

        def _get_js_filename(self) -> Response:
            """Getting js file name. To receive an anonymous token."""
            return self.dream._request("GET", url=self.urls.get("js_filename"))

        def _get_google_key(self, url: str) -> Response:
            """Getting the google key from the name of the js file. To receive an anonymous token."""
            return self.dream._request("GET", url=url)

        @abstractmethod
        def _get_auth_key(self, new: bool = False) -> str:
            """Sending requests for an anonymous token. If a custom token was passed, it will be returned."""

        def new_auth_key(self) -> str:
            """Get new auth key."""
            return self._get_auth_key(new=True)
        
    class API(ABC, Generic[T]):
        _url = "https://paint.api.wombo.ai/api/v2/tasks"
        def __init__(self, dream: T) -> None:
            self.dream = dream

        @staticmethod
        def _data_gen(text: str, 
                      style: int, 
                      ratio: str, 
                      premium: bool, 
                      display_freq: int) -> dict:
            """Generate data for image creating."""
            return {
                "is_premium": premium,
                "input_spec": {
                    "aspect_ratio": ratio,
                    "prompt": text,
                    "style": style,
                    "display_freq": display_freq,
                },
            }

        def create_task(self, text: str, 
                        style: int = 115, 
                        ratio: str = "old_vertical_ratio", 
                        premium: bool = False, 
                        display_freq: int = 10) -> TaskModel:
            """Sending a photo generation task in the wombo servers."""
            return self.dream._request("POST", model=TaskModel,
                                       url=self._url,
                                       headers=self.dream._headers_gen(self.dream._token),
                                       json=self._data_gen(text, style, ratio, premium, display_freq))

        def check_task(self, task_id: str) -> TaskModel:
            """Checking readiness of task"""
            return self.dream._request("GET", 
                                       model=TaskModel,
                                       url=f"{self._url}/{task_id}",
                                       headers=self.dream._headers_gen(self.dream._token))

        def tradingcard(self, task_id: str) -> Response:
            """Generate original wombo image. Return url."""
            return self.dream._request("POST", 
                                       url=f"https://paint.api.wombo.ai/api/tradingcard/{task_id}",
                                       headers=self.dream._headers_gen(self.dream._token))
        
    class Profile(ABC, Generic[T]):
        """
        It was designed to work with a personalized profile, but this feature is not currently supported. 
        I am able to accept edits. All responses are in their original form.
        """

        prefix = "/api"
        def __init__(self, dream: T) -> None:
            self.dream = dream

        def gallery(self, 
                    task_id: str, is_public: bool = True, 
                    name: str = "", is_prompt_visible: str = True,
                    tags: list = None, limit: int = None) -> Response:
            """Save the image in your profile. You will need a profile token."""
            if limit is not None:
                return self.dream._request("GET",
                                           url=f"{self.dream._url}/{self.prefix}/gallery",
                                           headers=self.dream._headers_gen(self.dream._token),
                                           params={"limit": limit})
            return self.dream._request("POST",
                                       url=f"{self.dream._url}/{self.prefix}/gallery",
                                       headers=self.dream._headers_gen(self.dream._token),
                                       json={
                                            "task_id": task_id,
                                            "is_public": is_public,
                                            "name": name,
                                            "is_prompt_visible": is_prompt_visible,
                                            "tags": tags,
                                        })

        def delete(self, id_list: list) -> Response:
            """Deletes images from the user's profile."""
            return self.dream._request("POST",
                                       url=f"{self.dream._url}/{self.prefix}/gallery/multi-delete",
                                       headers=self.dream._headers_gen(self.dream._token),
                                       json={
                                            "id_list": id_list,
                                        })

        def edit(self, profile_bio: str = "", website_link: str = "") -> Response:
            """Edit dream (wombo) profile."""
            return self.dream._request("POST",
                                       url=f"{self.dream._url}/{self.prefix}/users",
                                       headers=self.dream._headers_gen(self.dream._token),
                                       json={
                                            "profile_bio": profile_bio,
                                            "website_link": website_link,
                                        })

    _url = "https://dream.ai/"
    def __init__(self, token: str = None):
        self.Style = self.Style(self)
        self.Auth = self.Auth(self)
        self.API = self.API(self)
        self.Profile = self.Profile(self)
        self._token = token

    @staticmethod
    def _headers_gen(auth_key: str) -> dict:
        return {
            "authorization": f"bearer {auth_key}",
            "x-app-version": "WEB-2.0.0",
        }
    
    @abstractmethod
    def _request[Model](self, method: str, model: Model = None, **kwargs) -> None:
        ...

    @abstractmethod
    def generate(self, text: str,
                 style: int = 115,
                 ratio: str = "old_vertical_ratio",
                 premium: bool = False, 
                 display_freq: int = 10,
                 timeout: int = 60,
                 check_for: int = 3) -> TaskModel:
        """Generate image."""