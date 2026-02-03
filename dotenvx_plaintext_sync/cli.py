import click
import logging

from dotenvx_plaintext_sync import encryption, decryption


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
def cli(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
    )


@cli.command()
@click.argument("env")
@click.option("--update", is_flag=True, help="Update existing values (with confirmation)")
def encrypt(env: str, update: bool) -> None:
    encryption.main(env, update=update)


@cli.command()
@click.argument("env")
def decrypt(env: str) -> None:
    decryption.main(env)


@cli.command()
@click.argument("env")
def pull(env: str) -> None:
    decryption.pull(env)


@cli.command()
def init() -> None:
    from dotenvx_plaintext_sync.init import run_init
    run_init()


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
