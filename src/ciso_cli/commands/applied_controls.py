from __future__ import annotations

from pathlib import Path
from typing import Optional, Any

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ciso_cli.io import TableReader
from ciso_cli.api.resources import (
    AppliedControlsResource,
    FoldersResource,
    ReferenceControlsResource,
)

app = typer.Typer(help="Applied controls import/export")
console = Console()


@app.command("import")
def import_applied_controls(
    ctx: typer.Context,
    file: Path = typer.Option(
        ..., "--file", exists=True, dir_okay=False, help="CSV or XLSX file"
    ),
    sheet: Optional[str] = typer.Option(
        None, "--sheet", help="Excel sheet name (optional)"
    ),
    required_control_col: str = typer.Option(
        "required control",
        "--required-control-col",
        help="Column containing reference control ref_id",
    ),
    domain_col: str = typer.Option(
        "domain",
        "--domain-col",
        help="Column containing domain (maps to folder name/path)",
    ),
    name_col: str = typer.Option(
        "name", "--name-col", help="Applied control name column"
    ),
    description_col: str = typer.Option(
        "description", "--description-col", help="Description column"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Do not POST, only print payloads"
    ),
) -> None:
    """
    Import applied controls:
      - required control (ref_id string) -> reference_control UUID
      - domain -> folder UUID
      - POST /api/applied-controls/

    Notes:
    - Column names are case-sensitive as read from file headers (we only strip spaces).
    - Use --dry-run to validate lookups/payloads without creating objects.
    """
    reader = TableReader()
    try:
        rows = reader.read(file, sheet=sheet)
    except Exception as e:
        raise typer.BadParameter(str(e))

    if not rows:
        console.print("[yellow]No rows found.[/yellow]")
        raise typer.Exit(code=0)

    client = ctx.obj["client"]

    ref_controls = ReferenceControlsResource(client)
    folders = FoldersResource(client)
    applied = AppliedControlsResource(client)

    # per-run caches to avoid repeated lookups
    ref_cache: dict[str, str] = {}
    folder_cache: dict[str, str] = {}

    created = 0
    failed = 0

    with Progress(
        SpinnerColumn(), TextColumn("{task.description}"), transient=True
    ) as progress:
        task = progress.add_task("Importing applied controls...", total=len(rows))

        for idx, row in enumerate(rows, start=1):
            try:
                ref_id = str(row.get(required_control_col, "") or "").strip()
                domain = str(row.get(domain_col, "") or "").strip()
                name = str(row.get(name_col, "") or "").strip()

                # description may be non-string (Excel cell)
                raw_desc: Any = row.get(description_col, None)

                if not name:
                    raise ValueError(f"Row {idx}: missing '{name_col}'")
                if not ref_id:
                    raise ValueError(f"Row {idx}: missing '{required_control_col}'")
                if not domain:
                    raise ValueError(f"Row {idx}: missing '{domain_col}'")

                ref_uuid = ref_cache.setdefault(ref_id, ref_controls.resolve_id(ref_id))
                folder_uuid = folder_cache.setdefault(
                    domain, folders.resolve_id(domain)
                )

                payload = applied.build_create_payload(
                    name=name,
                    reference_control_id=ref_uuid,
                    folder_id=folder_uuid,
                    description=str(raw_desc) if raw_desc not in (None, "") else None,
                )

                if dry_run:
                    console.print(payload)
                else:
                    applied.create(payload)
                    created += 1

            except Exception as e:
                failed += 1
                console.print(f"[red]Row {idx} failed:[/red] {e}")

            finally:
                progress.advance(task)

    console.print(f"[green]Created:[/green] {created}  [red]Failed:[/red] {failed}")
