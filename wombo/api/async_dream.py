from typing import Union

import re
import io
import asyncio

from wombo.config import not_imported
from wombo.base_models import BaseDream, Style
from wombo.urls import urls, headers_gen, check_headers, auth_key_headers
from wombo.models.check_task import CheckTask
from wombo.models.create_task import CreateTask
from wombo.models.style import StyleModel

import httpx

if "pillow" in not_imported:
    pass
else:
    from PIL import Image


class AsyncDream(BaseDream):
    def __init__(self, max_requests_per_token: int = 30, out_msg = "") -> None:
        self.client = httpx.AsyncClient()
        self.max_requests_per_token = max_requests_per_token
        self.out_msg = out_msg

    async def _get_js_filename(self) -> str:
        """
    Get the name of the JavaScript file from which the Google Key is extracted.

    This method asynchronously retrieves the name of the JavaScript file that contains
    the Google API key. The extracted name is used to construct the URL for the JavaScript file.

    Returns:
        str: The name of the JavaScript file.

    Raises:
        IndexError: If the JavaScript filename extraction fails.

    Note:
        The 'client' attribute is expected to be defined elsewhere and represents an HTTP client for making requests.
        The 'urls' dictionary is expected to be defined elsewhere.
        The 're' module for regular expressions is assumed to be imported.

    Example:
        js_filename = await self._get_js_filename()
        # Returns the name of the JavaScript file containing the Google API key.
    """
        response = await self.client.get(urls["js_filename"])
        js_filename = re.findall(r"_app-(\w+)", response.text)
        return js_filename[0]

    async def _get_google_key(self) -> str:
        """
    Get the Google API key from the JavaScript file.

    This method asynchronously retrieves the Google API key from a JavaScript file
    associated with the application. It extracts the key from the fetched JavaScript content.

    Returns:
        str: The Google API key.

    Raises:
        IndexError: If the key extraction fails.

    Note:
        The 'client' attribute is expected to be defined elsewhere and represents an HTTP client for making requests.
        The '_get_js_filename' method is expected to be defined elsewhere.
        The 're' module for regular expressions is assumed to be imported.

    Example:
        google_key = await self._get_google_key()
        # Returns the Google API key.
    """
        js_filename = await self._get_js_filename()

        url = f"https://dream.ai/_next/static/chunks/pages/_app-{js_filename}.js"
        response = await self.client.get(url)

        key = re.findall(r'"(AI\w+)"', response.text)
        return key[0]

    async def _get_auth_key(self) -> str:
        """
    Get the authentication key from the server or cache.

    This method asynchronously retrieves the authentication key used for making API requests.
    It checks if the current authentication token is still valid and fetches a new one if necessary.

    Returns:
        str: The authentication key/token.

    Raises:
        ValueError: If the server doesn't return a valid authentication token.

    Note:
        The 'client' attribute is expected to be defined elsewhere and represents an HTTP client for making requests.
        The '_counter_calls_auth' and '_auth_token' attributes are assumed to be defined elsewhere for tracking and caching.
        The '_get_google_key' method is expected to be defined elsewhere and provides a Google API key.
        The 'urls' dictionary and 'auth_key_headers' are expected to be defined elsewhere.

    Example:
        auth_key = await self._get_auth_key()
        # Returns the authentication key/token.
    """
        if self._counter_calls_auth < self.max_requests_per_token and self._auth_token:
            self._counter_calls_auth += 1
            return self._auth_token

        params = {"key": await self._get_google_key()}
        json_data = {"returnSecureToken": True}

        response = await self.client.post(
            urls["auth_key"],
            headers=auth_key_headers,
            params=params,
            json=json_data,
            timeout=20,
        )

        result = response.json()
        self._auth_token = result.get("idToken")
        if not self._auth_token:
            raise ValueError("Error on the server side, the token was not returned")
        self._counter_calls_auth = 0
        return self._auth_token

    async def get_styles(self) -> StyleModel:
        """
    Retrieve a list of available styles for image generation.

    This method synchronously queries the server to retrieve a list of available styles
    that can be used for image generation.

    Returns:
        List[StyleModel]: A list of available styles for image generation.

    Note:
        The 'client' attribute is expected to be defined elsewhere and represents an HTTP client for making requests.
        The 'StyleModel.model_validate' method is expected to be defined elsewhere and validates the result data.

    Example:
        styles = self.get_styles()
        # Returns a list of available styles for image generation.
    """
        res = await self.client.get("https://dream.ai/_next/data/ddBu0LvpgvZcniN77Wr0h/create.json")
        return StyleModel.model_validate(res.json())
    
    async def check_task(self, task_id: str, only_bool: bool = False) -> Union[CheckTask, bool]:
        """
    Check the status of a task and retrieve generated image information.

    This method asynchronously checks the status of a task identified by the given task ID.
    It queries the server to determine whether the image associated with the task has been generated.

    Args:
        task_id (str): The ID of the task to be checked.
        only_bool (bool, optional): If True, return a boolean indicating image generation status.
            If False (default), return detailed CheckTask information.

    Returns:
        Union[CheckTask, bool]: If only_bool is False, returns detailed CheckTask information.
            If only_bool is True, returns a boolean indicating whether the image is generated.

    Note:
        The 'client' attribute is expected to be defined elsewhere and represents an HTTP client for making requests.
        The 'check_headers' dictionary is expected to be defined elsewhere.
        The 'CheckTask.model_validate' method is expected to be defined elsewhere and validates the result data.

    Example:
        task_status = await self.check_task("task123")
        # Returns detailed task status information.

        image_generated = await self.check_task("task456", only_bool=True)
        # Returns True if the image is generated, False otherwise.
    """
        img_check_url = f"https://paint.api.wombo.ai/api/v2/tasks/{task_id}"

        response = await self.client.get(img_check_url, headers=check_headers, timeout=10)
        result = CheckTask.model_validate(response.json())
        return bool(result.photo_url_list) if only_bool else result
    
    async def create_task(self, text: str, style: Union[Style, int] = Style.BASESTYLE) -> CreateTask:
        """
    Create a task for generating an image with specified text and style.

    This method asynchronously creates a task for generating an image using the provided input text and style.
    It sends a request to a specified URL with the input data and returns the task information.

    Args:
        text (str): The input text for generating the image.
        style (Style, optional): The style to be applied for the image generation. Defaults to Style.BASESTYLE.

    Returns:
        dict: Task information including the task ID and other relevant details.

    Raises:
        HTTPError: If the HTTP request to create the task fails.

    Note:
        The 'client' attribute is expected to be defined elsewhere and represents an HTTP client for making requests.
        The '_get_auth_key' method is expected to be defined elsewhere and provides the authentication key.
        The 'headers_gen' function is expected to be defined elsewhere and generates the required headers for the request.
        The 'CreateTask.model_validate' method is expected to be defined elsewhere and validates the result data.

    Example:
        task_info = await self.create_task("Generate an image with this text.")
        # Returns task information containing the task ID and other details.
    """
        draw_url = "https://paint.api.wombo.ai/api/v2/tasks"
        auth_key = await self._get_auth_key()
        data = (
                '{"is_premium":false,"input_spec":{"prompt":"%s","style":%d,"display_freq":10}}'
                % (text[:200], style)
        )

        response = await self.client.post(
            url=draw_url, headers=headers_gen(auth_key), data=data, timeout=20
        )
        result_row = response.json()
        result = CreateTask.model_validate(result_row)
        return result
        
    
    async def generate(self,
            text: str,
            style: Style = Style.BASESTYLE,
            timeout: int = 60,
            check_for: int = 3,
            gif: bool = False)-> Union[io.BytesIO, CheckTask]:
        """
    Generate content based on input text and style asynchronously.

    This method generates content, potentially images, based on the provided input text
    and style. It asynchronously creates a task for generation, periodically checks its
    status, and returns the generated content once available.

    Args:
        self: An instance of the class containing this method.
        text (str): The input text for generating content.
        style (Style, optional): The style to be applied for generation. Defaults to Style.BASESTYLE.
        timeout (int, optional): The maximum time in seconds to wait for generation completion. Defaults to 60.
        check_for (int, optional): The time interval in seconds for checking generation status. Defaults to 3.

    Returns:
        Union[GeneratedContent, str]: The generated content or an error message if generation fails.

    Raises:
        TimeoutError: If the generation process exceeds the specified timeout duration.

        ImportError: If the 'gif' option is requested and required dependencies are missing.

    Note:
        The 'create_task', 'check_task', and 'gif' methods are expected to be defined elsewhere.

    Example:
        generated_content = await self.generate("Hello, world!")
        # Returns the generated content or raises TimeoutError if generation takes too long.
    """
        task = await self.create_task(text=text, style=style)
        for _ in range(timeout, 0, -check_for):
            check_task = await self.check_task(task.id)
            if check_task.photo_url_list and check_task.state != "generating":
                if gif:
                    if "pillow" in not_imported:
                        raise ImportError("Pillow not imported, To use without errors, install the extra GIF package or install pillow via pip")
                    return await self.gif(check_task.photo_url_list)
                return check_task
            await asyncio.sleep(check_for)
        else:
            raise TimeoutError(self.out_msg)
        
    async def gif(self, url_list: list, thread: bool = True) -> io.BytesIO:
        """
    Create a streaming GIF from a list of image URLs.

    This method asynchronously creates a streaming GIF from a list of image URLs. It uses the 'Pillow' library
    to process the images and create the GIF.

    Args:
        url_list (list): A list of image URLs to be used for creating the GIF.
        thread (bool, optional): If True, create the GIF in a separate thread for better performance. Defaults to True.

    Returns:
        io.BytesIO: A stream containing the generated GIF.

    Raises:
        ImportError: If 'Pillow' library is not imported or installed.

    Note:
        The 'client' attribute is expected to be defined elsewhere and represents an HTTP client for fetching URLs.
        The 'save_frames_as_gif' method is expected to be defined elsewhere and handles the actual GIF creation.

    Example:
        gif_stream = await self.gif(["url1", "url2", "url3"])
        # Returns a streaming GIF from the provided image URLs.
    """
        if "pillow" in not_imported:
            raise ImportError("Pillow not imported, To use without errors, install the library extra GIF package or install pillow via pip")
        tasks = [asyncio.create_task(self.client.get(url)) for url in url_list]
        urls = await asyncio.gather(*tasks)
        frames = [Image.open(io.BytesIO(url.content)) for url in urls]
        return await asyncio.to_thread(self.save_frames_as_gif(frames)) if thread else self.save_frames_as_gif(frames)