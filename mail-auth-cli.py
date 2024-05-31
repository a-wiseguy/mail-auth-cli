import os
import click
import imaplib
import smtplib
import ssl
from click.exceptions import ClickException


def test_imap_connection(host, port, user, passw, verbose):
    try:
        if verbose:
            click.echo(f"Connecting to IMAP server {host}:{port} as {user}...")
        mail = imaplib.IMAP4_SSL(host, port)
        mail.login(user, passw)
        mail.logout()
        click.echo("IMAP connection successful.")
    except Exception as e:
        raise ClickException(f"IMAP connection failed: {e}")


def test_smtp_connection_tls(host, port, user, passw, verbose):
    try:
        if verbose:
            click.echo(f"Connecting to SMTP server {host}:{port} as {user} with TLS...")
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(user, passw)
        server.quit()
        click.echo("SMTP connection successful.")
    except Exception as e:
        raise ClickException(f"SMTP connection failed: {e}")


def test_smtp_connection_ssl(host, port, user, passw, verbose):
    try:
        if verbose:
            click.echo(f"Connecting to SMTP server {host}:{port} as {user} with SSL...")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(user, passw)
            server.quit()
        click.echo("SMTP connection successful.")
    except Exception as e:
        raise ClickException(f"SMTP connection failed: {e}")


@click.command(
    help="Test IMAP and SMTP connection details using the provided credentials. "
    "You can specify the connection details either through command-line options or a configuration file, but not both."
)
@click.option(
    "--config-file",
    type=click.File("r"),
    help="Configuration file with connection details in JSON format.",
)
@click.option("--imap-host", help="IMAP server host.")
@click.option(
    "--imap-port",
    default=993,
    show_default=True,
    help="IMAP server port (default: 993).",
)
@click.option("--smtp-host", help="SMTP server host.")
@click.option(
    "--smtp-port",
    default=None,
    help="SMTP server port (default: 465 for SSL, 587 for TLS).",
)
@click.option("--username", help="Username for login.")
@click.option(
    "--password",
    envvar="EMAIL_PASSWORD",
    help="Password for login. If not provided, you will be prompted.",
    hide_input=True,
)
@click.option(
    "--use-tls",
    is_flag=True,
    default=False,
    help="Use TLS for SMTP connection (default: False).",
)
@click.option("--verbose", is_flag=True, default=False, help="Enable verbose output.")
@click.option(
    "--test-imap", is_flag=True, default=False, help="Test IMAP connection only."
)
@click.option(
    "--test-smtp", is_flag=True, default=False, help="Test SMTP connection only."
)
def main(
    config_file,
    imap_host,
    imap_port,
    smtp_host,
    smtp_port,
    username,
    password,
    use_tls,
    verbose,
    test_imap,
    test_smtp,
):
    if config_file:
        if any([imap_host, smtp_host, username, password]):
            raise ClickException(
                "Cannot use both configuration file and CLI options together. Please use only one method."
            )
        import json

        try:
            config = json.load(config_file)
            imap_host = config.get("imap_host")
            imap_port = config.get("imap_port", 993)
            smtp_host = config.get("smtp_host")
            smtp_port = config.get("smtp_port", 587 if config.get("use_tls") else 465)
            username = config.get("username")
            password = config.get("password")
            use_tls = config.get("use_tls", False)
            test_imap = config.get("test_imap", False)
            test_smtp = config.get("test_smtp", False)
        except json.JSONDecodeError:
            raise ClickException(
                "Invalid configuration file format. Please provide a valid JSON file."
            )
    else:
        if not all([imap_host, smtp_host, username, password]):
            raise ClickException(
                "Missing required options for CLI. Please provide imap-host, smtp-host, username, and password."
            )

    if not smtp_port:
        smtp_port = 587 if use_tls else 465

    if not password:
        password = click.prompt("Password", hide_input=True, confirmation_prompt=True)

    if not test_smtp and not test_imap:
        test_imap = test_smtp = True  # Default to testing both if neither flag is set

    if test_imap and imap_host:
        test_imap_connection(imap_host, imap_port, username, password, verbose)

    if test_smtp and smtp_host:
        if use_tls:
            test_smtp_connection_tls(smtp_host, smtp_port, username, password, verbose)
        else:
            test_smtp_connection_ssl(smtp_host, smtp_port, username, password, verbose)
    elif test_smtp and not smtp_host:
        click.echo("SMTP host not provided.", err=True)


if __name__ == "__main__":
    main()
