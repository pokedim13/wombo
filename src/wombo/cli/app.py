import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional, List, Annotated

from wombo import __version__, Dream, AsyncDream
from wombo.models import StyleModel

console = Console()
app = typer.Typer(
    name="wombo",
    help="CLI для библиотеки Wombo - генерация изображений с помощью нейросети dream.ai",
    add_completion=False,
)

def version_callback(value: bool):
    if value:
        console.print(f"[bold green]Wombo CLI[/bold green] версия: [bold]{__version__}[/bold]")
        raise typer.Exit()

@app.callback()
def main(
    version: Annotated[Optional[bool], typer.Option("--version", "-v", help="Показать версию и выйти", callback=version_callback)] = False,
):
    """
    CLI для библиотеки Wombo - генерация изображений с помощью нейросети dream.ai
    """
    pass

if __name__ == "__main__":
    app() 