import json
import os
import typer
import platform
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from wombo import Dream
from .app import app

console = Console()

def get_config_path() -> Path:
    """Получение пути к конфигурационному файлу в зависимости от ОС."""
    system = platform.system()
    
    if system == "Windows":
        # Для Windows используем AppData/Roaming
        config_dir = Path(os.environ.get("APPDATA", "")) / "akellare" / "wombo"
    else:
        # Для Unix-систем (Linux, macOS) используем ~/.config/wombo
        config_dir = Path.home() / ".config" / "akellare" / "wombo"
        
    config_dir.mkdir(exist_ok=True, parents=True)
    return config_dir / "config.json"

def get_images_dir() -> Path:
    """Получение пути к директории для сохранения изображений."""
    system = platform.system()
    
    if system == "Windows":
        # Для Windows используем Документы/wombo
        docs_path = Path(os.path.expanduser("~/Documents"))
        images_dir = docs_path / "akellare" / "wombo" / "images"
    else:
        # Для Unix-систем (Linux, macOS) используем ~/wombo/images
        images_dir = Path.home() / "akellare" / "wombo" / "images"
        
    images_dir.mkdir(exist_ok=True, parents=True)
    return images_dir

def save_token(token: str) -> None:
    """Сохранение токена в конфигурационный файл."""
    config_path = get_config_path()
    config = {}
    
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            console.print("[yellow]Ошибка чтения файла конфигурации. Создаём новый.[/yellow]")
    
    config["token"] = token
    
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

def load_token() -> str | None:
    """Загрузка токена из конфигурационного файла."""
    config_path = get_config_path()
    
    if not config_path.exists():
        return None
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("token")
    except (json.JSONDecodeError, FileNotFoundError):
        return None

@app.command()
def login(
    token: str = typer.Option(None, "--token", "-t", help="Указать существующий токен API"),
    force_new: bool = typer.Option(False, "--force-new", "-f", help="Принудительно получить новый токен"),
):
    """
    Аутентификация в сервисе Wombo Dream. 
    Если токен не указан, будет получен анонимный токен.
    """
    existing_token = None if force_new else load_token()
    
    if existing_token and not token:
        console.print("[green]Используется существующий токен из конфигурации.[/green]")
        save_token(existing_token)
        return
    
    if token:
        # Используем указанный токен
        console.print("[green]Используется указанный токен.[/green]")
        save_token(token)
        return
    
    # Получаем анонимный токен через API
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Получение анонимного токена...[/bold blue]"),
        console=console,
    ) as progress:
        progress.add_task("download", total=None)
        try:
            dream = Dream()
            new_token = dream.Auth._get_auth_key()
            
            if new_token:
                save_token(new_token)
                console.print(Panel(
                    "[bold green]Аутентификация успешна[/bold green]\n"
                    f"Анонимный токен получен и сохранен в [bold]{get_config_path()}[/bold]",
                    title="Wombo Login"
                ))
            else:
                console.print("[bold red]Не удалось получить токен.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Ошибка при получении токена: {e}[/bold red]")

@app.command()
def logout():
    """
    Выход из системы и удаление сохраненного токена.
    """
    config_path = get_config_path()
    
    if not config_path.exists():
        console.print("[yellow]Конфигурационный файл не найден. Вы не авторизованы.[/yellow]")
        return
    
    try:
        # Загружаем существующую конфигурацию
        with open(config_path, "r") as f:
            config = json.load(f)
        
        # Удаляем токен
        if "token" in config:
            del config["token"]
            
            # Сохраняем обновленную конфигурацию
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
                
            console.print(Panel(
                "[bold green]Выход выполнен успешно[/bold green]\n"
                "Токен авторизации удален из конфигурации.",
                title="Wombo Logout"
            ))
        else:
            console.print("[yellow]Токен не найден в конфигурации. Вы уже не авторизованы.[/yellow]")
            
    except Exception as e:
        console.print(f"[bold red]Ошибка при выходе из системы: {e}[/bold red]") 