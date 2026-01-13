import typer
from rich.console import Console
from ciso_cli.api.resources import ReferenceControlsResource

app = typer.Typer()
console = Console()

@app.command("resolve")
def resolve(ctx: typer.Context, ref_id: str = typer.Option(..., "--ref-id")):
    client = ctx.obj["client"]
    rc = ReferenceControlsResource(client)
    console.print(rc.resolve_id(ref_id))
