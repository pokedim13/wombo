from typing import List
from io import BytesIO

from PIL.Image import Image
from httpx._client import BaseClient


class BaseDream:
    """
    Base class for all dreams (sync / async).
    """

    client: BaseClient

    def save_frames_as_gif(self, frames: List[Image], duration: int = 400) -> BytesIO:
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
    
    def generate(self):
        raise NotImplementedError("Method not Implemented")
