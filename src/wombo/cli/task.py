import os
import time
import typer
from pathlib import Path
from typing import Optional, List, Annotated
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.markdown import Markdown

from wombo import Dream
from wombo.models import TaskModel
from .app import app
from .login import load_token, get_images_dir

console = Console()

def save_image(url: str, filename: str) -> Path:
    """Сохранение изображения по URL."""
    import httpx
    
    # Получаем директорию для сохранения изображений
    images_dir = get_images_dir()
    
    # Полный путь к файлу
    file_path = images_dir / filename
    
    console.print(f"[blue]Загрузка изображения с URL: {url}[/blue]")
    
    # Скачиваем изображение
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url)
            response.raise_for_status()
            
            # Проверяем размер ответа
            content_length = len(response.content)
            console.print(f"[blue]Получен ответ, размер: {content_length} байт[/blue]")
            
            if content_length == 0:
                raise ValueError("Пустой ответ от сервера")
                
            # Сохраняем изображение
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            console.print(f"[green]Файл успешно записан: {file_path}[/green]")
            
            return file_path
    except httpx.RequestError as e:
        raise Exception(f"Ошибка сетевого запроса: {e}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"Сервер вернул ошибку: {e.response.status_code}")
    except Exception as e:
        raise Exception(f"Ошибка при сохранении: {str(e)}")

def display_task_info(task: TaskModel) -> None:
    """Отображение информации о задаче."""
    table = Table(show_header=False)
    table.add_column("Параметр", style="cyan")
    table.add_column("Значение", style="green")
    
    table.add_row("ID задачи", task.id)
    table.add_row("Состояние", task.state)
    table.add_row("Запрос", task.input_spec.prompt)
    table.add_row("Стиль", str(task.input_spec.style))
    table.add_row("Соотношение", task.input_spec.aspect_ratio)
    table.add_row("Премиум", "Да" if task.premium else "Нет")
    table.add_row("Создана", task.created_at)
    table.add_row("Обновлена", task.updated_at)
    
    # Отображаем URL изображения, если задача завершена
    if task.result:
        table.add_row("Результат", "[bold green]Готово[/bold green]")
        table.add_row("URL", task.result.final)
    
    console.print(Panel(table, title=f"Задача: {task.id}", expand=False))
    
    # Отображаем превью URL, если задача завершена
    if task.result:
        console.print(Panel(f"[link={task.result.final}]Ссылка на изображение[/link]", 
                           title="Результат", expand=False))

@app.command()
def create(
    prompt: Annotated[str, typer.Argument(help="Текстовый запрос для генерации изображения")],
    style: Annotated[int, typer.Option("--style", "-s", help="ID стиля изображения")] = 115,
    ratio: Annotated[str, typer.Option("--ratio", "-r", help="Соотношение сторон изображения")] = "old_vertical_ratio",
    premium: Annotated[bool, typer.Option("--premium", "-p", help="Использовать премиум опции")] = False,
    display_freq: Annotated[int, typer.Option("--freq", "-f", help="Частота обновления изображения")] = 10,
    wait: Annotated[bool, typer.Option("--wait", "-w", help="Ожидать завершения задачи")] = False,
    timeout: Annotated[int, typer.Option("--timeout", "-t", help="Время ожидания в секундах при --wait")] = 60,
    check_interval: Annotated[int, typer.Option("--interval", "-i", help="Интервал проверки в секундах при --wait")] = 3,
    save: Annotated[bool, typer.Option("--save", help="Сохранить изображение локально после генерации")] = False,
):
    """
    Создание задачи на генерацию изображения в Wombo Dream.
    """
    # Загружаем токен
    token = load_token()
    if not token:
        console.print("[bold red]Не авторизован. Используйте [/bold red][bold]wombo login[/bold][bold red] для авторизации.[/bold red]")
        raise typer.Exit(code=1)
    
    # Создаем клиент
    dream = Dream(token=token)
    
    task = None
    
    # Создаем задачу и получаем её ID
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Создание задачи генерации...[/bold blue]"),
        console=console,
    ) as progress:
        progress.add_task("create", total=None)
        try:
            # Создаем задачу
            task = dream.API.create_task(
                text=prompt,
                style=style,
                ratio=ratio,
                premium=premium,
                display_freq=display_freq
            )
        except Exception as e:
            console.print(f"[bold red]Ошибка при создании задачи: {e}[/bold red]")
            raise typer.Exit(code=1)
    
    # Выводим информацию о созданной задаче
    console.print("[bold green]Задача успешно создана![/bold green]")
    display_task_info(task)
    
    # Если указан флаг ожидания, ждем завершения после закрытия первого Progress
    if wait:
        wait_and_check_task(dream, task.id, timeout, check_interval, save)
    else:
        console.print(f"\nИспользуйте [bold]wombo check {task.id}[/bold] для проверки статуса.")

@app.command()
def check(
    task_id: Annotated[str, typer.Argument(help="ID задачи для проверки")],
    save: Annotated[bool, typer.Option("--save", help="Сохранить изображение локально после генерации")] = False,
):
    """
    Проверка статуса задачи по ID.
    """
    # Загружаем токен
    token = load_token()
    if not token:
        console.print("[bold red]Не авторизован. Используйте [/bold red][bold]wombo login[/bold][bold red] для авторизации.[/bold red]")
        raise typer.Exit(code=1)
    
    # Создаем клиент
    dream = Dream(token=token)
    
    task = None
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Проверка статуса задачи...[/bold blue]"),
        console=console,
    ) as progress:
        progress.add_task("check", total=None)
        try:
            # Проверяем статус задачи
            task = dream.API.check_task(task_id)
        except Exception as e:
            console.print(f"[bold red]Ошибка при проверке задачи: {e}[/bold red]")
            raise typer.Exit(code=1)
    
    display_task_info(task)
    
    # Если задача завершена и нужно сохранить изображение
    if task.result and save:
        save_and_show_image(task)

def wait_and_check_task(dream: Dream, task_id: str, timeout: int, check_interval: int, save: bool):
    """Ожидание и проверка статуса задачи."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Ожидание результата...[/bold blue] {task.description}"),
        BarColumn(),
        TextColumn("[bold]{task.percentage:.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task_progress = progress.add_task(task_id="generation", total=timeout, description="Инициализация...")
        
        start_time = time.time()
        elapsed = 0
        completed = False
        
        while elapsed < timeout:
            try:
                # Обновляем прогресс
                progress.update(task_progress, completed=elapsed, description=f"Прошло {elapsed}с из {timeout}с")
                
                # Проверяем статус задачи
                task = dream.API.check_task(task_id)
                
                # Если задача завершена
                if task.result is not None:
                    progress.update(task_progress, completed=timeout, description="Генерация завершена!")
                    completed = True
                    break
                
                # Ждем следующей проверки
                time.sleep(check_interval)
                elapsed = int(time.time() - start_time)
                
            except Exception as e:
                console.print(f"[bold red]Ошибка при проверке задачи: {e}[/bold red]")
                break
    
    if completed:
        console.print("[bold green]Задача успешно завершена![/bold green]")
        task = dream.API.check_task(task_id)
        display_task_info(task)
        
        # Сохраняем изображение, если указан флаг
        if save:
            save_and_show_image(task)
    else:
        console.print("[bold yellow]Время ожидания истекло. Задача может всё ещё выполняться.[/bold yellow]")
        console.print(f"Используйте [bold]wombo check {task_id}[/bold] для повторной проверки.")

def save_and_show_image(task: TaskModel):
    """Сохранение и отображение информации об изображении."""
    if not task.result or not task.result.final:
        console.print("[bold red]Ошибка: задача не имеет результата или URL изображения.[/bold red]")
        return
        
    # Формируем имя файла из запроса и ID задачи
    safe_prompt = "".join(c if c.isalnum() or c == '_' else '_' for c in task.input_spec.prompt[:20])
    filename = f"{safe_prompt}_{task.id}.jpg"
    
    console.print(f"[bold blue]Сохранение изображения с URL: {task.result.final}[/bold blue]")
    try:
        file_path = save_image(task.result.final, filename)
        console.print(f"[bold green]Изображение сохранено:[/bold green] {file_path}")
    except Exception as e:
        console.print(f"[bold red]Ошибка при сохранении изображения: {e}[/bold red]") 