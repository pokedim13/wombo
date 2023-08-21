from abc import ABC, abstractmethod
from io import BytesIO
from typing import List, Union, TypeVar

from httpx._client import Client, AsyncClient

Image = TypeVar("Image")

from wombo.models.check_task import CheckTask
from wombo.models.create_task import CreateTask

class BaseDream(ABC):
    "Base model for sync and async dream"
    client: Union[Client, AsyncClient]
    _counter_calls_auth: int = 0
    _auth_token: str = ""


    @staticmethod
    def save_frames_as_gif(frames: List[Image], duration: int = 400) -> BytesIO:
        """
    Convert a list of frames to a GIF and return it as bytes for a writable stream.

    This static method takes a list of image frames and creates a GIF animation using the provided frames.
    The resulting GIF is returned as bytes in a BytesIO object that can be used for writing to a stream.

    Args:
        frames (List[Image]): A list of PIL.Image.Image frames to be used in the GIF.
        duration (int, optional): The duration in milliseconds for each frame. Defaults to 400 ms.

    Returns:
        BytesIO: A bytes stream containing the generated GIF.

    Example:
        image_frames = [...]  # List of PIL.Image.Image frames
        gif_stream = ClassName.save_frames_as_gif(image_frames)
        # Returns a bytes stream with the GIF animation.
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
    def generate(
            self,
            text: str,
            style: int,
            timeout: int,
            check_for: int,
            gif: bool
    ) -> BytesIO:
        pass