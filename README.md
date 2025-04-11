<div align="center">
    <h2>Hello, Hello! My name is</h2>
    <img src="assets/logos/wombo.png">
    <h2>Библиотека и CLI для работы с Wombo Dream API</h2>
</div>

## Установка

```bash
# Только библиотека
pip install wombo

# Установка с CLI интерфейсом
pip install wombo[cli]

# С помощью uv
uv pip install wombo[cli]

# Для разработки из исходников
git clone https://github.com/pokedim13/wombo.git
cd wombo
uv sync --all-groups  # установка всех зависимостей
uv pip install -e .   # установка библиотеки в режиме разработки
```

## Использование библиотеки

```python
from wombo.api import Dream

# Создаем экземпляр Dream
dream = Dream()

# Получаем доступные стили
styles = dream.Style.get_styles()

# Генерируем изображение
task = dream.generate(
    text="Русская зима в деревне",
    style=115,  # Dreamland v3
    timeout=60
)

# Получаем URL изображения
print(task.result.final)
```

## CLI-интерфейс

Библиотека также предоставляет CLI-интерфейс для удобного использования в командной строке.

### Вывод доступных стилей

```bash
wombo styles
```

Параметры:
- `--page`, `-p`: Номер страницы для отображения (по умолчанию 1)
- `--size`, `-s`: Количество стилей на странице (по умолчанию 20)
- `--premium`: Показать только премиум стили
- `--free`: Показать только бесплатные стили

Примеры:
```bash
# Показать первую страницу стилей
wombo styles

# Показать только премиум стили
wombo styles --premium

# Показать вторую страницу с размером 10 стилей
wombo styles -p 2 -s 10
```

### Информация о стиле

```bash
wombo style <ID>
```

Пример:
```bash
wombo style 115
```

### Генерация изображения

```bash
wombo generate <ЗАПРОС> [ПАРАМЕТРЫ]
```

Параметры:
- `--style`, `-s`: ID стиля генерации (по умолчанию 115)
- `--ratio`, `-r`: Соотношение сторон изображения (по умолчанию old_vertical_ratio)
- `--premium`, `-p`: Использовать премиум-функции
- `--timeout`, `-t`: Время ожидания генерации в секундах (по умолчанию 60)
- `--output`, `-o`: Путь для сохранения изображения

Примеры:
```bash
# Генерация изображения с запросом "Русская зима в деревне"
wombo generate "Русская зима в деревне"

# Генерация с указанным стилем и сохранением в файл
wombo generate "Русская зима в деревне" -s 46 -o image.jpg
```

### Сравнение стилей

```bash
wombo examples [СТИЛИ] [ПАРАМЕТРЫ]
```

Параметры:
- `--prompt`, `-p`: Запрос для примеров (по умолчанию "Русская зима в деревне")

Примеры:
```bash
# Сравнение стандартных стилей
wombo examples

# Сравнение указанных стилей
wombo examples 3 46 115 130 --prompt "Закат на море"
```

### Управление аккаунтом

```bash
# Вход в аккаунт с токеном
wombo login <ТОКЕН>

# Выход из аккаунта
wombo logout

# Проверка статуса авторизации
wombo status
```

## Использование с uv

Если вы используете uv, можно запускать команды через него:

```bash
uv run wombo styles
uv run wombo generate "Ваш запрос" -s 115
```

<div>См. примеры использования</div>
<img src="assets/example.gif">