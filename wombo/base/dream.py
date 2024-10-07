from abc import ABC, abstractmethod, abstractproperty
from typing import Union

from httpx._client import AsyncClient, Client
from pydantic import BaseModel

from wombo.models import StyleModel, TaskModel, pydantic_version


class BaseDream(ABC):
    "BaseDream Class"
    _client: Union[Client, AsyncClient]
    class Style(ABC):
        def __init__(self, dream: "BaseDream") -> None:
            self.dream = dream
            self.styles = None

        def __getitem__(self, key):
            for style in self.styles.root:
                if key == style.name:
                    return style.id 
            return None

        @property
        def free(self) -> StyleModel:
            res = []
            for style in self.styles.root:
                if style.is_premium:
                    continue
                res.append(style)
            return self.dream._get_model(StyleModel, res)
        
        @property
        def premium(self) -> StyleModel:
            res = []
            for style in self.styles.root:
                if not style.is_premium:
                    continue
                res.append(style)
            return self.dream._get_model(StyleModel, res)
            

        @abstractproperty
        def url(self) -> str:
            """Returns the URL associated with this styles.

            This abstract method must be overridden in child classes to provide a specific URL that matches the style type.

            Returns:
                str: The URL of the styles.
            """

        @abstractmethod
        def _get_styles(self)-> StyleModel:
            """Retrieves the style model for the current object.

            This abstract method must be redefined in subclasses for 
            getting up-to-date information about styles. The returned style model
            It can contain various attributes such as colors, fonts, etc.

            Returns:
                StyleModel: A style model containing information about styles.
            """

        def _save_styles(self, styles: StyleModel):
            self.styles = styles

    class Auth(ABC):
        urls = {
            "js_filename": "https://dream.ai/create",
            "google_key": "https://dream.ai/_next/static/chunks/pages/_app-{js_filename}.js",
            "auth_key": "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        }
        def __init__(self, dream: "BaseDream") -> None:
            self.dream = dream

        @abstractmethod
        def _get_js_filename(self) -> str:
            """Getting a js file with authorization data
            
            Returns:
                str: file_name.
            """

        @abstractmethod
        def _get_google_key(self) -> str:
            """Getting a token to send to google and receive an authorization token
            
            Returns:
                str: google token.
            """

        @abstractmethod
        def _get_auth_key(self) -> str:
            """Getting a authorization token
            
            Returns:
                str: authorization token.
            """

    class API(ABC):
        url = "https://paint.api.wombo.ai/api/v2/tasks"

        def __init__(self, dream: "BaseDream"):
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
        
        @abstractmethod
        def create_task(self, text: str, style: int)-> TaskModel:
            """Creating a generative image creation task
            
            Returns:
                TaskModel: Task attrs."""

        @abstractmethod
        def check_task(self, task_id: str) -> TaskModel:
            """Creating a generative image creation task
            
            Returns:
                TaskModel: Task attrs."""
        
    def __init__(self, token: str = None, debug: bool = False) -> None:
        self.style = self.Style(self)
        self.auth = self.Auth(self)
        self.api = self.API(self)
        self.token = token
        self.debug = debug

    def _get_model(self, model: BaseModel, data: any) -> BaseModel:
        if pydantic_version.split(".")[0] == "1":
            return model.parse_obj(data)
        if pydantic_version.split(".")[0] == "2":
            return model.model_validate(data)
        raise ValueError

    @abstractmethod
    def generate(self, text: str, style: int, timeout: int, check_for: int) -> TaskModel:
        """generate picture
        
        Returns:
            TaskModel: Task attrs."""

