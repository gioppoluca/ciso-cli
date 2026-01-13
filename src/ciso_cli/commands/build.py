import typer
from rich.console import Console

from ciso_cli.config import get_settings
from ciso_cli.api.client import CisoApiClient

app = typer.Typer(help="Build / version commands")
console = Console()


@app.command("info")
def info(ctx: typer.Context):
    client = ctx.obj["client"]
    out = client.get("/api/build/")
    console.print("[green]OK[/green] Connected.")
    if out is not None:
        console.print(out)