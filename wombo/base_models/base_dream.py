from io import BytesIO
from abc import ABC, abstractmethod
from typing import List, Union

from PIL.Image import Image
from httpx._client import Client, AsyncClient

from wombo.models import CheckTask, CreateTask


class BaseDream(ABC):
    """
    Base class for all dreams (sync / async).
    """

    client: Union[Client, AsyncClient]
    _counter_calls_auth: int = 0
    _auth_token: str = ''

    @staticmethod
    def save_frames_as_gif(frames: List[Image], duration: int = 400) -> BytesIO:
        """
        Saves a list of frames as a gif and returns as bytes IO for writing stream.
        """
        result = BytesIO()

        frames[0].save(
            fp=result,
            save_all=True,
            append_images=frames[1:],
            format="GIF",
            duration=duration,
            loop=1,
        )

        return result

    @abstractmethod
    def _get_js_filename(self) -> str:
        pass

    @abstractmethod
    def _get_google_key(self) -> str:
        pass

    @abstractmethod
    def _get_auth_key(self) -> str:
        pass

    @abstractmethod
    def create_task(self, text: str, style: int) -> CreateTask:
        pass

    @abstractmethod
    def check_task(self, task_id: str, only_bool: bool) -> Union[CheckTask, bool]:
        pass

    @abstractmethod
    def _generate_model_image(
            self,
            text: str,
            style: int,
            timeout: int,
            check_for: int
    ) -> CreateTask:
        pass

    @abstractmethod
    def generate_image(
            self,
            text: str,
            style: int,
            timeout: int,
            check_for: int
    ) -> BytesIO:
        pass

    @abstractmethod
    def generate_gif(
            self,
            text: str,
            style: int,
            timeout: int,
            check_for: int
    ) -> BytesIO:
        pass
