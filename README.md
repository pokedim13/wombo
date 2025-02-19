<div align="center">
    <h1 align="center">Привет, меня зовут</h1>
    <a href="https://gitverse.ru/sweetdogs/wombo" target="_blank">
        <img src="assets/logos/wombo.png"/>
    </a>
    <div>
        Я модуль для использования нейросети dream от компании wombo
    </div>
    <div align="center" style="padding-top: 10px;">
        <a href="https://gitverse.ru/sweetdogs/wombo" target="_blank">
            <img src="https://img.shields.io/badge/License-MIT-blue.svg"/>
        </a>
    </div>
</div>
<div align="center">
    <h2 align="center">Документация</h2>
    <details>
        <summary style="font-size: 18px; font-weight: bold;">Генерация изображения</summary>
        ВАЖНО: После недавнего обновления, после создания экземпляра нужно обновлять токен с помощью Dream().auth._get_auth_key(). Если вы используете свой от аккаунта, это не требуется!
        <div style="margin-top: 10px; font-size: 16px;">
        <details style="padding-bottom: 10px;">
            <summary>может принимать следующие параметры</summary>
            <ul style="list-style-type: disc; padding-left: 20px;">
            <li><strong>text:</strong> str</li>
            <li><strong>*style:</strong> int</li>
            <li><strong>*ratio:</strong> str</li>
            <li><strong>*premium:</strong> bool</li>
            <li><strong>*display_freq:</strong> int</li>
            <li><strong>*timeout:</strong> int</li>
            <li><strong>*check_for:</strong> int</li>
        </ul>
        </details>
        <pre style="padding: 10px; border-radius: 5px; overflow: auto;">
from wombo.models import TaskModel
picture: TaskModel = dream.generate("anime waifu")
        </pre>
    </div>
    </details>
    <details>
        <summary style="font-size: 18px; font-weight: bold;">Профиль</summary>
        Этому разделу прекращена поддержка, но он рабочий. Смотрите в коде
    </details>
    <details>
        <summary style="font-size: 18px; font-weight: bold;">Стили</summary>
        <pre>
from wombo.models import StylesModel, StyleModel
styles: = dream.styles.get_styles()
        </pre>
    </details>
    <details>
        <summary style="font-size: 18px; font-weight: bold;">API</summary>
        <div>
            ВАЖНО: После недавнего обновления, после создания экземпляра нужно обновлять токен с помощью Dream().auth._get_auth_key(). Если вы используете свой от аккаунта, это не требуется!
        </div>
        <details style="padding-bottom: 10px;">
            <summary>может принимать следующие параметры</summary>
            <ul style="list-style-type: disc; padding-left: 20px;">
            <li><strong>text:</strong> str</li>
            <li><strong>*style:</strong> int</li>
            <li><strong>*ratio:</strong> str</li>
            <li><strong>*premium:</strong> bool</li>
            <li><strong>*display_freq:</strong> int</li>
        </ul>
        </details>
        <pre>
task: TaskModel = dream.api.create_task("anime waifu")
dream.api.check_task(task.id)
dream.api.tradingcard(task.id)
        </pre>
    </details>
    <div align="center" style="padding-top: 10px;">
        <div>Скачать можно тут</div>
        <a href="https://gitverse.ru/sweetdogs/wombo/packages" target="_blank">
            <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
        </a>
    </div>
</div>
<div align="center" style="padding-top: 10px;">
    <h2 align="center">Разработчики</h2>
    <div align="center">
        <a href="https://gitverse.ru/sweetdogs" style="color: inherit; text-decoration: none; font-size: 18px; background-image: linear-gradient(to right,rgb(28, 245, 28),rgb(124, 124, 241)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">sweetdogs</a>
    </div>
    <div align="center">
        <a href="https://github.com/mayn3r" style="color: inherit; text-decoration: none; font-size: 18px; background-image: linear-gradient(to right, #ff0033, #ff4da6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">mayn3r</a>
    </div>
</div>