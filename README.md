<h1 align="center">Hi there, I'm</h1>


<a href="https://github.com/pokedim13/WOMBO" target="_blank">
  <img src="https://upload.wikimedia.org/wikipedia/commons/d/d7/WomboLogo.svg"/>
</a>

### I am a module for using wombo dream ai (neural network of image generation)

#### There are some changes in the new version of dream, We did not record the last version, so you will have to rewrite your previous code. We apologize for the sincere inconvenience

<details>
    <summary style="font-size: 24px; font-weight: bold;">Documentation</summary>
    For the asynchronous use case, it is similar
    <details>
        <summary style="font-size: 24px; font-weight: bold;">Creating an instance</summary> 
        <pre>
from wombo import Dream
dream = Dream()
        </pre>
    </details>
    <details>
        <summary style="font-size: 24px; font-weight: bold;">Generate picture</summary> 
        <pre>
from wombo.models import TaskModel
picture: TaskModel = dream.generate("anime waifu")
        </pre>
    </details>
    <details>
        <summary style="font-size: 24px; font-weight: bold;">API</summary> 
        <pre>
task: TaskModel = dream.api.create_task("anime waifu")
dream.api.check_task(task.id)
        </pre>
    </details>
    <details>
        <summary style="font-size: 24px; font-weight: bold;">Styles</summary> 
        <pre>
from wombo.models import StyleModel
styles: = dream.styles._get_styles()
dream.styles["Dreamland v3"] # Required after executing _get_styles()
        </pre>
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
</details>
