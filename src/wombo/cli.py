#!/usr/bin/env python3

import json
import os
import sys
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

from wombo.api.dream import Dream
from wombo.models import ArtStyleModel

app = typer.Typer(
    name="wombo",
    help="CLI для генерации изображений с помощью Wombo Dream",
    add_completion=False,
)

console = Console()

CONFIG_DIR = Path.home() / ".config" / "wombo"
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_token() -> Optional[str]:
    """Получить токен из конфигурационного файла."""
    if not CONFIG_FILE.exists():
        return None
    
    with open(CONFIG_FILE, "r") as f:
        try:
            config = json.load(f)
            return config.get("token")
        except json.JSONDecodeError:
            return None


def get_dream_with_auth(token=None):
    """Получить экземпляр Dream с авторизацией, если токен не передан."""
    if token is None:
        token = get_token()
    
    dream = Dream(token=token)
    
    # Если токен не был передан или найден в конфиге,
    # Wombo API сам создаст анонимный токен при первом запросе
    if dream._token is None:
        dream.Auth._get_auth_key()
    
    return dream


@app.command()
def styles(
    page: int = typer.Option(1, "--page", "-p", help="Номер страницы для отображения"),
    page_size: int = typer.Option(20, "--size", "-s", help="Количество стилей на странице"),
    premium_only: bool = typer.Option(False, "--premium", help="Показать только премиум стили"),
    free_only: bool = typer.Option(False, "--free", help="Показать только бесплатные стили"),
):
    """Показать доступные стили генерации изображений."""
    dream = get_dream_with_auth()
    
    try:
        art_styles = dream.Style.get_styles()
        
        table = Table(title="Доступные стили")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Название", style="green")
        table.add_column("Премиум", justify="center", style="magenta")
        
        # Сортировка по ID
        sorted_styles = sorted(art_styles.root, key=lambda x: x.id)
        
        # Фильтрация по премиум/бесплатные
        if premium_only:
            sorted_styles = [s for s in sorted_styles if s.is_premium]
        elif free_only:
            sorted_styles = [s for s in sorted_styles if not s.is_premium]
        
        # Пагинация
        total_pages = (len(sorted_styles) + page_size - 1) // page_size
        
        if page < 1 or (total_pages > 0 and page > total_pages):
            console.print(f"[bold red]Ошибка: Страница {page} не существует. Доступно страниц: {total_pages}[/bold red]")
            sys.exit(1)
        
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, len(sorted_styles))
        
        for style in sorted_styles[start_idx:end_idx]:
            premium = "✓" if style.is_premium else "✗"
            table.add_row(str(style.id), style.name, premium)
        
        console.print(table)
        console.print(f"Страница {page} из {total_pages}")
    except Exception as e:
        console.print(f"[bold red]Ошибка при получении стилей: {e}[/bold red]")
        sys.exit(1)


@app.command()
def style(
    style_id: int = typer.Argument(..., help="ID стиля для просмотра информации")
):
    """Показать подробную информацию о стиле."""
    dream = get_dream_with_auth()
    
    try:
        art_styles = dream.Style.get_styles()
        
        # Поиск стиля по ID
        style = next((s for s in art_styles.root if s.id == style_id), None)
        
        if style is None:
            console.print(f"[bold red]Стиль с ID {style_id} не найден.[/bold red]")
            sys.exit(1)
        
        # Создание форматированного вывода информации о стиле
        style_info = Text()
        style_info.append(f"ID: ", style="bright_white")
        style_info.append(f"{style.id}\n", style="cyan")
        
        style_info.append(f"Название: ", style="bright_white")
        style_info.append(f"{style.name}\n", style="green")
        
        style_info.append(f"Премиум: ", style="bright_white")
        style_info.append(f"{'Да' if style.is_premium else 'Нет'}\n", 
                          style="magenta" if style.is_premium else "blue")
        
        style_info.append(f"Модель: ", style="bright_white")
        style_info.append(f"{style.type_model}\n", style="yellow")
        
        style_info.append(f"Поддержка входных изображений: ", style="bright_white")
        style_info.append(f"{'Да' if style.supports_input_images else 'Нет'}\n", 
                          style="green" if style.supports_input_images else "red")
        
        style_info.append(f"Новинка: ", style="bright_white")
        style_info.append(f"{'Да' if style.is_new else 'Нет'}\n", 
                          style="bright_yellow" if style.is_new else "blue")
        
        style_info.append(f"Создан: ", style="bright_white")
        style_info.append(f"{style.created_at}\n", style="blue")
        
        style_info.append(f"Обновлен: ", style="bright_white")
        style_info.append(f"{style.updated_at}\n", style="blue")
        
        # URL изображения со стилем
        style_info.append(f"URL изображения: ", style="bright_white")
        style_info.append(f"{style.photo_url}", style="bright_blue")
        
        console.print(Panel(
            style_info,
            title=f"Стиль: {style.name}",
            border_style="green" if not style.is_premium else "magenta",
            padding=(1, 2)
        ))
        
        console.print("\nПример использования:")
        console.print(f"[bold]wombo generate \"Ваш запрос\" --style {style.id}[/bold]")
        
    except Exception as e:
        console.print(f"[bold red]Ошибка при получении информации о стиле: {e}[/bold red]")
        sys.exit(1)


@app.command()
def examples(
    style_ids: Optional[List[int]] = typer.Argument(None, help="ID стилей для примеров (до 4 стилей)"),
    prompt: str = typer.Option("Русская зима в деревне", "--prompt", "-p", help="Запрос для примеров")
):
    """Сгенерировать примеры изображений с разными стилями для сравнения."""
    import httpx
    
    if not style_ids:
        # Если стили не указаны, используем несколько популярных
        style_ids = [3, 115, 46, 130]  # No Style, Dreamland v3, Anime, HDR v3
    
    if len(style_ids) > 4:
        console.print("[bold red]Можно указать максимум 4 стиля для сравнения.[/bold red]")
        sys.exit(1)
    
    dream = get_dream_with_auth()
    
    # Получаем информацию о стилях
    try:
        art_styles = dream.Style.get_styles()
        styles_info = {}
        
        for style_id in style_ids:
            style = next((s for s in art_styles.root if s.id == style_id), None)
            if style is None:
                console.print(f"[bold red]Стиль с ID {style_id} не найден.[/bold red]")
                sys.exit(1)
            styles_info[style_id] = style.name
    
    except Exception as e:
        console.print(f"[bold red]Ошибка при получении информации о стилях: {e}[/bold red]")
        sys.exit(1)
    
    # Генерируем изображения
    results = {}
    for style_id in style_ids:
        console.print(f"Генерация изображения со стилем [bold]{styles_info[style_id]}[/bold] (ID: {style_id})...")
        
        try:
            with console.status(f"[bold green]Генерация...[/bold green]", spinner="dots"):
                task = dream.generate(
                    text=prompt,
                    style=style_id,
                    timeout=120  # Увеличиваем таймаут для генерации нескольких изображений
                )
                
                if task.result is None:
                    console.print(f"[bold red]Не удалось сгенерировать изображение для стиля {styles_info[style_id]}.[/bold red]")
                    continue
                
                results[style_id] = {
                    "name": styles_info[style_id],
                    "url": task.result.final
                }
                
                console.print(f"[green]✓[/green] Изображение для стиля [bold]{styles_info[style_id]}[/bold] готово")
        
        except Exception as e:
            console.print(f"[bold red]Ошибка при генерации изображения для стиля {styles_info[style_id]}: {e}[/bold red]")
    
    # Выводим результаты
    if results:
        console.print("\n[bold]Результаты генерации:[/bold]")
        
        for style_id, data in results.items():
            console.print(f"\n[bold]{data['name']}[/bold] (ID: {style_id})")
            console.print(f"URL: [blue]{data['url']}[/blue]")
    else:
        console.print("[bold red]Не удалось сгенерировать ни одного изображения.[/bold red]")


@app.command()
def generate(
    prompt: str = typer.Argument(..., help="Текстовый запрос для генерации изображения"),
    style: int = typer.Option(115, "--style", "-s", help="ID стиля генерации"),
    ratio: str = typer.Option("old_vertical_ratio", "--ratio", "-r", help="Соотношение сторон изображения"),
    premium: bool = typer.Option(False, "--premium", "-p", help="Использовать премиум-функции"),
    timeout: int = typer.Option(60, "--timeout", "-t", help="Время ожидания генерации в секундах"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Путь для сохранения изображения"),
):
    """Сгенерировать изображение на основе текстового запроса."""
    import httpx
    
    token = get_token()
    dream = get_dream_with_auth(token)
    
    if premium and not token:
        console.print("[bold red]Для использования премиум-функций необходимо войти в аккаунт.[/bold red]")
        sys.exit(1)
    
    with console.status("[bold green]Генерация изображения...[/bold green]", spinner="dots"):
        try:
            task = dream.generate(
                text=prompt, 
                style=style, 
                ratio=ratio, 
                premium=premium, 
                timeout=timeout
            )
            
            if task.result is None:
                console.print("[bold red]Не удалось сгенерировать изображение в указанное время.[/bold red]")
                sys.exit(1)
            
            image_url = task.result.final
            console.print(f"[bold green]Изображение сгенерировано![/bold green]")
            console.print(f"URL: [bold blue]{image_url}[/bold blue]")
            
            if output:
                # Создаем директорию, если она не существует
                output.parent.mkdir(parents=True, exist_ok=True)
                
                # Скачиваем изображение
                with httpx.Client() as client:
                    response = client.get(image_url)
                    with open(output, "wb") as f:
                        f.write(response.content)
                
                console.print(f"Изображение сохранено: [bold]{output}[/bold]")
        
        except Exception as e:
            console.print(f"[bold red]Ошибка при генерации изображения: {e}[/bold red]")
            sys.exit(1)


@app.command()
def login(token: str = typer.Argument(..., help="Токен для аутентификации")):
    """Войти в аккаунт, используя токен."""
    # Проверяем токен
    dream = Dream(token=token)
    
    try:
        # Пробуем получить стили, чтобы проверить валидность токена
        dream.Style.get_styles()
        
        # Сохраняем токен в конфигурационный файл
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(CONFIG_FILE, "w") as f:
            json.dump({"token": token}, f)
        
        console.print("[bold green]Успешный вход в аккаунт![/bold green]")
    
    except Exception as e:
        console.print(f"[bold red]Ошибка при входе в аккаунт: {e}[/bold red]")
        sys.exit(1)


@app.command()
def logout():
    """Выйти из аккаунта."""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
        console.print("[bold green]Выход из аккаунта выполнен успешно![/bold green]")
    else:
        console.print("[yellow]Вы не были авторизованы.[/yellow]")


@app.command()
def status():
    """Показать текущий статус авторизации."""
    token = get_token()
    if token:
        console.print("[bold green]Вы авторизованы.[/bold green]")
        console.print(f"Токен: [dim]{token[:10]}...{token[-5:]}[/dim]")
    else:
        console.print("[yellow]Вы не авторизованы.[/yellow]")


if __name__ == "__main__":
    app() 