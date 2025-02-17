<h1 align="center">Привет всем, меня зовут</h1>


<a href="https://gitverse.ru/sweetdogs/wombo" target="_blank">
  <img src="https://upload.wikimedia.org/wikipedia/commons/d/d7/WomboLogo.svg"/>
</a>

### Я модуль для использования нейросети dream от кампании wombo 

#### Sweetdogs (Разработчик, так же известный как pokedim13, H3try) придерживается ZeroVer. Поэтому обратная совместимость не гарантируется. Так же кампания wombo может обанкротиться или ещё что. В общем issue вы написать сможете, но решения вашей проблемы можете не ждать.


<details>
    <summary style="font-size: 24px; font-weight: bold;">Документация</summary>
    При асинхронном использовании, всё точно так же, только не забудьте вызвать await
    <details>
        <summary style="font-size: 24px; font-weight: bold;">Создание экземпляра</summary> 
        <pre>
from wombo import Dream # or AsyncDream
dream = Dream()
        </pre>
    </details>
    <details>
        <summary style="font-size: 24px; font-weight: bold;">Генерация изображения</summary> Может принимать следующие параметры:
        <li>text: str</li>
        <li>*style: int</li>
        <li>*ratio: str</li>
        <li>*premium: bool</li>
        <li>*display_freq: int</li>
        <li>*timeout: int</li>
        <li>*check_for: int</li>
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
dream.api.tradingcard(task.id)
        </pre>
    </details>
    <details>
    <summary style="font-size: 24px; font-weight: bold;">Стили</summary> 
        <pre>
from wombo.models import StylesModel, StyleModel
styles: = dream.styles.get_styles()
        </pre>
    </details>
    <details>
    <summary style="font-size: 24px; font-weight: bold;">Профиль</summary> 
    Смотрите в коде
    </details>

</details>

#

<details>
    <summary style="font-size: 24px; font-weight: bold;">Разработчики</summary>

- [@sweetdogs](https://vk.com/sweetdogs) - Мой профиль
</details>