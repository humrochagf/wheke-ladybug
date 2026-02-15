import typer
from rich.console import Console
from typer import Context
from wheke import get_container

from .service import get_social_service

cli = typer.Typer(short_help="Social commands")
console = Console()


@cli.command()
def create_db(ctx: Context) -> None:
    container = get_container(ctx)
    service = get_social_service(container)

    console.print("Creating database...")

    service.users.create_table()
    service.posts.create_table()
