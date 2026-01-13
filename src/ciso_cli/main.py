import typer

from ciso_cli.commands.build import app as build_app

app = typer.Typer(help="CISO Assistant CLI")
app.add_typer(build_app, name="build")


def main():
    app()


if __name__ == "__main__":
    main()
