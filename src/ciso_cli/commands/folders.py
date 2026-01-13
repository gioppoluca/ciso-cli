import typer
from rich.console import Console

from ciso_cli.api.resources import FoldersResource

app = typer.Typer(help="Folders (domains) commands")
console = Console()


@app.command("resolve")
def resolve(ctx: typer.Context, domain: str = typer.Option(..., "--domain", help="Folder name or path")):
    client = ctx.obj["client"]
    folders = FoldersResource(client)
    console.print(folders.resolve_id(domain))


@app.command("create-child")
def create_child(
    ctx: typer.Context,
    parent: str = typer.Option(..., "--parent", help="Parent folder domain (name or path)"),
    child_name: str = typer.Option(..., "--child-name", help="New child folder name to create"),
    description: str | None = typer.Option(None, "--description", help="Optional folder description"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Do not POST, only show payload"),
):
    """
    Create a new folder attached to an existing parent folder.
    This uses POST /api/folders/ with {"name": child_name, "parent": <parent_uuid>}.
    """
    client = ctx.obj["client"]
    folders = FoldersResource(client)

    parent_id = folders.resolve_id(parent)
    payload = folders.build_create_payload(
        name=child_name,
        parent_id=parent_id,
        description=description,
    )

    if dry_run:
        console.print(payload)
        return

    created = folders.create(payload)
    console.print("[green]OK[/green] Folder created.")
    if created is not None:
        console.print(created)
