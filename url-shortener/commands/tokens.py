from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens

app = typer.Typer(
    name="token",
    help="Tokens management.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(
            help="The token to check",
        ),
    ],
):
    """
    Check if the passed token is valid - exists or not
    """
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[green]exists[/green]."
            if redis_tokens.token_exists(token)
            else "[red]does not exists[/red]."
        ),
    )


@app.command(name="list")
def list_tokens():
    """
    Список всех токенов
    """
    print(Markdown("# Available API Tokens"))
    print(Markdown("\n- ".join([""] + redis_tokens.get_tokens())))
    print()
