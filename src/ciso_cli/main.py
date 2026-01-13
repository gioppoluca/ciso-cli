import typer

from ciso_cli.config import get_settings
from ciso_cli.api.client import CisoApiClient

from ciso_cli.commands.build import app as build_app
from ciso_cli.commands.folders import app as folders_app
from ciso_cli.commands.reference_controls import app as ref_controls_app
from ciso_cli.commands.applied_controls import app as applied_controls_app

app = typer.Typer(help="CISO Assistant CLI")

app.add_typer(build_app, name="build")
app.add_typer(folders_app, name="folders")
app.add_typer(ref_controls_app, name="reference-controls")
app.add_typer(applied_controls_app, name="applied-controls")


@app.callback()
def main(ctx: typer.Context):
    """
    Initialize shared objects (API client) for all subcommands.
    """
    # Click/Typer may pass ctx.obj=None unless we initialize it
    if ctx.obj is None:
        ctx.obj = {}

    s = get_settings()

    # Create the client once per CLI invocation
    ctx.obj["client"] = CisoApiClient(
        base_url=str(s.url),
        api_token=s.api_token,
        timeout=s.timeout,
        verify_tls=s.verify_tls,
    )


if __name__ == "__main__":
    app()
