# Simple IMAP and SMTP Credential Tester

This CLI tool allows you to test IMAP and SMTP connection details using provided credentials. 
You can specify the connection details either through command-line options or a configuration file, but not both.

## Features

- Test IMAP and SMTP connections.
- Support for SSL and TLS.
- Provide credentials through CLI or a JSON configuration file.
- Verbose mode for detailed connection information.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/a-wiseguy/mail-auth-cli.git
```

2. Navigate to the project directory:

```sh
cd mail-auth-cli
```

3. (Optional) Create a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

4. Install the required packages:

```sh
pip install -r requirements.txt
```

## Usage

You can run the script using either CLI options or a JSON configuration file.

### Using CLI Options

```sh
python mail-auth-cli.py --imap-host <IMAP_HOST> --smtp-host <SMTP_HOST> --username <USERNAME> --password <PASSWORD> [OPTIONS]
```

### Using a Configuration File

Create a JSON file (e.g., `config.json`) with the following structure:

```json
{
  "imap_host": "mail.example.com",
  "imap_port": 993,
  "smtp_host": "mail.example.com",
  "smtp_port": 465,
  "username": "user@example.com",
  "password": "passwordhere",
  "use_tls": false,
  "test_imap": true,
  "test_smtp": true
}
```

Run the script with the configuration file:

```sh
python mail-auth-cli.py --config-file config.json
```

### Command-Line Options

- `--config-file` : Configuration file with connection details in JSON format.
- `--imap-host` : IMAP server host.
- `--imap-port` : IMAP server port (default: 993).
- `--smtp-host` : SMTP server host.
- `--smtp-port` : SMTP server port (default: 465 for SSL, 587 for TLS).
- `--username` : Username for login.
- `--password` : Password for login. If not provided, you will be prompted.
- `--use-tls` : Use TLS for SMTP connection (default: False).
- `--verbose` : Enable verbose output.
- `--test-imap` : Test IMAP connection only.
- `--test-smtp` : Test SMTP connection only.

### Example

Testing both IMAP and SMTP connections with verbose output:

```sh
python mail-auth-cli.py --imap-host mail.example.com --smtp-host mail.example.com --username user@example.com --password passwordhere --verbose
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## Issues

If you encounter any issues, please create a new issue in the [GitHub repository](https://github.com/a-wiseguy/mail-auth-cli/issues).

## Contact

For any inquiries, please contact [arvin@wise-it.dev](mailto:arvin@wise-it.dev).

