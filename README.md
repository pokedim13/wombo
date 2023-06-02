<h1 align="center">Hi there, I'm <a href="https://github.com/pokedim13/WOMBO" target="_blank">Wombo</a> 

### I am a module for using wombo dream ai (neural network of image generation)

## Mini Documentation
#### Asynchronous and synchronous module
```
from wombo import AsyncDream # async
from wombo import Dream # sync
```

#### Create a task 
- since all actions are the same in both versions, I will consider only one module, namely the asynchronous
```
dream = AsyncDream()
task = await dream.create_task(prompt: str, style: int)
```
- The list of styles will be available via github

#### Check a task (complite or no)
```
task = await dream.check_task(task.id) 
# To get information about readiness in bool format

task = await dream.check_task(task.id, False) 
# To get information about readiness
```

#### Create gif
- photo_url_list Only the already generated image has. To check the image, use check_task(). Return io.BytesIO()
```
gif = await dream.gif(task.photo_url_list)

gif = await dream.gif(task.photo_url_list, thread=False)
# Used if you don't want to use an asynchronous thread.
# to generate a gif, it is true since the generation is quite long
```


<h2>requirements</h2>

- [httpx](https://pypi.org/project/httpx/)
- [pillow](https://pypi.org/project/Pillow/)
- [pydantic](https://pypi.org/project/pydantic/)
