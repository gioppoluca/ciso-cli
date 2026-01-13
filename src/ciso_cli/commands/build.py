import typer
from rich.console import Console

from ciso_cli.config import get_settings
from ciso_cli.api.client import CisoApiClient

app = typer.Typer(help="Build / version commands")
console = Console()


@app.command("info")
def build_info() -> None:
    """
    Calls GET /api/build/ as connection/auth test.
    """
    settings = get_settings()

    client = CisoApiClient(
        base_url=str(settings.url),
        api_token=settings.api_token,
        timeout=settings.timeout,
        verify_tls=settings.verify_tls,
    )

    try:
        result = client.get("/api/build/")
        console.print("[green]OK[/green] Connected to CISO Assistant API.")
        if result is not None:
            console.print(result)
        else:
            console.print("[dim](No response body)[/dim]")
    finally:
        client.close()
