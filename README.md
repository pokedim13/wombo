<h1 align="center">Hi there, I'm <a href="https://github.com/pokedim13/WOMBO" target="_blank">Wombo</a> 

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
dream = AsyncDream()
task = await dream.create_task(prompt: str, style: int)
```
- The list of styles will be available via github

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

gif = await dream.gif(task.photo_url_list, thread=False)
# Used if you don't want to use an asynchronous thread.
# to generate a gif, it is true since the generation is quite long
# Generation in the thread is not available for the synchronous library
```

</details>

#

<details>
<summary style="font-size: 24px; padding-left: 6vh;">Generate</summary>

- 1 command to receive, reply immediately. without checks via check_task()
```
gif = await dream.generate(taxt:str, syle: int, gif: bool)

```

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
