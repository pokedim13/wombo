<h1 align="center">Hi there, I'm</h1>

<script src="https://vk.com/js/api/openapi.js?169" type="text/javascript"></script>

<a href="https://github.com/pokedim13/WOMBO" target="_blank">
  <img src="https://upload.wikimedia.org/wikipedia/commons/d/d7/WomboLogo.svg"/>
</a>

### I am a module for using wombo dream ai (neural network of image generation)

#### There are some changes in the new version of dream, We did not record the last version, so you will have to rewrite your previous code. We apologize for the sincere inconvenience

<details>
    <summary style="font-size: 24px">Mini Documentation</summary>
    <details>
        <summary style="font-size: 20px; padding-left: 6vh;">Synchro version</summary>
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">Import</summary>
            <div>Basic import</div> 
            <pre>
from wombo import Dream # sync
dream = Dream(out_msg: str)
# out_msg: Message for response errors from the server
            </pre>
        </details>
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">Get styles</summary>
            <pre>
dream.get_styles() -> StyleModel
# return pydantic model
            </pre>
        </details>
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">Check task</summary>
            <pre>
dream.check_task(self, task_id: str, only_bool: bool = False) -> Union[CheckTask, bool]
# only_bool: If this flag is set, false or True will be returned, depending on the completeness of the task
            </pre>
        </details>    
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">Create task</summary>
            <pre>
dream.create_task(self, text: str, style: Union[Style, int] = Style.BASESTYLE) -> CreateTask
# style: Style identifier, yes, too fashionable class, it's on style
            </pre>
        </details>
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">Generate</summary>
            <pre>
dream.generate(text: str, style: Style = Style.BASESTYLE, timeout: int = 60, check_for: int = 3, gif: bool = False)  -> Union[io.BytesIO, CheckTask]
# style: Style identifier, yes, too fashionable class, it's on style
# timeout: The number of seconds after which the task will stop being checked and will throw Timeout error
# check_for: Race in how many seconds to do the check
# gif: Flag, create a gif or not
            </pre>
        </details>
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">GIF</summary>
            <pre>
dream.gif(self, url_list: list) -> io.BytesIO
# url_list: List[str] list of links to images (CheckTask.photo_url_list)
            </pre>
        </details>
    </details>
    <details>
        <summary style="font-size: 20px; padding-left: 6vh;">Asynchronous version</summary>
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">Import</summary>
            <div>Basic import</div> 
            <pre>
from wombo import AsyncDream # sync
dream = AsyncDream(out_msg: str)
# out_msg: Message for response errors from the server
            </pre>
        </details>
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">Get styles</summary>
            <pre>
await dream.get_styles() -> StyleModel
# return pydantic model
            </pre>
        </details>
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">Check task</summary>
            <pre>
await dream.check_task(self, task_id: str, only_bool: bool = False) -> Union[CheckTask, bool]
# only_bool: If this flag is set, false or True will be returned, depending on the completeness of the task
            </pre>
        </details>    
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">Create task</summary>
            <pre>
await dream.create_task(self, text: str, style: Union[Style, int] = Style.BASESTYLE) -> CreateTask
# style: Style identifier, yes, too fashionable class, it's on style
            </pre>
        </details>
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">Generate</summary>
            <pre>
await dream.generate(text: str, style: Style = Style.BASESTYLE, timeout: int = 60, check_for: int = 3, gif: bool = False)  -> Union[io.BytesIO, CheckTask]
# style: Style identifier, yes, too fashionable class, it's on style
# timeout: The number of seconds after which the task will stop being checked and will throw Timeout error
# check_for: Race in how many seconds to do the check
# gif: Flag, create a gif or not
            </pre>
        </details>
        <details>
            <summary style="font-size: 16px; padding-left: 12vh;">GIF</summary>
            <pre>
await dream.gif(self, url_list: list, thread: bool = True) -> io.BytesIO
# url_list: List[str] list of links to images (CheckTask.photo_url_list)
# thread: Run the task to create a gif in another thread, so as not to block the program
            </pre>
        </details>
    </details>
</details>

#

<details>
<summary style="font-size: 24px; font-weight: bold;">Creditless</summary>

- [@mayneryt](https://vk.com/mayneryt) her give me algoritm
- [@pokedim13](https://vk.com/h3try) me

</details>

#

<details>
<summary style="font-size: 24px; font-weight: bold;">Requirements</summary>

- [httpx](https://pypi.org/project/httpx/)
- [pydantic](https://pypi.org/project/pydantic/)
- [pillow](https://pypi.org/project/Pillow/) Optinal

</details>
