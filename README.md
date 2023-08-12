<h1 align="center">Hi there, I'm</h1>


<a href="https://github.com/pokedim13/WOMBO" target="_blank">
  <img src="https://upload.wikimedia.org/wikipedia/commons/d/d7/WomboLogo.svg"/>
</a>

### I am a module for using wombo dream ai (neural network of image generation)

<details>
<summary style="font-size: 36px">Mini Documentation</summary>

<details>
<summary style="font-size: 24px; padding-left: 6vh;">Asynchronous and synchronous module</summary>

```
from wombo import AsyncDream # async
from wombo import Dream # sync
```

</details>

#

<details>
<summary style="font-size: 24px; padding-left: 6vh;">Create a task</summary>

- since all actions are the same in both versions, I will consider only one module, namely the asynchronous
```
from wombo.base_models.styles import Style

dream = AsyncDream()
task = await dream.create_task(prompt: str, style: Style)
```
- The list of styles is in Style(Enum) your IDE will tell you to find the desired style

</details>

#

<details>
<summary style="font-size: 24px; padding-left: 6vh;">Check a task (complite or no)</summary>

```
task = await dream.check_task(task.id) 
# To get information about readiness in bool format

task = await dream.check_task(task.id, False) 
# To get information about readiness
```

</details>

#

<details>
<summary style="font-size: 24px; padding-left: 6vh;">Create gif</summary>

- photo_url_list Only the already generated image has. To check the image, use check_task(). Return io.BytesIO()
```
gif = await dream.gif(task.photo_url_list)

# to generate a gif, it is true since the generation is quite long
# Generation in the thread is not available for the synchronous library
```

</details>

#

<details>
<summary style="font-size: 24px; padding-left: 6vh;">Generate</summary>

- one command to receive, reply immediately. without checks via check_task()


<details>
<summary style="font-size: 15px; padding-left: 6vh;">Generate Image</summary>

```
image = await dream.generate_image(taxt:str, syle: Style)
```
- Return io.BytesIO
</details>


<details>
<summary style="font-size: 15px; padding-left: 6vh;">Generate Image</summary>

```
gif = await dream.generate_gif(taxt:str, syle: Style)
```
- Return io.BytesIO
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
- [pillow](https://pypi.org/project/Pillow/)
- [pydantic](https://pypi.org/project/pydantic/)

</details>
