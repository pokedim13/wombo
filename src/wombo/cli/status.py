import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .app import app
from .login import load_token, get_config_path

console = Console()

@app.command()
def status():
    """
    Проверка текущего статуса авторизации в сервисе Wombo Dream.
    """
    token = load_token()
    config_path = get_config_path()
    
    # Создаем таблицу для отображения информации
    table = Table(show_header=False, box=None)
    table.add_column("Параметр", style="cyan")
    table.add_column("Значение", style="green")
    
    # Путь к конфигурации
    table.add_row("Конфигурация", str(config_path))
    
    # Статус авторизации
    if token:
        auth_status = "[bold green]Авторизован[/bold green]"
        # Показываем часть токена для безопасности
        masked_token = f"{token[:8]}...{token[-8:]}" if len(token) > 16 else "***"
        table.add_row("Статус", auth_status)
        table.add_row("Токен", masked_token)
    else:
        auth_status = "[bold red]Не авторизован[/bold red]"
        table.add_row("Статус", auth_status)
        
    # Выводим информацию в консоль
    console.print(Panel(
        table,
        title="Статус Wombo Dream",
        expand=False
    ))
    
    # Подсказка для действий
    if not token:
        console.print("\nДля авторизации используйте: [bold]wombo login[/bold]") 