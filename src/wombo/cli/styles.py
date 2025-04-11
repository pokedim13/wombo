import typer
from typing import Optional, Annotated
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from wombo import Dream
from wombo.models import StyleModel
from .app import app
from .login import load_token

console = Console()

@app.command()
def styles(
    show_premium: Annotated[bool, typer.Option("--premium", "-p", help="Показать только премиум стили")] = False,
    show_regular: Annotated[bool, typer.Option("--regular", "-r", help="Показать только обычные стили")] = False,
    sort_by: Annotated[str, typer.Option("--sort", "-s", help="Сортировка (id, name)")] = "id",
):
    """
    Получение списка доступных стилей для генерации изображений.
    """
    # Загружаем токен
    token = load_token()
    if not token:
        console.print("[bold red]Не авторизован. Используйте [/bold red][bold]wombo login[/bold][bold red] для авторизации.[/bold red]")
        raise typer.Exit(code=1)
    
    # Создаем клиент
    dream = Dream(token=token)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Получение списка стилей...[/bold blue]"),
        console=console,
    ) as progress:
        progress.add_task("styles", total=None)
        try:
            # Получаем стили
            art_styles = dream.Style.get_styles()
        except Exception as e:
            console.print(f"[bold red]Ошибка при получении стилей: {e}[/bold red]")
            raise typer.Exit(code=1)
    
    # Создаем таблицу для отображения стилей
    table = Table(title="Стили изображений Wombo Dream")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Название", style="green")
    table.add_column("Премиум", justify="center")
    table.add_column("Новый", justify="center")
    
    # Фильтруем и сортируем стили
    styles_list = art_styles.root
    
    # Фильтрация по типу (премиум/обычные)
    if show_premium and not show_regular:
        styles_list = [style for style in styles_list if style.is_premium]
    elif show_regular and not show_premium:
        styles_list = [style for style in styles_list if not style.is_premium]
    
    # Сортировка
    if sort_by.lower() == "name":
        styles_list = sorted(styles_list, key=lambda x: x.name)
    else:  # По умолчанию сортируем по ID
        styles_list = sorted(styles_list, key=lambda x: x.id)
    
    # Заполняем таблицу данными
    for style in styles_list:
        premium_status = "[bold green]Да[/bold green]" if style.is_premium else "[red]Нет[/red]"
        new_status = "[bold yellow]Да[/bold yellow]" if style.is_new else "[grey]Нет[/grey]"
        table.add_row(
            str(style.id),
            style.name,
            premium_status,
            new_status
        )
    
    # Выводим таблицу
    console.print(table)
    
    # Вывод итоговой статистики
    premium_count = len([s for s in styles_list if s.is_premium])
    regular_count = len(styles_list) - premium_count
    
    console.print(f"\nВсего стилей: [bold]{len(styles_list)}[/bold] "
                 f"([bold green]{premium_count}[/bold green] премиум, "
                 f"[bold blue]{regular_count}[/bold blue] обычных)")
    
    # Подсказка для использования
    console.print("\nДля генерации изображения с выбранным стилем используйте:")
    console.print("[bold]wombo create \"ваш запрос\" --style ID_СТИЛЯ[/bold]") 