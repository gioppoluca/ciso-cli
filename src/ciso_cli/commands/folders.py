import typer
from rich.console import Console
from ciso_cli.api.resources import FoldersResource

app = typer.Typer()
console = Console()

@app.command("resolve")
def resolve(ctx: typer.Context, domain: str = typer.Option(..., "--domain")):
    client = ctx.obj["client"]
    folders = FoldersResource(client)
    console.print(folders.resolve_id(domain))
