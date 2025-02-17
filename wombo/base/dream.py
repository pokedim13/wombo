import re
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from httpx import Response
from pydantic import __version__ as pydantic_version

from wombo.models import ArtStyleModel, TaskModel

T = TypeVar("T", bound="BaseDream")
class BaseDream(ABC):
    class Style(ABC, Generic[T]):
        """Styles url and functions for use styles."""
        def __init__(self, dream: T) -> None:
            self.dream = dream

        @staticmethod
        def regex(responce: Response) -> str:
            """The regex is needed to get a file containing all the styles."""
            regex = re.findall(r"/_next/static/([a-zA-Z0-9-]+)/_ssgManifest.js", responce.text)
            return f"https://dream.ai/_next/data/{regex[0]}/create.json"
        
        @property
        @abstractmethod
        def url(self) -> str:
            """Getting a link to styles."""

        @abstractmethod
        def get_styles(self) -> ArtStyleModel:
            """Function of getting styles."""

    class Auth(ABC, Generic[T]):
        """Auth system. Get dream api token for requests."""
        urls = {
            "js_filename": "https://dream.ai/create",
            "google_key": "https://dream.ai/_next/static/chunks/pages/_app-{js_filename}.js",
            "auth_key": "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
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

        @abstractmethod
        def _get_js_filename(self) -> str:
            """Getting js file name. To receive an anonymous token."""

        @abstractmethod
        def _get_google_key(self) -> str:
            """Getting the google key from the name of the js file. To receive an anonymous token."""

        @abstractmethod
        def _get_auth_key(self) -> str:
            """Sending requests for an anonymous token. If a custom token was passed, it will be returned."""

    class API(ABC, Generic[T]):
        """Base API for use."""
        url = "https://paint.api.wombo.ai/api/v2/tasks"

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
                    "display_freq": display_freq
                },
            }
        
        @abstractmethod
        def create_task(self, text: str, 
                        style: int = 115, 
                        ratio: str = "old_vertical_ratio", 
                        premium: bool = False, 
                        display_freq: int = 10) -> TaskModel:
            """Sending a photo generation task in the wombo servers."""

        @abstractmethod
        def check_task(self, task_id: str) -> TaskModel:
            """Checking readiness of task"""

        @abstractmethod
        def tradingcard(self, task_id: str) -> str:
            """Generate original wombo image. Return url."""

    class Profile(ABC, Generic[T]):
        """
        It was designed to work with a personalized profile, but this feature is not currently supported. 
        I am able to accept edits. All responses are in their original form.
        """

        def __init__(self, dream: T) -> None:
            self.dream = dream

        @abstractmethod
        def gallery(self, 
                    task_id: str, is_public: bool = True, 
                    name: str = "", is_prompt_visible: str = True,
                    tags: list = None) -> Response:
            """Save the image in your profile. You will need a profile token."""

        @abstractmethod
        def delete(self) -> Response:
            """Deletes images from the user's profile."""

        @abstractmethod
        def edit(self) -> Response:
            """Edit dream (wombo) profile."""
    
    base_url = "https://dream.ai/"
    def __init__(self, token: str = None):
        self.style = self.Style(self)
        self.auth = self.Auth(self)
        self.api = self.API(self)
        self.profile = self.Profile(self)
        self.token = token

    @staticmethod
    def _headers_gen(auth_key: str) -> dict:
        return {
            "authorization": f"bearer {auth_key}",
            "x-app-version": "WEB-2.0.0",
        }

    @staticmethod
    def _get_model[Model](model: Model, data: any) -> Model:
        if pydantic_version.split(".")[0] == "1":
            return model.parse_obj(data)
        if pydantic_version.split(".")[0] == "2":
            return model.model_validate(data)
        raise ValueError("Support pydantic version not found.")
    
    @abstractmethod
    def generate(self, text: str,
                 style: int = 115,
                 ratio: str = "old_vertical_ratio",
                 premium: bool = False, 
                 display_freq: int = 10,
                 timeout: int = 60,
                 check_for: int = 3) -> TaskModel:
        """Generate image."""